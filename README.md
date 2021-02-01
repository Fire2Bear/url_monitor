# URL MONITOR

## Setup
```
git clone https://github.com/Fire2Bear/url_monitor.git
cd url_monitor
python3 -m venv ../venv_url_monitor
source ../venv_url_monitor/bin/activate
pip install -r requirements.txt
cp url_monitor/example_dev_settings.py url_monitor/local_settings.py
python manage.py migrate
```
## Initial datas
Pour que l'application fonctionne on doit tout d'abord ajouter 
via l'interface d'administration Django les 3 types de vérification
actuellement développés. 
Un type pour chaque Identifiant unique (HTTP, TXT, TIME)
