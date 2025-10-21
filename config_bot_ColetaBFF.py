import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv('.env.local')

# Token do Telegram
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

if not TELEGRAM_TOKEN:
    raise ValueError("TOKEN_DO_BOT_NAO_CONFIGURADO: Defina a variável de ambiente TELEGRAM_TOKEN")

# Configurações do Banco de Dados MySQL usando variáveis de ambiente
MYSQL_CONFIG = {
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'host': os.getenv('MYSQL_HOST', 'localhost'),  # Altere para o IP do seu servidor Docker
    'port': int(os.getenv('MYSQL_PORT', 3306)),
    'database': os.getenv('MYSQL_DATABASE', 'basealephbff')
}

# Validação de configurações críticas
if not MYSQL_CONFIG['password']:
    raise ValueError("SENHA_BANCO_NAO_CONFIGURADA: Defina a variável de ambiente MYSQL_PASSWORD")