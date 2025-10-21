FROM python:3.11

# Instalar bibliotecas nativas necessárias
RUN apt-get update && apt-get install -y \
    libzbar0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Diretório de trabalho
WORKDIR /bot

# Copiar e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código do bot
COPY . .

# Comando para rodar o bot

CMD ["python", "ColetasCodBarraMultiplos.py"]

