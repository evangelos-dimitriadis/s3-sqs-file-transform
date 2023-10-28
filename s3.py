import logging
import boto3
from pathlib import Path
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


class s3Wrapper:
    """Encapsulates S3 object actions."""
    def __init__(self, s3_resource: type[boto3]) -> None:
        """
        :param s3_resource: A Boto3 s3 low-level service client
        """
        self.s3_resource = s3_resource

    def upload(self, file: str, bucket_name: str) -> None:
        """
        Upload a file.
        :param file_name: The file to upload including the path to the file to upload.
        :param bucket_name: The name of the bucket.
        """
        try:
            key = Path(file).name
        except FileNotFoundError:
            logger.exception(f"No such file: '{file}'.")
            raise

        try:
            self.s3_resource.upload_file(Filename=file, Bucket=bucket_name, Key=key)
            waiter = self.s3_resource.get_waiter('bucket_exists')
            waiter.wait(Bucket=bucket_name, WaiterConfig={'Delay': 5, 'MaxAttempts': 10})
            logger.info(f"Upload object {key} to bucket {bucket_name}.")
        except ClientError:
            logger.exception("Couldn't upload object {key} to bucket {bucket_name}.")
            raise

    def download(self, file: str, bucket_name: str) -> None:
        """
        Download the file_name
        :param file: The file to download including the path to the file to download to.
        :param bucket_name: The name of the bucket.
        """
        try:
            key = Path(file).name
        except FileNotFoundError:
            logger.exception(f"No such file: '{file}'.")
            raise

        try:
            self.s3_resource.download_file(Filename=file, Bucket=bucket_name, Key=key)
            logger.info(f"Download file {key} from bucket {bucket_name}.")
        except ClientError:
            logger.exception(f"Couldn't download file {key} from bucket {bucket_name}.")
            raise
