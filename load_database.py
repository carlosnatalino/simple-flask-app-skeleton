import os
import sys
import random
import datetime
import requests
from flasksite import db, bcrypt, app
from flasksite.models import User
from lorem_text import lorem

host = 'localhost'  # host where the system is running
port = 5000  # port where the process is running


def reload_database():
    exit_reload = False
    try:
        response = requests.get(f'http://{host}:{port}')
        app.logger.critical('The website seems to be running. Please stop it and run this file again.')
        exit_reload = True
    except:
        pass
    if exit_reload:
        exit(11)
    try:
        os.remove('flasksite/site.db')
        app.logger.info('previous DB file removed')
    except:
        app.logger.info('no previous DB file found')

    assert not os.path.exists('flasksite/site.db'), 'It seems that site.db was not deleted. Please delete it manually!'

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

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        app.logger.critical('Error while committing the user insertion.')
        app.logger.exception(e)

    # testing if the users were added correctly
    assert len(User.query.all()) == 3, 'It seems that user failed to be inserted!'

    # TODO: Here you should include the generation of rows for your database

    try:
        db.session.commit()
        app.logger.info('Finalized - database created successfully!')
    except Exception as e:
        db.session.rollback()
        app.logger.critical('The operations were not successful.')
        app.logger.exception(e)


def query_database():
    # listing all the users
    users = User.query.all()
    print('\nAll users:')
    for user in users:
        print('\t', user)


if __name__ == '__main__':
    reload_database()
    query_database()
