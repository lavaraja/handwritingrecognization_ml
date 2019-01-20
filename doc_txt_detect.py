from google.oauth2 import service_account
from config import *
# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from google.cloud import vision
from google.cloud import storage
from google.protobuf import json_format
credentials = service_account.Credentials.from_service_account_file(GCP_SERVICE_AUTH_FILE)


def detect_hand_writtent_text(gcs_source_uri, gcs_destination_uri,input_file):
    """OCR with PDF/TIFF as source files on GCS"""

    import re
    # Supported mime_types are: 'application/pdf' and 'image/tiff'
    mime_type = 'application/pdf'
    # How many pages should be grouped into each json output file.
    batch_size = 1
    client = vision.ImageAnnotatorClient(credentials=credentials)
    feature = vision.types.Feature(
        type=vision.enums.Feature.Type.DOCUMENT_TEXT_DETECTION)
    gcs_source = vision.types.GcsSource(uri=gcs_source_uri)
    print("Processing File "+input_file.split("/")[-1]+" ...")
    input_config = vision.types.InputConfig(
        gcs_source=gcs_source, mime_type=mime_type)
    gcs_destination = vision.types.GcsDestination(uri=gcs_destination_uri)
    output_config = vision.types.OutputConfig(
        gcs_destination=gcs_destination, batch_size=batch_size)
    async_request = vision.types.AsyncAnnotateFileRequest(
        features=[feature], input_config=input_config,
        output_config=output_config)
    operation = client.async_batch_annotate_files(
        requests=[async_request])

    print('Waiting for the operation to finish.')
    operation.result(timeout=180)

    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.get_bucket(bucket_name=BUCKET_NAME)
    # Process the first output from API
    blob=bucket.blob("output/output-1-to-1.json")
    json_string = blob.download_as_string()
    response = json_format.Parse(
        json_string, vision.types.AnnotateFileResponse())
    # The actual response for the first page of the input file.
    page_response = response.responses[0]
    annotation = page_response.full_text_annotation
    f = open(input_file.split('.')[0]+".txt", "a")
    result=annotation.text
    print(result)
    f.write(annotation.text)
    f.close()
    print("Completed Processing File.The output is available at " + input_file + " ...")
    return True

#gcs_destination_uri="gs://mldata101/"
#gcs_source_uri="gs://mldata101/FORM-FREETEXTINOUTBOXES_4.pdf"
#async_detect_document(gcs_source_uri,gcs_destination_uri,"result.txt")