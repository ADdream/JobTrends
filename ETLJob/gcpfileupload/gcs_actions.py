import os
from os import environ, listdir
from os.path import isfile
from google.cloud import storage
from ETLJob.gcpfileupload.config_gcp import set_gcs_environ


def uploadFiles():
    set_gcs_environ()
    storage_client = storage.Client.from_service_account_json('credentials.json')
    bucket_name = environ.get('GCP_BUCKET_NAME')
    bucket_folder = environ.get('GCP_FOLDER_NAME')
    local_folder = environ.get('LOCAL_FOLDER')

    bucket = storage_client.get_bucket(bucket_name)
    files_list = [f for f in listdir(local_folder) if isfile(os.path.join(local_folder, f))]
    for file_name in files_list:
        local_file = os.path.join(local_folder, file_name)
        blob = bucket.blob(bucket_folder + file_name)
        blob.upload_from_filename(local_file)
    return f'Uploaded {files_list} to "{bucket_name}" bucket.'

if __name__ == '__main__':
    uploadFiles()