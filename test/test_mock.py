import unittest
import boto3
from moto import mock_s3

@mock_s3
class TestMockClassLevel(unittest.TestCase):

    def create_my_bucket(self):
        s3 = boto3.resource('s3')
        bucket = s3.Bucket("mybucket")
        bucket.create()
        assert 1 == 1

    def test_1_should_create_bucket(self):
        self.create_my_bucket()

        client = boto3.client("s3")
        assert len(client.list_buckets()["Buckets"]) == 1

    def test_2_bucket_still_exists(self):
        client = boto3.client("s3")
        assert len(client.list_buckets()["Buckets"]) == 1
