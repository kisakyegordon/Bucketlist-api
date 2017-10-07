#!flask/bin/python
import os
from app import create_app

#config_name = os.getenv('APP_SETTINGS')
app = create_app('testing')

if __name__ == '__main__':
    app.run()