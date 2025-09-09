# Dockerfile
FROM python:3.11-slim

# Variáveis para runtime mais limpo
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    # Torna 'run' importável a partir de /app/src
    PYTHONPATH=/app/src

# Diretório de trabalho
WORKDIR /app

# Dependências do sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Instalar libs Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY src/web/ ./src

# Porta interna do app
EXPOSE 8040

# Healthcheck simples: tenta conectar na porta (ajuste se quiser endpoint HTTP)
HEALTHCHECK --interval=30s --timeout=5s --retries=5 CMD python -c "import socket,sys;s=socket.socket();s.settimeout(2);s.connect(('127.0.0.1',8040));s.close()" || exit 1

# Comando de execução corrigido para waitress-serve encontrar o módulo correto
CMD ["waitress-serve", "--port=8040", "dash_app:server"]
