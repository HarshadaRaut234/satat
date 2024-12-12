make and activate virtual environment followed by installing dependencies
```sh
python -m venv satat_env
source satat_env/bin/activate # run activate.PS1 or activate.bat file for windows
pip install -r requirements.txt
cd satat_backend
python manage.py runserver
```