FROM python:3.9-slim

# Instalar herramientas necesarias
RUN apt-get update && apt-get install -y git curl && rm -rf /var/lib/apt/lists/*

# Instalar pytest para ejecutar las pruebas
COPY requirements.txt /
RUN pip install -r requirements.txt

WORKDIR /workspaces/experiment_python
COPY . /workspaces/experiment_python

RUN python /workspaces/experiment_python/create_db.py

# Configuración de las credenciales del usuario para evitar problemas de permisos
ARG USERNAME=vscode
RUN if [ "$USERNAME" != "root" ]; then useradd -m $USERNAME && chown -R $USERNAME /workspaces/experiment_python; fi

# [Optional] Set the default user. Omit if you want to keep the default as root.
USER $USERNAME
