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

Downloading items, icons, and price data is fairly easy. There are
django commands available for each of the three tasks. Getting set up
from a fresh database is as simple as running them.

However, due to how long it takes for the items to download, there is a
fixture included that has all the item information included. So then,
instead of downloading all of them you will only need the most recently
added ones.

```bash
./manage.py loaddata items.json
./manage.py get_items
./manage.py get_icons
./manage.py get_prices
```

There are additional fixtures for commonly used tags, runes, and spells.

```bash
./manage.py loaddata tags.json
./manage.py loaddata taggeditems.json
./manage.py loaddata runes.json
./manage.py loaddata spells.json
./manage.py loaddata requiredrunes.json
```

Keeping the item and prices list up to date is easy too, thanks to
[huey](https://huey.readthedocs.io/en/latest/index.html), a simple
task queue using redis. If you have redis installed, simply modify
`settings.py` to point towards it and run the worker.

```bash
./manage.py run_huey
```

### Web App

![interface](./demo.png)

The web app is written with Typescript and React and bundled with
webpack. To start, edit the `API_URL` in the webpack config to an
instance of the API, and run `yarn build` in the merchapp directory.
The app will be outputted to /dist/ which can be uploaded to a host of
your choice.