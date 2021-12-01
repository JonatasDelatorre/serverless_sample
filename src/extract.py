import json
import os
import logging
import awswrangler as wr

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_sns_message(event):
    message = json.loads(event['Records'][0]['body'])['Message']
    source_key = json.loads(message)['Records'][0]['s3']['object']['key']
    return source_key

def read_csv_from_s3(source_path):
    df = wr.s3.read_csv(path=source_path)
    return df

def write_parquet_on_s3(df, raw_path):
    result = wr.s3.to_parquet(
        df=df,
        path=raw_path,
        dataset=True,
        compression="snappy",
        partition_cols=['data']
    )
    return result

def handler(event, context):

    try:
        logger.info(event)

        # ENVIRONMENT VARIABLES
        DATALAKE_BUCKET = os.environ["DATALAKE_BUCKET"]
        
        # Get object key from event message
        source_key = get_sns_message(event)
        raw_key = 'raw'
        
        source_path = 's3://{}/{}'.format(DATALAKE_BUCKET, source_key)
        raw_path = 's3://{}/{}/'.format(DATALAKE_BUCKET, raw_key)

        # Get csv file from s3
        df = read_csv_from_s3(source_path)

        result = write_parquet_on_s3(df, raw_path)
    
    except Exception as e:
        logger.error(e)
