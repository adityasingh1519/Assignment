# api/utils/event_parser.py

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


def within_time_range(event, start_time: int, end_time: int) -> bool:
    return (
        int(event["starttime"]) >= start_time
        and int(event["endtime"]) <= end_time
    )


def matches_query(event, query: str) -> bool:
    if not query:
        return True

    q = query.lower()

    for field in ("account_id", "srcaddr", "dstaddr", "action"):
        if q in event[field].lower():
            return True

    return False
