import os
import sys
import random
import datetime
import requests
from flasksite import db, bcrypt
from flasksite.models import User
from lorem_text import lorem

host = 'localhost'  # host where the system is running
port = 5000  # port where the process is running


def reload_database():
    exit_reload = False
    try:
        response = requests.get(f'http://{host}:{port}')
        print('The website seems to be running. Please stop it and run this file again.', file=sys.stderr)
        exit_reload = True
    except:
        pass
    if exit_reload:
        exit(11)
    try:
        os.remove('flasksite/site.db')
        print('previous DB file removed')
    except:
        print('no previous file found')

    db.create_all()

    # creating two users
    hashed_password = bcrypt.generate_password_hash('testing').decode('utf-8')
    default_user1 = User(username='Default',
                         email='default@test.com',
                         image_file='another_pic.jpeg',
                         password=hashed_password)
    db.session.add(default_user1)

    hashed_password = bcrypt.generate_password_hash('testing2').decode('utf-8')
    default_user2 = User(username='Default Second',
                         email='second@test.com',
                         image_file='7798432669b8b3ac.jpg',
                         password=hashed_password)
    db.session.add(default_user2)

    hashed_password = bcrypt.generate_password_hash('testing3').decode('utf-8')
    default_user3 = User(username='Default Third',
                         email='third@test.com',
                         password=hashed_password)
    db.session.add(default_user3)

    # TODO: Here you should include the generation of rows for your database

    try:
        db.session.commit()
        print('\nFinalized - database created successfully!')
    except Exception as e:
        print('The operations were not successful. Error:', file=sys.stderr)
        print(e, file=sys.stderr)
        db.session.rollback()


if __name__ == '__main__':
    reload_database()
