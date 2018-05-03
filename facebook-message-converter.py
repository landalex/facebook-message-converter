import json
import argparse
import heapq
from datetime import datetime

DATE_FORMAT = '%Y.%m.%d'
TIME_FORMAT = '%H:%M:%S'
MESSAGE_KEY = 2

parser = argparse.ArgumentParser(description='FB Message Archive Converter')
parser.add_argument('--in', dest='archivePath', required=True, help="Path to JSON archive")
parser.add_argument('--out', dest='outPath', required=True, help="Path to output file")
parser.add_argument('--format', dest='format', required=True, help='txt or json, for conversation-analyzer or FacebookChatStatistics respectively')
args = parser.parse_args()

with open(args.archivePath, 'r') as json_file:
    data = json.load(json_file)

heap = []
senders = set()
tiebreaker_counter = 0
for message in data['messages']:
    message_datetime = datetime.fromtimestamp(int(message['timestamp']))
    if 'content' not in message:
        continue
    if 'json' in args.format:
        sender = message['sender_name'].encode('iso-8859-1').decode('utf-8')
        senders.add(sender)
        new_message = {
            "date": message_datetime.isoformat(),
            "sender": sender,
            "message": message['content'].encode('iso-8859-1').decode('utf-8')
        }
    else:
        new_message = "{date} {time} {sender} {message}\n".format(date=message_datetime.strftime(DATE_FORMAT),
                                                                  time=message_datetime.strftime(TIME_FORMAT),
                                                                  sender=message['sender_name'].replace(' ', '').encode(
                                                                      'iso-8859-1').decode('utf-8'),
                                                                  message=message['content'].replace('\n', ' ').encode(
                                                                      'iso-8859-1').decode('utf-8'))
    heapq.heappush(heap, (int(message['timestamp']), tiebreaker_counter, new_message))
    tiebreaker_counter += 1

messages = sorted(heap, key=lambda x: x[0])
messages = [message[MESSAGE_KEY] for message in messages]
if 'json' in args.format:
    json_output = {
        "threads": [
            {
                "participants": list(senders),
                "messages": messages
            }
        ]
    }
    with open(args.outPath, 'w', encoding='utf-8') as out_file:
        out_file.write(json.dumps(json_output))
else:
    with open(args.outPath, 'w', encoding='utf-8') as out_file:
        out_file.writelines(messages)
