# Runemerchant [![Build Status](https://travis-ci.org/arlyon/runemerchant.svg?branch=master)](https://travis-ci.org/arlyon/runemerchant)

An api and web app for tracking your runescape trading.

## Getting started

### API

The api is fairly simple to get started with. Just clone the app,
set up a virtual environment, run the tests, and finally deploy.

```bash
git clone git@github.com:arlyon/runemerchant.git
cd runemerchant
python -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
./manage.py test
./manage.py migrate
./manage.py runserver
```

There are a set of management commands for downloading items, icons,
and price data as well as item fixtures.

### Web App

![interface](./demo.png)

The web app is written with Typescript and React and bundled with
webpack. To start, edit the `API_URL` in the webpack config to an
instance of the API, and run `yarn build` in the merchapp directory.
The app will be outputted to /dist/ which can be uploaded to a host of
your choice.