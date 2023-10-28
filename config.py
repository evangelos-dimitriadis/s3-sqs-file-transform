import os

SERVER_BUCKET = os.getenv('SERVER_BUCKET') or 'serverbucket4321'
CLIENT_BUCKET = os.getenv('CLIENT_BUCKET') or 'clientbucket4321'
QUEUE_URL = os.getenv('QUEUE_URL') or 'http://localhost:4566/000000000000/my-queue'
QUEUE_REGION = os.getenv('QUEUE_REGION') or 'eu-central-1'
ENDPOINT_URL = os.getenv('ENDPOINT_URL') or None
AWS_PROFILE = os.getenv('AWS_PROFILE') or 'default'
AWS_REGION = os.getenv('AWS_REGION') or 'eu-central-1'
