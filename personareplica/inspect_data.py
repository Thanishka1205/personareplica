import json
import sys
from pathlib import Path

with open('data/raw/medical.jsonl', 'r') as f:
    for i, line in enumerate(f):
        if i >= 1:
            break
        data = json.loads(line)
        print(f"Keys: {list(data.keys())}")
        for k in list(data.keys())[:8]:
            val = str(data[k])[:100]
            print(f"  {k}: {val}")
