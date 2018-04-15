import os

from runemerchant.settings import BASE_DIR

ICONS_DIR = os.path.join(BASE_DIR, 'merchapi/static/icons')

if not os.path.exists(ICONS_DIR):
    os.makedirs(ICONS_DIR)
