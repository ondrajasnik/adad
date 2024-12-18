# Použij oficiální základní image Pythonu
FROM python:3.10-slim

# Nastav pracovní adresář v kontejneru
WORKDIR /app

# Zkopíruj obsah aktuálního adresáře do kontejneru na /app
COPY . .

# Nainstaluj potřebné závislosti
RUN pip install --no-cache-dir -r requirements.txt

# Otevři port, na kterém poběží Flask
EXPOSE 5000

# Nastav proměnné prostředí pro produkční režim aplikace
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Spusť Flask aplikaci v režimu vývoje
CMD ["flask", "run"]
