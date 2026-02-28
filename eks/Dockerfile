FROM node:22-slim

WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    curl \
    git \
    python3 \
    && rm -rf /var/lib/apt/lists/*

# Instala OpenClaw globalmente
RUN npm install -g openclaw

# Cria diretório de dados
RUN mkdir -p /data/.openclaw/workspace

# Configura variáveis de ambiente
ENV OPENCLAW_DATA_DIR=/data/.openclaw
ENV NODE_ENV=production

# Porta do gateway
EXPOSE 18789

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:18789/ || exit 1

CMD ["openclaw", "gateway", "start", "--foreground"]
