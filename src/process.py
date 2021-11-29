import os
import json
import boto3
import awswrangler as wr
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_stepfunctions_message(event):
    return event['detail']['requestParameters']['key']

def read_parquet_from_s3(raw_path, moto_s3=None):
    df = wr.s3.read_parquet(path=raw_path)
    return df

def df_processes(df):
    df['ano'] = df['data'].apply(lambda x: x.split('-')[0])
    df['mes'] = df['data'].apply(lambda x: x.split('-')[1])
    df['dia'] = df['data'].apply(lambda x: x.split('-')[2])
    df = df.drop(columns=['data'])
    print(df)
    return df

def write_parquet_on_s3(df, processed_path,  moto_s3=None):
    result = wr.s3.to_parquet(
        df=df,
        path=processed_path,
        dataset=True,
        compression="snappy",
        partition_cols=['ano', 'mes', 'dia']
    )
    return result


def handler(event, context):
    try:
        logger.info(event)

        # ENVIRONMENT VARIABLES
        DATALAKE_BUCKET = os.environ["DATALAKE_BUCKET"]

        # Key dos objetos
        raw_key = get_stepfunctions_message(event)
        processed_key = 'processed'

        # Paths de leitura e escrita
        raw_path = 's3://{}/{}'.format(DATALAKE_BUCKET, raw_key)
        processed_path = 's3://{}/{}/'.format(DATALAKE_BUCKET, processed_key)

        # Leitura do arquivo do s3 RAW a partir do evento recebido do SQS
        df = read_parquet_from_s3(raw_path)

        df = df_processes(df)

        result = write_parquet_on_s3(df, processed_path)

        ##########################
        #
        # Atualiza as partições na tabela do glue
        #
        #########################

    except Exception as e:
        logger.error(e)
