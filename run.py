#!flask/bin/python
"""Module that starts the application"""
from app import create_app

#config_name = os.getenv('APP_SETTINGS')
app = create_app('testing')

if __name__ == '__main__':
    app.run()
