import logging
import io
import threading
from datetime import datetime
from typing import List, Set
import mysql.connector
from mysql.connector import errorcode
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
)
from pyzbar.pyzbar import decode as decode_barcode
from PIL import Image
from config_bot_ColetaBFF import TELEGRAM_TOKEN, MYSQL_CONFIG

# --- CONFIGURAÇÃO ---
# Lista de setores disponíveis para seleção
SETORES_DISPONIVEIS = ["STL", "SAU", "PCD", "Oficina"]

salvar_lock = threading.Lock()

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Este conjunto ainda é útil para um rápido controle de quem está com a câmera "ativa"
usuarios_coletando: Set[int] = set()

# --- FUNÇÃO DE BANCO DE DADOS ATUALIZADA ---
def salvar_codigos(codigos: List[str], setor: str) -> int:
    """
    Salva uma lista de códigos de barras no banco de dados, associando-os a um setor.
    Retorna a quantidade de códigos novos inseridos.
    Retorna 0 se todos os códigos já existiam.
    Retorna -1 em caso de erro.
    """
    if not setor:
        logger.error("Tentativa de salvar códigos sem um setor definido.")
        return -1 # Erro, pois o setor é obrigatório

    codigos = list(set(codigos))
    conn = None
    cursor = None
    try:
        with salvar_lock:
            conn = mysql.connector.connect(**MYSQL_CONFIG)
            cursor = conn.cursor()

            if codigos:
                query_codigos_existentes = "SELECT barcode FROM coletados WHERE barcode IN (%s)" % ",".join(['%s'] * len(codigos))
                cursor.execute(query_codigos_existentes, tuple(codigos))
                codigos_salvos = {item[0] for item in cursor.fetchall()}
            else:
                codigos_salvos = set()

            codigos_novos = [c for c in codigos if c not in codigos_salvos]

            if not codigos_novos:
                logger.info("Nenhum código novo para inserir. Todos já existem.")
                return 0

            now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Query de inserção atualizada para incluir o campo 'setor'
            sql_insert = "INSERT INTO coletados (barcode, data_coleta, status, setor) VALUES (%s, %s, %s, %s)"
            # Valores para inserir atualizados para incluir a variável 'setor'
            valores_para_inserir = [(codigo, now_str, "Novo", setor) for codigo in codigos_novos]

            cursor.executemany(sql_insert, valores_para_inserir)
            conn.commit()

            return len(codigos_novos)

    except mysql.connector.errors.IntegrityError as err:
        if err.errno == errorcode.ER_DUP_ENTRY:
            logger.warning(f"Tentativa de inserir código(s) duplicado(s) detectada: {err}")
            return 0
        else:
            logger.error(f"Erro de integridade no banco de dados: {err}")
            return -1
    except mysql.connector.Error as err:
        logger.error(f"Erro geral no banco de dados ao salvar códigos: {err}")
        return -1
    finally:
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

# --- FUNÇÕES DO BOT (HANDLERS) ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Inicia a conversa, limpa o estado anterior do usuário e pede para escolher um setor.
    """
    # Limpa dados de sessões anteriores para garantir uma seleção de setor nova
    context.user_data.clear()
    user_id = update.effective_user.id
    usuarios_coletando.discard(user_id)

    # Cria o teclado com as opções de setor
    keyboard = [SETORES_DISPONIVEIS[i:i + 2] for i in range(0, len(SETORES_DISPONIVEIS), 2)]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

    await update.message.reply_text(
        "👋 Olá! Bem-vindo ao Coletor de Códigos.\n\n"
        "Primeiro, por favor, selecione o seu setor:",
        reply_markup=reply_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Gerencia todas as mensagens de texto, direcionando para a ação correta
    baseado no texto da mensagem e no estado atual do usuário.
    """
    user_id = update.effective_user.id
    texto_mensagem = update.message.text

    # Lógica 1: Usuário está escolhendo um setor
    if texto_mensagem in SETORES_DISPONIVEIS:
        context.user_data['setor'] = texto_mensagem
        logger.info(f"Usuário {user_id} selecionou o setor: {texto_mensagem}")

        keyboard = [["📷 Iniciar coleta"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(
            f"Setor '{texto_mensagem}' selecionado com sucesso!\n\n"
            "Clique em '📷 Iniciar coleta' para começar a enviar as fotos.",
            reply_markup=reply_markup
        )
        return

    # Lógica 2: Usuário quer iniciar a coleta (e já deve ter escolhido um setor)
    if texto_mensagem == "📷 Iniciar coleta":
        if 'setor' not in context.user_data:
            await update.message.reply_text("❗ Por favor, selecione seu setor primeiro. Use /start para ver as opções.")
            return

        setor_selecionado = context.user_data['setor']
        usuarios_coletando.add(user_id)
        keyboard = [["🛑 Parar coleta"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(
            f"✅ Modo coleta iniciado para o setor: *{setor_selecionado}*.\n\n"
            "Agora envie quantas fotos quiser. Quando terminar, clique em '🛑 Parar coleta'.",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        return

    # Lógica 3: Usuário quer parar a coleta
    if texto_mensagem == "🛑 Parar coleta":
        usuarios_coletando.discard(user_id)
        # Mantém o botão de iniciar para o caso de quererem fazer outra coleta no mesmo setor
        keyboard = [["📷 Iniciar coleta"]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(
            "🛑 Coleta finalizada!\n\n"
            f"O setor '{context.user_data.get('setor', 'N/D')}' ainda está selecionado. "
            "Você pode iniciar uma nova coleta ou usar /start para trocar de setor.",
            reply_markup=reply_markup
        )
        return

async def ler_codigo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Processa as fotos enviadas para extrair e salvar códigos de barras.
    """
    user_id = update.effective_user.id
    # Proteção: só processa fotos se o usuário estiver no modo de coleta
    if user_id not in usuarios_coletando:
        return

    # Proteção: Verifica se um setor foi definido para este usuário
    if 'setor' not in context.user_data or not context.user_data['setor']:
        await update.message.reply_text(
            "❌ Erro: Setor não definido. Por favor, pare a coleta e inicie novamente com /start para selecionar um setor."
        )
        return
    
    setor_atual = context.user_data['setor']

    file = None
    if update.message.photo:
        file = await update.message.photo[-1].get_file()
    elif (update.message.document and update.message.document.mime_type.startswith("image/")):
        file = await update.message.document.get_file()
    else:
        # Esta mensagem provavelmente não será vista pois o handler filtra por imagem, mas é uma boa prática
        await update.message.reply_text("❗ Por favor, envie uma foto ou imagem do código de barras.")
        return

    try:
        img_bytes = await file.download_as_bytearray()
        image = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        barcodes = decode_barcode(image)
    except Exception as e:
        logger.error("Erro ao processar imagem ou decodificar: %s", e)
        await update.message.reply_text("❌ Erro ao processar a imagem. Tente novamente.")
        return

    if not barcodes:
        await update.message.reply_text("⚠️ Nenhum código de barras encontrado. Tente novamente, evite reflexos ou borrões.")
        return

    codigos_lidos = [barcode.data.decode("utf-8").strip() for barcode in barcodes if barcode.data]

    if not codigos_lidos:
        await update.message.reply_text("⚠️ Não foi possível extrair códigos válidos da imagem.")
        return

    # Passa os códigos e o setor para a função de salvar
    qtd_novos = salvar_codigos(codigos_lidos, setor_atual)

    if qtd_novos == -1:
         await update.message.reply_text("❌ Ocorreu um erro grave ao salvar os dados. Por favor, contate o administrador.")
    elif qtd_novos == 0:
        await update.message.reply_text(
            f"ℹ️ Códigos já Coletados!\n\nSetor: *{setor_atual}*\nCódigos detectados:\n" +
            "\n".join(sorted(set(codigos_lidos))),
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text(
            f"✅ Código(s) lido(s) com sucesso!\n\nSetor: *{setor_atual}*\nCódigos:\n" +
            "\n".join(sorted(set(codigos_lidos))) +
            f"\n\n*{qtd_novos}* código(s) novo(s) salvo(s) no banco de dados.",
            parse_mode='Markdown'
        )
        logger.info(f"Códigos salvos para o setor {setor_atual}: {codigos_lidos}")

def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Adiciona os handlers
    app.add_handler(CommandHandler("start", start))
    # Um único handler de mensagem de texto gerencia as diferentes etapas da conversa
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    # O handler de imagem permanece o mesmo, mas a lógica interna foi atualizada
    app.add_handler(MessageHandler(filters.PHOTO | filters.Document.IMAGE, ler_codigo))

    logger.info("🤖 Bot coletor de códigos (v2 - com setores) rodando...")
    app.run_polling()

if __name__ == "__main__":
    main()
