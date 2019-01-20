Language: Python
Runtime version:2.7

Other requirements : This code uses Google Vision API to detect the hand written text in documents.So we need google
cloud service account created for this purpose. This service request will be used in  API call to google cloud.


Step1 :

Follow below instruction create a service account and once the service account file created copy the file.
https://docs.bmc.com/docs/PATROL4GoogleCloudPlatform/10/creating-a-service-account-key-in-the-google-cloud-platform-project-799095477.html

The service account needs to have below privileges:
1.Storage bucket admin- To create/modify buckets/items
2.Privileges to create/use machine learning models on google cloud

once the service is created download the .json file containing credentials to access the Cloud API


Step2 :

Please update config.py for below values: (Or you can  default values .)

################# Config section ############ (config.py file)

BUCKET_NAME="mldata101"                       -- Bucket for storing data temporarily
INPUT_BUCKET_PATH="/input/"                   -- input directory name in the above bucket
OUTPUT_BUCKET_DIR="/output/"                   -- output directory name in the above bucket
GCP_SERVICE_AUTH_FILE="testkey.json"           -- Service file created in Google cloud.

####################################################



Step3 :

Environment setup :

Please run below commands to setup environment

1. sudo apt update
2. sudo apt install python
3. sudo apt install python-pip
4. pip install -r requirements.txt



Running the code :

1. I have created one default service account in GCP and that can be used for testing the code.
2. Create a  directory with name "data" and create a folder with name "001"  and place all input files testing the model.

|---data
|   ----001
|       ------ input1.pdf
|       ------ input2.pdf
|       ------ input3.pdf

3. Now run the code

    python input_ml.py

    input:
             Please enter top level directory of the test data: "/home/lavaraja/test/data/"

 4. Once done output will be available under output directory inside data folder.


 Thanks.