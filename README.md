# Passo a Passo
>  Python 3.8 usado!
## Download e instalação
''' bash
git clone https://github.com/hfa2020/evagas
cd evagas
pip install -r requirements.txt
'''
## Testes e set up
### Testes
''' bash
python manage.py test
'''
### Setup para uso
''' bash
python manage.py makemigrations usuarios oportunidades
python manage.py migrate
python manage.py collectstatic
python manage.py runserver
'''