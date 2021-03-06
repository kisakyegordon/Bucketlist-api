[![Build Status](https://travis-ci.org/freshprincekla/Bucketlist-api.svg?branch=master)](https://travis-ci.org/freshprincekla/Bucketlist-api)
[![Coverage Status](https://coveralls.io/repos/github/freshprincekla/Bucketlist-api/badge.svg?branch=master)](https://coveralls.io/github/freshprincekla/Bucketlist-api?branch=master)
[![BCH compliance](https://bettercodehub.com/edge/badge/freshprincekla/Bucketlist-api?branch=master)](https://bettercodehub.com/)

# Bucket list Api Application using flask framework

"The challenge of keeping track of dreams and goals is a need for many individuals that
requires an innovative and robust solution that will allow them to remember and share
the fun with others "

The innovative bucket list app is an application that allows users  to record and share
things they want to achieve or experience before reaching a certain age meeting the needs
of keeping track of their dreams and goals.

### Features:
* Users can create accounts
* Users can login
* Users can create. edit, view and delete bucket list
* Users can create, edit, view and delete bucket list items.

### ** Python Version **

Python 3.6.1

### Endpoints to create a user account and login into the application
HTTP Method|End point | Public Access|Action
-----------|----------|--------------|------
POST | /auth/register | True | Create an account
POST | /auth/login | True | Login a user
POST | /auth/logout | False | Logout a user
POST | /auth/reset-password | True | Reset a user password

#### Endpoints to create, update, view and delete a bucket list
HTTP Method|End point | Public Access|Action
-----------|----------|--------------|------
POST | /bucketlists | False | Create a bucket list
GET | /bucketlists | False | View all bucket lists
GET | /bucketlists/id | False | View details of a bucket list
PUT | /bucketlists/id | False | Updates a bucket list with a given id
DELETE | /bucketlists/id | False | Deletes a bucket list with a given id

#### Endpoints to create, update, view and delete a bucket list item
HTTP Method|End point | Public Access|Action
-----------|----------|--------------|------
GET | /bucketlists/id/items | False | View Items of a given list id
GET | /bucketlists/id/items/<item_id> | False | View details of a particular item on a given list id
POST | /bucketlists/id/items | False | Add an Item to a bucket list
PUT | /bucketlists/id/items/<item_id> | False | Update a bucket list item on a given list
DELETE | /bucketlists/id/items/<item_id> | False | Delete a bucket list item from a given list




## ** Installation **

#### Step 1
Install a  virtualenvwrapper
A Virtual Environment is a tool to keep the dependencies required by different projects in separate places, by creating virtual Python environments for them.
To install  the virtualenvwrapper follow the link installing [Installing Virtual Environment](http://docs.python-guide.org/en/latest/dev/virtualenvs/).

#### Step 2
Clone Github repository

```
https://github.com/freshprincekla/Bucketlist-api.git

```

#### Step 3
Install the required dependencies

```
$ pip install -r requirements.txt

```
or

```
$ pip install --upgrade -r requirements.txt

```

#### Step 5
### Running the application
Navigate to the root directory and and run the following command:

```
$ python run.py

```