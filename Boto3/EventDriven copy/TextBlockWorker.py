import json
from ..main_async_q import upload_file

# Receives Input from Document Text Blocks
def handle(message):
    content = message['data']['payload']['text_block']['text']
    payload = {"inputs": content}
    upload_file(payload)

if __name__ == '__main__':
    with open('./Boto3/EventDriven/SampleEvents/InputNotification-Kafka.json', 'r') as data:
        obj = json.load(data)
        handle(obj)
