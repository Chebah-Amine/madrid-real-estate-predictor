# Etape 1: Utiliser une image de base officielle Python, version 3.8 slim
FROM python:3.11

RUN apt-get update \
    &&  apt-get install -y --no-install-recommends \
    locales apt-utils git libicu-dev g++ libpng-dev libxml2-dev libzip-dev libonig-dev libxslt-dev unzip libpq-dev nodejs npm wget \
    apt-transport-https lsb-release ca-certificates

RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen  \
    &&  echo "fr_FR.UTF-8 UTF-8" >> /etc/locale.gen \
    &&  locale-gen

# Etape 2: Définir le répertoire de travail dans le conteneur
WORKDIR /psid

# Etape 3: Copier les fichiers requirements.txt dans le conteneur
COPY requirements.txt .

# Etape 4: Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Etape 7: Définir la commande pour démarrer l'application
CMD tail -f /dev/null

# Etape 8: Définir le user
RUN useradd -ms /bin/bash api-user

RUN chown -R api-user:api-user /psid

RUN chmod 755 /psid

USER api-user

