# Facebook Message Converter
There are a few good projects on GitHub for pulling statistics from Facebook message archives, like [conversation-analyzer](https://github.com/5agado/conversation-analyzer) and [FacebookChatStatistics](https://github.com/davidkrantz/FacebookChatStatistics), but recent changes to the format of Facebook export archives have broken compatibility. This script allows for conversion from the new JSON message archive format to formats that work with the above tools.

# Formats
This script exports in a simple text format used by [conversation-analyzer](https://github.com/5agado/conversation-analyzer), as well as the JSON format defined by [fbchat-archive-parser](https://github.com/ownaginatious/fbchat-archive-parser) (used by [FacebookChatStatistics](https://github.com/davidkrantz/FacebookChatStatistics)).

# Usage
```
$ python3 facebook-message-converter.py --help
usage: facebook-message-converter.py [-h] --in ARCHIVEPATH --out OUTPATH
                                     --format FORMAT

FB Message Archive Converter

optional arguments:
  -h, --help        show this help message and exit
  --in ARCHIVEPATH  Path to JSON archive
  --out OUTPATH     Path to output file
  --format FORMAT   txt or json, for conversation-analyzer or
                    FacebookChatStatistics respectively
```

### Example usage:
```
# Convert to a json format for FacebookChatStatistics
$ python3 facebook-message-converter.py --in message.json --out converted.json --format json
```

```
# Convert to a txt format for conversation-analyzer
$ python3 facebook-message-converter.py --in message.json --out converted.txt --format txt
```
