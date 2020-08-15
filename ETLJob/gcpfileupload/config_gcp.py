import os

def set_gcs_environ():
    os.environ['GCP_BUCKET_NAME'] = "jobcrawl-bucket"
    os.environ['GCP_FOLDER_NAME'] = 'demo/'
    os.environ['LOCAL_FOLDER'] = "C:\\Users\\manoh\\Videos\\JobMarket\\search"


def set_bigquery_environ():
    os.environ['GCP_BIGQUERY_DATASET'] = 'jobfunnel'
    os.environ['GCP_BIGQUERY_TABLE'] = 'jobinfo'
    os.environ['TARGET_URI'] = 'gs://jobcrawl-bucket/demo/master_list.csv'





