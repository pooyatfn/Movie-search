import os

API_URL = "https://imdb146.p.rapidapi.com/v1/find/"

ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL', 'http://elasticsearch:9200')
ELASTICSEARCH_PASSWORD = os.environ.get('ELASTICSEARCH_PASSWORD', 'SomePass@')
ELASTICSEARCH_USER = os.environ.get('ELASTICSEARCH_USER', 'elastic')

REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', 'SomePass@')
REDIS_PORT = os.environ.get('REDIS_PORT', 6379)

HOSTNAME = os.environ.get('HOSTNAME', 'localhost')
