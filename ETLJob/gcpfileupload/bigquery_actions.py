from google.cloud import bigquery
from os import environ
from ETLJob.gcpfileupload.config_gcp import set_bigquery_environ


def bigquery_createtable(targetURI, datasetId, tableId):


    bigquery_client = bigquery.Client.from_service_account_json('credentials.json')
    dataset_ref = bigquery_client.dataset(datasetId)
    job_config = bigquery.LoadJobConfig()
    job_config.autodetect = True
    job_config.skip_leading_rows = 1
    job_config.field_delimiter = '|'
    job_config.source_format = bigquery.SourceFormat.CSV
    uri = targetURI
    load_job = bigquery_client.load_table_from_uri(uri,
                                                   dataset_ref.table(tableId),
                                                   job_config=job_config)

if __name__ == '__main__':
    set_bigquery_environ()
    bigquery_createtable(environ.get('TARGET_URI'), environ.get('GCP_BIGQUERY_DATASET'),
                                     environ.get('GCP_BIGQUERY_TABLE'))