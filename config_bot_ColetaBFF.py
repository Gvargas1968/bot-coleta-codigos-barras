import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv('.env.local')

# Token do Telegram
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', '7843033735:AAH93o7O0DGb_aSwC33W_lSpkF5IQmqsL8o')

# Configurações do Banco de Dados MySQL usando variáveis de ambiente
MYSQL_CONFIG = {
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', 'M$&dff!ch'),
    'host': os.getenv('MYSQL_HOST', 'localhost'),  # Altere para o IP do seu servidor Docker
    'port': int(os.getenv('MYSQL_PORT', 3306)),
    'database': os.getenv('MYSQL_DATABASE', 'basealephbff')
}