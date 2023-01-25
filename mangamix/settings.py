import os

ES_HOST = os.getenv('ES_HOST', 'http://localhost:9200')
ES_USER = os.getenv('ES_USER', 'elastic')
ES_PASSWORD = os.getenv('ES_PASSWORD', 'dzNIt6zKlFN5ynoOlnsD')
ES_INDEX = os.getenv('ES_INDEX', 'mangamix')
S3_HOST = os.getenv('S3_HOST', 'localhost:9000')
S3_ACCESS_KEY = os.getenv('S3_ACCESS_KEY', 'minio')
S3_SECRET_KEY = os.getenv('S3_SECRET_KEY', 'minio123')
S3_BUCKET = os.getenv('S3_BUCKET', 'mangamix')
MMX_SEARCH_SIZE = int(os.getenv('MMX_SEARCH_SIZE', '10'))
MMX_ANIMES = os.getenv('MMX_ANIMES').split(',') if os.getenv('MMX_ANIMES') else []
