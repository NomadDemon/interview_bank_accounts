# Bank accounts interview task
Simple tool to manage fake bank accounts

## Features
- create accounts
- create deposits
- create withdrawals
- create transfers between accounts
- added currency support


## How to install

App was tested and developed on Ubuntu 20.04, so instruction will be based on Ubuntu experience
app is based on docker-compose, so you will have to have installed docker and docker-compose

- install docker [snap or apt]
- install docker-compose
- enter folder with downloaded repo
- sudo docker-compose build
- sudo docker-compose run web python manage.py migrate
- sudo docker-compose up
- app now should be ready to test on http://0.0.0.0:8000/


## How to run tests
```
sudo docker-compose run web pytest
```


## Disclaimer

- You need to use same currency for transfer and accounts at same time
- You first need to create currency, then account
- I should use factoryboy / faker, but its small app, so...
- I used normal django templating frontend as app interface
- Mostly no type annotations
- Forms my be duplicated, but... explicit is better than implicit :)
- There may be some leftovers as empty files or many settings files. I used my own "web_station" codebase as base of this app and incorporated some good practices I found in my own projects [anyway, they were stripped by many lines]
- Code formatted by isort + black
- Frontend is... simple AF... but it works :)

# And most important
You need to create .env file in same folder where dockerfile is

minimum .env lines are
```
ENV_TYPE='DEV'
APP_NAME='bank accounts'
SERVER_URL='www.bank-accounts.local'
SECRET_KEY='django-insecure-)3!%(@@$f1d^-7+8#-6c@zh*0gqm4)3@2709y4nsm(*%exao%p'

```
