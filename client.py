import boto3
import argparse
from s3 import s3Wrapper
from config import AWS_PROFILE, AWS_REGION, ENDPOINT_URL, CLIENT_BUCKET


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Upload a file to a S3 bucket.')
    parser.add_argument("file", metavar="file", type=str,
                        help="A file to upload to the client")
    args = parser.parse_args()
    file = args.file

    try:
        # Create a custom session
        session = boto3.Session(profile_name=AWS_PROFILE, region_name=AWS_REGION)
        s3_resource = session.client('s3', endpoint_url=ENDPOINT_URL)

        bucket_name = CLIENT_BUCKET
        s3 = s3Wrapper(s3_resource)
        s3.upload(file, bucket_name)
    except FileNotFoundError:
        print(f"No such file: '{file}'.")
    except Exception as e:
        print(f"Something went wrong with the Client: {e}")
