"""
Author : Lavaraja
Email: lavaraja.padala@gmail.com
"""

import os
from config import *
from google.oauth2 import service_account
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from google.cloud import vision
from google.cloud import storage
from google.protobuf import json_format
from doc_txt_detect import detect_hand_writtent_text
credentials = service_account.Credentials.from_service_account_file(GCP_SERVICE_AUTH_FILE)

print("""
1.This model requires input in a folder.Please keep all the input file in single folder. 
2.Create a folder 001 under parent directory and store all test  data  inside the folder.
Example: 

|---data
|   ----001
|       ------ input1.pdf
|       ------ input2.pdf
|       ------ input3.pdf

3. Pass the parent folder name to python program

ex: "/home/lavaraja/mlproject/data" 

""")

input_dir=str(input("Please enter top level directory of the test data: "))

if os.path.isdir(input_dir):
    print("Input directory path is valid")
else:
    print("\n Entered path is not valid please check the format and enter again ")
    os._exit(1)

data_dir=os.path.abspath(input_dir)

if not os.path.isdir(os.path.abspath(data_dir)+"/001"):
    print("Could not find the input directory (001) in entered path. Please check the input path")
    os._exit(2)

if not os.path.exists(os.path.abspath(data_dir)+"/output/"):
        os.makedirs(os.path.abspath(data_dir)+"/output/")

for input_file in os.listdir(data_dir+"/001"):
    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.get_bucket(BUCKET_NAME)
    blob = bucket.blob("input/"+input_file)
    blob.upload_from_filename(os.path.abspath(data_dir)+"/001/"+input_file)
    gcs_source_uri = "gs://" + BUCKET_NAME + INPUT_BUCKET_PATH+input_file
    gcs_destination_uri= "gs://" + BUCKET_NAME + OUTPUT_BUCKET_DIR
    detect_hand_writtent_text(gcs_source_uri,gcs_destination_uri , os.path.abspath(data_dir)+"/output/"+input_file)
print("All files are processed. Please find the output in data/output directory..")

#gcs_destination_uri="gs://mldata101/"
#gcs_source_uri="gs://mldata101/FORM-FREETEXTINOUTBOXES_4.pdf"
#async_detect_document(gcs_source_uri,gcs_destination_uri,"result.txt"