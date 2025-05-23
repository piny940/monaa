import json
import csv
import re
from typing import Any
from dateutil.parser import parse

IMAGE_POLICY = {'name': 'stg-portfolio-updater', 'namespace': 'default'}

mappings = [
    ['no new tags found, next scan in 1m0s', 'N'],
    [r"^Latest image tag for 'ghcr.io/piny940/portfolio-updater' resolved to main-\S+$", 'U']
]

logs: list[dict[str, Any]] = []

with open('log/flux-system.image-reflector.csv') as f:
  reader = csv.DictReader(f)
  for row in reader:
    log: dict[str, Any] = json.loads(row['log'])
    logs.append(log)

# 昇順にする
logs.reverse()

texts = []

for log in logs:
  if log.get('ImageRepository', False) and log['ImageRepository']['name'] != IMAGE_POLICY['name']:
    continue
  msg: str = log['msg']
  time_str: str = log['ts']
  time = parse(time_str)
  for mapping in mappings:
    if re.match(mapping[0], msg):
      texts.append(f'{mapping[1]} {time.timestamp()}\n')

with open('examples/flux-system.image-reflector.log', 'w') as f:
  f.writelines(texts)
