import sys
import json
import argparse
import heapq
from datetime import datetime
from collections import namedtuple

# Date and time format for conversation-analyzer's txt format
DATE_FORMAT = '%Y.%m.%d'
TIME_FORMAT = '%H:%M:%S'

# For storing messages in an object that the heap can sort
MessageTuple = namedtuple('MessageTuple', 'timestamp tiebreak_value message')

parser = argparse.ArgumentParser(description='FB Message Archive Converter')
parser.add_argument('--in', dest='archivePath', required=True, help="Path to JSON archive")
parser.add_argument('--out', dest='outPath', required=True, help="Path to output file")
parser.add_argument('--format', dest='format', required=True,
                    help='txt or json, for conversation-analyzer or FacebookChatStatistics respectively')
args = parser.parse_args()

with open(args.archivePath, 'r') as json_file:
    data = json.load(json_file)

heap = []
message_senders = set()
tiebreaker_counter = 0
for message in data['messages']:
    try:
        if 'timestamp_ms' in message:
            message_timestamp = int(message['timestamp_ms']) / 1000
        else:
            message_timestamp = int(message['timestamp'])
        message_datetime = datetime.fromtimestamp(message_timestamp)
        if 'content' not in message:
            # 'content' property contains the message text, other message types (stickers, media etc) use different
            # properties which aren't handled here
            continue
        sender = message['sender_name'].encode('raw_unicode_escape').decode('utf-8')
        message_content = message['content'].encode('raw_unicode_escape').decode('utf-8')
        if 'json' in args.format:
            message_senders.add(sender)
            new_message = {
                "date": message_datetime.isoformat(),
                "sender": sender,
                "message": message_content
            }
        else:
            new_message = "{date} {time} {sender} {message}\n".format(date=message_datetime.strftime(DATE_FORMAT),
                                                                      time=message_datetime.strftime(TIME_FORMAT),
                                                                      sender=sender.replace(' ', ''),
                                                                      message=message_content.replace('\n', ' '))
        heapq.heappush(heap, MessageTuple(timestamp=message_timestamp, tiebreak_value=tiebreaker_counter,
                                          message=new_message))
        tiebreaker_counter += 1
    except KeyError as e:
        print(e, file=sys.stderr)

sorted_messages = sorted(heap, key=lambda x: x[0])
# The messages were MessageTuples, now pull just the message string out
sorted_messages = [item.message for item in sorted_messages]

if 'json' in args.format:
    json_output = {
        "threads": [
            {
                "participants": list(message_senders),
                "messages": sorted_messages
            }
        ]
    }
    with open(args.outPath, 'w', encoding='utf-8') as out_file:
        out_file.write(json.dumps(json_output))
else:
    with open(args.outPath, 'w', encoding='utf-8') as out_file:
        out_file.writelines(sorted_messages)
