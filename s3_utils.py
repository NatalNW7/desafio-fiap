import boto3
from botocore.exceptions import ClientError
import os
import json

s3_client = boto3.client('s3')

def upload_file(file_name, bucket, object_name=None):
    """Carregar um arquivo para um bucket S3

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    try:
        with open(file_name, "rb") as f:
            response = s3_client.upload_fileobj(f,  bucket, object_name)
        print(f"Arquivo {object_name} criado")
    except ClientError as e:
        print(e)
        return False
    return True
    
    
def delete_file(bucket, key):
    response = s3_client.delete_object(
        Bucket=bucket, 
        Key=key
    )
        
    print(json.dumps(response, indent=4))
        

if __name__ == '__main__':
    nomeDoBucket = "tudojunto2-341463"
    arquivoLocal="img/arquitetura.png"
    arquivoLocal2="img/aws.png"
    
    upload_file(arquivoLocal, nomeDoBucket)