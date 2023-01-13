import json, io, time
from botocore.exceptions import ClientError

def upload_file(client,payload,bucket,key):
    payload = json.dumps(payload)
    fo = io.BytesIO(bytes(payload,'UTF-8'))
    return client.upload_fileobj(fo, bucket,key)

def download_file(sess,bucket,key):
    # keep making request until the file is found
    while True:
        try:
            return sess.read_s3_file(bucket=bucket, key_prefix=key)
        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchKey":
                print("waiting for output...")
                time.sleep(2)
                continue
            raise