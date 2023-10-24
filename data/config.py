import os
import json

PORT = os.getenv('PORT')
EMAIL = os.getenv('EMAIL')
DB_URI = os.getenv('DB_URI')
SMTP_HOST = os.getenv('SMTP_HOST')
SMTP_PORT = os.getenv('SMTP_PORT')
SMTP_LOGIN = os.getenv('SMTP_LOGIN')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
SMTP_EMAIL = os.getenv('SMTP_EMAIL')
SMTP_NAME = os.getenv('SMTP_NAME')

DB_NAME = 'test_task'

# sha256 "ООО Эйс Плэйс"
API_KEY = '124b0fc76e1df9c405f87d059a4227b46b72928ad14097a9fe456b4e0c18754d'

with open('data/templates.json', 'r', encoding='utf-8') as file:
    templates = json.load(file)