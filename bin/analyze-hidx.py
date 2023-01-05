# usage: python3 bin/analyze-hidx.py this/is/a/path/hashmark_4_example.hidx

import requests
import sys

FILE_NAME = sys.argv[1]

files = {'file': (FILE_NAME, open(FILE_NAME, 'rb'))}
headers = {'user-agent': 'your user-agent value'}
response = requests.post("https://iotcube.net/api/wf1",
                         files=files,
                         headers=headers)

print(response.text)