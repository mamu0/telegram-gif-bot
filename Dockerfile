FROM python:3.11-slim

# Imposta il working directory
WORKDIR /app

# Installa le dipendenze di sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copia i file del progetto
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia il codice dell'applicazione
COPY . .

# Imposta variabili di ambiente di default
ENV PYTHONUNBUFFERED=1

# Espone la porta (non usata direttamente, ma utile per documentazione)
EXPOSE 8080

# Comando di avvio
CMD ["python", "main.py"]
