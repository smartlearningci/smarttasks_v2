# RNF-02/RNF-06: imagem Python simples e reproduzível para formação.
FROM python:3.12-slim
WORKDIR /code
# Copiar primeiro dependências permite reutilizar a camada no rebuild.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# A aplicação é copiada depois das dependências.
COPY app/ ./app/
# Utilizador sem privilégios; não são necessárias credenciais.
RUN useradd --create-home appuser
USER appuser
EXPOSE 8000
# Um processo/worker para manter o armazenamento em memória coerente.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
