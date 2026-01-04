# api/utils/event_parser.py

import base64
import json

EVENT_FIELDS = [
    "serialno",
    "version",
    "account_id",
    "instance_id",
    "srcaddr",
    "dstaddr",
    "srcport",
    "dstport",
    "protocol",
    "packets",
    "bytes",
    "starttime",
    "endtime",
    "action",
    "log_status",
]


def parse_event_line(line: str):
    parts = line.strip().split()

    if len(parts) != len(EVENT_FIELDS):
        return None

    return dict(zip(EVENT_FIELDS, parts))


def within_time_range(event, start_time, end_time) -> bool:
    event_start = int(event["starttime"])
    event_end = int(event["endtime"])

    if start_time is not None and event_start < start_time:
        return False

    if end_time is not None and event_end > end_time:
        return False

    return True



def matches_query(event, query: str) -> bool:
    if not query:
        return True

    q = query.lower()

    for field in ("account_id", "instance_id", "srcaddr", "dstaddr", "action", "log_status"):
        if q in event[field].lower():
            return True

    return False



def encode_cursor(data: dict) -> str:
    return base64.b64encode(json.dumps(data).encode()).decode()

def decode_cursor(cursor: str) -> dict:
    return json.loads(base64.b64decode(cursor).decode())
