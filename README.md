# Bot de Coleta de Códigos de Barras

Bot do Telegram para coleta e armazenamento de códigos de barras com suporte a diferentes setores. O projeto permite que os usuários enviem fotos contendo códigos de barras para o bot, que então extrai e salva os códigos em um banco de dados MySQL, associando-os ao setor correspondente.

## Funcionalidades

- 📸 Leitura de códigos de barras a partir de fotos enviadas via Telegram
- 🏢 Suporte a diferentes setores (STL, SAU, PCD, Oficina)
- 💾 Armazenamento em banco de dados MySQL
- 🔄 Evita duplicatas (não salva códigos já existentes)
- 🛡️ Sistema de controle de sessão para evitar conflitos

## Tecnologias Utilizadas

- Python 3.11+
- python-telegram-bot (v22.1)
- MySQL Connector
- Pillow (PIL)
- pyzbar
- Docker

## Instalação e Configuração

### Pré-requisitos

- Python 3.11+
- MySQL Server
- Conta no Telegram
- Token de bot do Telegram

### Passos para Configuração

1. Clone este repositório:

```bash
git clone https://github.com/seu-usuario/bot-coleta-codigos-barras.git
cd bot-coleta-codigos-barras
```

2. Crie um ambiente virtual e instale as dependências:

```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente:

Crie um arquivo `.env.local` com as seguintes variáveis:

```env
TELEGRAM_TOKEN=seu_token_do_bot_aqui
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=seu_usuario
MYSQL_PASSWORD=sua_senha
MYSQL_DATABASE=nome_do_banco
```

4. Certifique-se de que o banco de dados MySQL esteja configurado com a tabela apropriada:

```sql
CREATE TABLE IF NOT EXISTS coletados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    barcode VARCHAR(255) UNIQUE NOT NULL,
    data_coleta DATETIME NOT NULL,
    status VARCHAR(50) NOT NULL,
    setor VARCHAR(50) NOT NULL
);
```

5. Teste a conexão com o banco de dados:

```bash
python test_db_connection.py
```

6. Execute o bot:

```bash
python ColetasCodBarraMultiplos.py
```

## Configuração com Docker

O projeto inclui um Dockerfile para facilitar a implantação:

```bash
# Build da imagem
docker build -t bot-coleta-codigos .

# Execução do container
docker run -d bot-coleta-codigos
```

## Uso

1. Inicie uma conversa com o bot no Telegram usando `/start`
2. Selecione seu setor a partir das opções disponíveis
3. Clique em "📷 Iniciar coleta" para ativar o modo de coleta
4. Envie fotos contendo códigos de barras
5. O bot processará cada imagem e salvará os códigos detectados
6. Ao terminar, clique em "🛑 Parar coleta"

## Estrutura do Projeto

```
bot1_coleta/
├── ColetasCodBarraMultiplos.py     # Código principal do bot
├── config_bot_ColetaBFF.py        # Configurações do bot
├── requirements.txt                # Dependências Python
├── test_db_connection.py           # Script de teste de conexão
├── INSTRUCOES.md                   # Instruções detalhadas
├── Dockerfile                      # Dockerfile para implantação
├── iniciar_bot.bat                 # Script de inicialização para Windows
├── .env.local                      # Configurações sensíveis (não commitado)
└── docker/                         # Configurações Docker adicionais
```

## Variáveis de Ambiente

- `TELEGRAM_TOKEN`: Token do bot fornecido pelo @BotFather no Telegram
- `MYSQL_HOST`: Host do servidor MySQL
- `MYSQL_PORT`: Porta do servidor MySQL (padrão: 3306)
- `MYSQL_USER`: Usuário do banco de dados
- `MYSQL_PASSWORD`: Senha do banco de dados
- `MYSQL_DATABASE`: Nome do banco de dados

## Segurança

- **ATENÇÃO**: Este projeto inclui valores padrão sensíveis que devem ser substituídos antes da implantação
- Os tokens e senhas reais são mantidos em arquivos de ambiente e ignorados pelo Git (graças ao .gitignore)
- Acesso controlado à câmera ativa com controle de sessão por usuário
- Prevenção de duplicatas no banco de dados
- **Proteção de dados sensíveis**:
  - Nunca commite arquivos .env ou .env.local
  - Sempre substitua os valores padrão antes de fazer deploy
  - Use variáveis de ambiente no ambiente de produção
  - O sistema agora valida a presença de variáveis críticas antes de iniciar

## Configuração de Segurança

Antes de executar o bot, é essencial configurar corretamente as variáveis de ambiente:

1. Crie um arquivo `.env.local` (já incluso no .gitignore)
2. Adicione as variáveis necessárias:

```env
TELEGRAM_TOKEN=seu_token_real_aqui
MYSQL_HOST=endereco_do_servidor
MYSQL_PORT=3306
MYSQL_USER=seu_usuario
MYSQL_PASSWORD=sua_senha_segura
MYSQL_DATABASE=nome_do_banco
```

3. Remova quaisquer valores padrão sensíveis que possam estar no código
4. Certifique-se de que o script de inicialização verifica a presença dessas variáveis

## Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Faça commit de suas alterações (`git commit -m 'Adiciona nova feature'`)
4. Envie para o branch remoto (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo LICENSE para detalhes.


Bot de Coleta de Códigos de Barras © 2025
