# %%
import os 
import tempfile
from google.cloud import storage
import zipfile
import datetime

# %%
def download_kaggle_to_gcs(dataset_path,bucket_name,gcp_project_name):
    storage_client = storage.Client(gcp_project_name)
    bucket = storage_client.bucket(bucket_name)

    with tempfile.TemporaryDirectory() as tmp:
        command = f'kaggle datasets download -d {dataset_path} -p {tmp}'
        result =os.system(command)

        if result !=0:
            raise RuntimeError("Error with downloading kaggledataset")
        
        zip_file_name =[f for f in os.listdir(tmp) if f.endswith('.zip')][0]
        zip_file_path = os.path.join(tmp,zip_file_name)

        with zipfile.ZipFile(zip_file_path,'r') as zip:
            zip.extractall(tmp)

        for f in os.listdir(tmp):
            if f.endswith('.csv'):
                local_path = os.path.join(tmp,f)
                blob_path =f'raw_data/{f}'
                blob = bucket.blob(blob_path)

                print(f"Updating {f}")
                blob.upload_from_filename(local_path)
    print('All updated')
