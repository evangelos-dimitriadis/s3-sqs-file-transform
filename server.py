import logging
import boto3
import json
from s3 import s3Wrapper
from xml_json import xml_json
from config import (AWS_PROFILE, AWS_REGION, ENDPOINT_URL, CLIENT_BUCKET, QUEUE_URL, QUEUE_REGION,
                    SERVER_BUCKET)


logging.basicConfig(level=logging.INFO)


def file_transform(s3_client: type[boto3], xml_file: str) -> None:
    """
    Downloads xml file from an s3 bucket and uploads json to another s3 bucket.
    :param xml_file: The xml file.
    :param s3_client: A Boto3 S3 low-level service client
    """
    try:
        s3 = s3Wrapper(s3_client)
        s3.download(xml_file, CLIENT_BUCKET)
        json_file = xml_json(xml_file)
        s3.upload(json_file, SERVER_BUCKET)
    except Exception as e:
        logging.exception(e)
        pass


def set_up_queue(sqs_client: type[boto3], s3_client: type[boto3]) -> None:
    """
    Finds and attaches a SQS to a S3 bucket.
    :param sqs_client: A Boto3 SQS low-level service client
    :param s3_client: A Boto3 S3 low-level service client
    """

    queue_arn = sqs_client.get_queue_attributes(QueueUrl=QUEUE_URL, AttributeNames=['QueueArn'])
    queue_arn = queue_arn['Attributes']['QueueArn']
    bucket_notification_config = {
        'QueueConfigurations': [
            {
                'QueueArn': queue_arn,
                'Events': [
                    's3:ObjectCreated:*',
                ]
            }
        ],
    }
    queue_policy = {
        "Version": "2008-10-17",
        "Id": "example-ID",
        "Statement": [{
            "Sid": "example-statement-ID",
            "Effect": "Allow",
            "Principal": {"AWS": "*"},
            "Action": ["SQS:SendMessage"],
            "Resource": queue_arn,
            "Condition": {
                "ArnLike": {"aws:SourceArn": "arn:aws:s3:*:*:" + CLIENT_BUCKET}
            }
        }]
    }
    # Set up the SQS to send messages regarding the CLIENT_BUCKET
    sqs_client.set_queue_attributes(QueueUrl=QUEUE_URL,
                                    Attributes={'Policy': json.dumps(queue_policy)})
    # Set up the notifications for the S3 bucket
    s3_client.put_bucket_notification_configuration(
        Bucket=CLIENT_BUCKET,
        NotificationConfiguration=bucket_notification_config
    )


def read_queue(sqs_client: type[boto3], s3_client: type[boto3]) -> None:
    """
    Reads from the SQS when a new object is created in the S3 bucket.
    :param sqs_client: A Boto3 SQS low-level service client
    :param s3_client: A Boto3 S3 low-level service client
    """
    while True:
        resp = sqs_client.receive_message(QueueUrl=QUEUE_URL, AttributeNames=['All'],
                                          MaxNumberOfMessages=10, WaitTimeSeconds=10)

        if 'Messages' not in resp:
            continue

        for message in resp['Messages']:
            # Read any new messages
            body = json.loads(message['Body'])
            try:
                record = body.get('Records')
                if record is None:
                    continue
                event_name = record[0].get('eventName')
            except Exception as e:
                logging.exception(f'Ignoring message because of error {str(e)}.')
                continue
            # Find if a new object has been created in s3
            try:
                if event_name and event_name.startswith('ObjectCreated'):
                    # New file created
                    s3_info = record[0]['s3']
                    if s3_info.get('bucket', {}).get('name') == CLIENT_BUCKET:
                        filename = s3_info['object']['key']
                        logging.info(f'A new file {filename} has been created on the client side.')
                        file_transform(s3_client, filename)

                # Delete read messages from the queue
                entries = [{'Id': msg['MessageId'], 'ReceiptHandle': msg['ReceiptHandle']}
                           for msg in resp['Messages']]
                resp = sqs_client.delete_message_batch(QueueUrl=QUEUE_URL, Entries=entries)
            except Exception as e:
                logging.exception(f'Ignoring object because of error {str(e)}.')
                continue


if __name__ == '__main__':
    try:
        # Create a custom session
        session = boto3.Session(profile_name=AWS_PROFILE, region_name=AWS_REGION)
        s3_client = session.client('s3', endpoint_url=ENDPOINT_URL)
        sqs_client = session.client('sqs', endpoint_url=ENDPOINT_URL, region_name=QUEUE_REGION)

        set_up_queue(sqs_client, s3_client)
        logging.info(f'Monitoring S3 backet {CLIENT_BUCKET} for new objects.')
        read_queue(sqs_client, s3_client)

    except KeyboardInterrupt:
        exit(0)
    except Exception:
        logging.exception("Something went wrong with the demo.")
