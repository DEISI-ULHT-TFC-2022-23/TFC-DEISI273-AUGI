# AUGI

Site Web : https://gaugi.herokuapp.com/

# Para instalação em máquina local

#Clonar projeto do Github para local

git clone "https://github.com/DEISI-ULHT-TFC-2022-23/TFC-DEISI273-AUGI.git"

#Ativar ambiente virtual

python -m venv venv

venv\scripts\activate.bat

#Instalar as dependências necessárias ao projeto

pip install -r requirements.txt

#Lançar o servidor do projeto

python manage.py runserver

Aceder via browser ao endereço http://127.0.0.1:8000/

# Para desinstalar 

pip uninstall -r requirements.txt -y

venv\scripts\deactivate.bat

rmdir /s venv      - Windows
