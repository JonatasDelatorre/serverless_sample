#coding=utf-8
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/src')
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
import json
import ast
import boto3
import pytest
import moto
import pandas as pd
import awswrangler as wr
from pandas.testing import assert_frame_equal

import extract
import process
from samples.data_samples import raw_dataframe
from samples.data_samples import processed_dataframe
from moto import mock_s3
BUCKET_NAME = "datalake-unittest"

@pytest.fixture(scope="function")
def moto_s3():
    with moto.mock_s3():
        s3 = boto3.resource("s3", region_name="us-east-1")
        bucket = s3.create_bucket(Bucket=BUCKET_NAME)
        bucket.upload_file('test/samples/source_csv.csv', 'source/source_csv.csv')
        bucket.upload_file('test/samples/raw_parquet.parquet', 'raw/raw_parquet.parquet')
        yield bucket

def test_raw_read_csv():
    path = "s3://{}/source/source_csv.csv".format(BUCKET_NAME)
    df = extract.read_csv_from_s3(path)
    assert len(df.index) == 3
    assert len(df.columns) == 2

def test_raw_write_parquet():
    path = "s3://{}/raw/".format(BUCKET_NAME)

    data = raw_dataframe
    df = pd.DataFrame(data)  

    result = extract.write_parquet_on_s3(df, path)
    def read_parquet_from_s3(raw_path):
    df = wr.s3.read_parquet(path=raw_path)
    return df
    assert result

def test_processed_read_parquet():
    path = "s3://{}/raw/raw_parquet.parquet".format(BUCKET_NAME)
    df = process.read_parquet_from_s3(path)
    assert len(df.index) == 3
    assert len(df.columns) == 2


def test_processed_write_parquet():
    path = "s3://{}/processed/".format(BUCKET_NAME)

    data = processed_dataframe
    df = pd.DataFrame(data)  

    result = process.write_parquet_on_s3(df, path)
    assert result

@mock_s3
class TestExtractFile(unittest.TestCase):    
       
    def test_lambda_sqs_message_input(self):
        
        with open('test/samples/source_sqs_message.txt') as f:
            contents = f.read()
            event = ast.literal_eval(contents)

        result = extract.get_sns_message(event)

        self.assertTrue(result)  

@mock_s3
class TestProcessFile(unittest.TestCase):    
       
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



