import os
import sys
import unittest
import boto3
import ast

sys.path.append(os.path.abspath(''))
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd

from moto import mock_s3
from pandas.testing import assert_frame_equal

from src import extract
from src import process
from samples.data_samples import raw_dataframe
from samples.data_samples import processed_dataframe


@mock_s3
class TestExtractFile(unittest.TestCase):    
    
    @classmethod
    @mock_s3
    def setUpClass(cls):
        s3 = boto3.resource('s3', region_name='us-east-1')
        cls.bucket_name = 'datalake-unittest'
        bucket = s3.create_bucket(Bucket=cls.bucket_name)

        bucket.upload_file('test/samples/source_csv.csv', 'source/source_csv.csv')

    def setUp(self):
        self.bucket_name = TestExtractFile.bucket_name

    def test_raw_read_csv(self):
        path = "s3://{}/source/source_csv.csv".format(self.bucket_name)
        df = extract.read_csv_from_s3(path)
        assert len(df.index) == 3
        assert len(df.columns) == 2

    def test_raw_write_parquet(self):
        path = "s3://{}/raw/".format(self.bucket_name)

        data = raw_dataframe
        df = pd.DataFrame(data)  

        result = extract.write_parquet_on_s3(df, path)
        self.assertTrue(result)  

    def test_lambda_sqs_message_input(self):
        
        with open('test/samples/source_sqs_message.txt') as f:
            contents = f.read()
            event = ast.literal_eval(contents)

        result = extract.get_sns_message(event)

        self.assertTrue(result)  

    # def test_2_bucket_still_exists(self):
    #     client = boto3.client("s3")
    #     assert len(client.list_buckets()["Buckets"]) == 1


@mock_s3
class TestProcessFile(unittest.TestCase):    
    
    @classmethod
    @mock_s3
    def setUpClass(cls):
        s3 = boto3.resource('s3', region_name='us-east-1')
        cls.bucket_name = 'datalake-unittest'
        bucket = s3.create_bucket(Bucket=cls.bucket_name)

        bucket.upload_file('test/samples/raw_parquet.parquet', 'raw/raw_parquet.parquet')

    def setUp(self):
        self.bucket_name = TestExtractFile.bucket_name

    def test_processed_read_parquet(self):
        path = "s3://{}/raw/raw_parquet.parquet".format(self.bucket_name)
        df = process.read_parquet_from_s3(path)
        assert len(df.index) == 3
        assert len(df.columns) == 2

    def test_processed_write_parquet(self):
        path = "s3://{}/processed/".format(self.bucket_name)

        data = processed_dataframe
        df = pd.DataFrame(data)  

        result = process.write_parquet_on_s3(df, path)
        assert result

    def test_lambda_stepfunction_message_input(self):
        
        with open('test/samples/raw_stepfunctions_message.txt') as f:
            contents = f.read()
            event = ast.literal_eval(contents)

        result = process.get_stepfunctions_message(event)

        self.assertTrue(result)  


    def test_df_processing(self):
        data_model = processed_dataframe
        df_model = pd.DataFrame(data_model)  

        data_initial = raw_dataframe
        df_initial = pd.DataFrame(data_initial)  

        df_final = process.df_processes(df_initial)
        assert_frame_equal(df_model, df_final)

if __name__ == '__main__':
    unittest.main()