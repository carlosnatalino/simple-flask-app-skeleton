"""
Integration test for the system.

Before starting the test, we setup by checking if the system is online.

The, we perform the following operations:
1 - Register
2 - Login

YOUR INTERMEDIATE STEPS HERE

Y - Logout
"""

import sys
import time
import random
import traceback
import requests
from lorem_text import lorem
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

wait_time = 1  # number of minutes to wait between actions
host = 'localhost'  # host where the system is running
port = 5000  # port where the process is running


def test_setup():

    # checking if the system is online
    try:
        response = requests.get(f'http://{host}:{port}')
        if response.status_code != 200:
            print(f'The website returned status code {response.status_code}!', file=sys.stderr)
            print(f'Check if the site is correctly configured and running!', file=sys.stderr)
            exit(10)  # stop the execution of the text
    except Exception as e:
        print(f'We are having troubles connecting to the system!', file=sys.stderr)
        print(f'Check if the site is correctly configured and running!', file=sys.stderr)
        print(f'Error description: {e}')
        exit(11)

    # setup the browser
    global driver
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    # driver.maximize_window()  # maximize the window
    driver.get(f'http://{host}:{port}')
    time.sleep(wait_time)


def test_register():
    driver.find_element_by_id('register').click()
    time.sleep(wait_time)

    driver.find_element_by_id('username').send_keys('new_user')
    driver.find_element_by_id('email').send_keys('new@user.com')
    driver.find_element_by_id('password').send_keys('user_password')
    driver.find_element_by_id('confirm_password').send_keys('user_password')
    driver.find_element_by_id('submit').click()
    time.sleep(wait_time)

    # validate if a success message is displayed
    try:
        driver.find_element_by_class_name('alert-success')
    except NoSuchElementException as nsee:
        raise AssertionError('The registering process seems to have failed! Check/reload your database!')


def test_register_duplicate_user():
    driver.find_element_by_id('register').click()
    time.sleep(wait_time)

    # testing first the username unique constraint
    driver.find_element_by_id('username').send_keys('new_user')
    driver.find_element_by_id('email').send_keys('new2@user.com')
    driver.find_element_by_id('password').send_keys('user_password')
    driver.find_element_by_id('confirm_password').send_keys('user_password')
    driver.find_element_by_id('submit').click()
    time.sleep(wait_time)

    # verifying if message is correctly displayed
    assert 'This username is taken. Please choose a different one.' in driver.page_source

    # testing second the email unique constraint
    driver.find_element_by_id('username').clear()
    driver.find_element_by_id('username').send_keys('new_user2')
    driver.find_element_by_id('email').clear()
    driver.find_element_by_id('email').send_keys('new@user.com')
    driver.find_element_by_id('password').send_keys('user_password')
    driver.find_element_by_id('confirm_password').send_keys('user_password')
    driver.find_element_by_id('submit').click()
    time.sleep(wait_time)

    # verifying if message is correctly displayed
    assert 'This email is taken. Please choose a different one.' in driver.page_source


def test_login():
    driver.find_element_by_id('login').click()
    time.sleep(wait_time)
    driver.find_element_by_id('email').send_keys('new@user.com')
    driver.find_element_by_id('password').send_keys('user_password')
    driver.find_element_by_id('submit').click()
    time.sleep(wait_time)

    assert 'Account' in driver.page_source


"""
here you should have the tests for the specific parts of your system
"""


def test_logout():
    driver.find_element_by_id('logout').click()
    time.sleep(wait_time)

    assert 'Account' not in driver.page_source


def test_teardown():
    try:
        driver.quit()
    except:
        pass


if __name__ == '__main__':
    stop = False

    # this version shows the errors in the output
    test_setup()

    if stop:
        i = input('Setup ran correctly. Proceed? [Y/n]')
        if i.strip().lower() == 'n':
            exit(12)
    # test_register()

    if stop:
        i = input('Register ran correctly. Proceed? [Y/n]')
        if i.strip().lower() == 'n':
            exit(12)
    test_register_duplicate_user()

    if stop:
        i = input('Test for duplicated users ran correctly. Proceed? [Y/n]')
        if i.strip().lower() == 'n':
            exit(12)
    test_login()

    if stop:
        i = input('Login ran correctly. Proceed? [Y/n]')
        if i.strip().lower() == 'n':
            exit(12)
    test_logout()

    if stop:
        i = input('Log out ran correctly. Proceed? [Y/n]')
        if i.strip().lower() == 'n':
            exit(12)
    test_teardown()
