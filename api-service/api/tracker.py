
import os
import asyncio
from glob import glob
import json

import tensorflow as tf
from google.cloud import storage


gcp_project = os.environ["GCP_PROJECT"]
bucket_name = "asl_best_model"
# local_experiments_path = "/persistent/experiments"
persistent_folder = "/api"
download_file = "Best_Model.h5"


def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    print("Downloading model...")
    storage_client = storage.Client(project=gcp_project)

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)
    

