import pytest
from s3 import s3Wrapper
from pathlib import Path


@pytest.fixture
def s3_test(s3_client):
    yield s3_client


def test_upload_download_s3(s3_test):
    s3 = s3Wrapper(s3_test)
    # Create a bucket
    s3_test.create_bucket(Bucket='test_bucket')

    file = Path(__file__).parent.parent.joinpath('examples/example.xml')

    res = s3.upload(file, 'test_bucket')
    assert res is None
    res = s3.download('example.xml', 'test_bucket')
    assert res is None
