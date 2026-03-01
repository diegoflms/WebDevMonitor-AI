FROM python:3.11-slim

# Define o diretório de trabalho
WORKDIR /app

# Instala ferramentas básicas
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código para dentro do container
COPY . .

# Roda o app usando a porta que o Railway mandar ($PORT)
CMD ["sh", "-c", "streamlit run app.py --server.port $PORT --server.address 0.0.0.0"]