import json, os,boto3,sagemaker
from utility.S3Utility import upload_file
from flask import Blueprint

text_block_bp = Blueprint('text_block', __name__)

ENDPOINT_NAME_Q = os.getenv("ENDPOINT_NAME_Q")

# PROCESS TEXT BLOCKS -> QUESTION MODEL INPUTS
@text_block_bp.route('/',methods=["POST"])
def handle(message = None):
    message = {
        "meta": {
            "message_id": "3aae5497-5c8b-44f8-b0e9-9b314f60a219",
            "message_timestamp": 1673419439543
        },
        "data": {
            "id": "45ac2a2961dc494696dbc62d0991938b",
            "type": "event",
            "event": "convos.text_block.created",
            "created_at": "2023-01-11T06:43:59.543015",
            "payload": {
                "text_block": {
                    "_id": "63be5aaec88789df50508a42",
                    "agent_id": "63be5800f06720a86c8ea2ce",
                    "organisation_id": "5dd7678079e96c691e71244c",
                    "document_id": "63be5aa5d8b1e1fffb9125b2",
                    "store_id": "62777bdf2d45f771b0ef2b00",
                    "file_id": "63be5aa5d8b1e1fffb9125b2/textblocks/p00001_i000002_paragraph",
                    "language_code": "en",
                    "from_page": 1,
                    "to_page": 1,
                    "index": 2,
                    "type": "paragraph",
                    "paragraph_count": 1,
                    "character_count": 369,
                    "checksum": "9511abd0a476cf7c887f737a12f44e92",
                    "is_processed": False,
                    "is_last_block": False,
                    "created_at": "2023-01-11T06:43:58.527000",
                    "updated_at": "2023-01-11T06:43:58.527000",
                    "text": "My new house is on a wide street with lots of trees. The upstairs floor of my house has three bedrooms and an office for working. The downstairs has a very large kitchen, a dining room with a table and six chairs, a living room with two green sofas, a television and curtains. In addition, it has a small terrace with pool where I can sunbathe in summer.",
                    "is_translated": True
                }
            }
        }
    }
    # Connections
    id = message['data']['payload']['text_block']['_id']
    s3_client = boto3.client("s3")
    sess = sagemaker.session.Session()

    # upload the file
    content = message['data']['payload']['text_block']['text']
    payload = {"inputs": content}
    s3_bucket = sess.default_bucket()
    key = f'async_inference_input/{ENDPOINT_NAME_Q}/{id}.in'

    upload_file(s3_client,payload,s3_bucket,key)

    return {}, 200

if __name__ == '__main__':
    with open('./Boto3/EventDriven/SampleEvents/InputNotification-Kafka.json', 'r') as data:
        obj = json.load(data)
        handle(obj)
