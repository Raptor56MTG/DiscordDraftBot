from decouple import config
import boto3


def upload():

    """This backs up the storage.json file to an S3 bucket
    on amazon. This is needed as heroku restarts dyno's every
    24 hours, causing local files to be erased. In order for
    the backup functionality to work, the storage.json file
    cannot be randomly erased."""

    client = boto3.client('s3',
                          aws_access_key_id=config('ACCESS_KEY'),
                          aws_secret_access_key=config('SECRET_ACCESS_KEY'))
    file = 'storage.json'
    bucket = 'discord-draft-bot'
    file_location = '/storage/storage.json'
    client.upload_file(file, bucket, file_location)


def load():

    """This downloads the storage.json file from the amazon
    s3 bucket, and allows for the draft to pick up from where
    it left off."""

    print("in load function")

    client = boto3.client('s3',
                          aws_access_key_id=config('ACCESS_KEY'),
                          aws_secret_access_key=config('SECRET_ACCESS_KEY'))

    bucket = 'discord-draft-bot'
    file = '/storage/storage.json'
    file_location = '../storage.json'

    print("preparing to download")

    print(client.download_file(bucket, file, file_location))

    print("downloaded the file")
