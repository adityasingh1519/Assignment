# api/services/search_service.py

import os
from concurrent.futures import ThreadPoolExecutor
PAGE_SIZE = 50  

from api.utils.event_parser import (
    parse_event_line,
    within_time_range,
    matches_query,
    encode_cursor,
    decode_cursor,
)


def search_file(file_path, query, start_time, end_time):
    matches = []
    

    file_name = os.path.basename(file_path)

    with open(file_path, "r") as f:
        for line in f:
            event = parse_event_line(line)
            if len(matches) >= MAX_RESULTS:
                break
            if not event:
                continue

            if not within_time_range(event, start_time, end_time):
                continue

            if not matches_query(event, query):
                continue

            matches.append({
                "srcaddr": event["srcaddr"],
                "dstaddr": event["dstaddr"],
                "action": event["action"],
                "log_status": event["log_status"],
                "file": file_name,
            })

    return matches


def search_dataset(
    dataset_dir,
    query,
    start_time,
    end_time,
    cursor=None,
    limit=PAGE_SIZE,
):
    results = []
    has_more = False

    log_files = sorted(
        os.path.join(dataset_dir, f)
        for f in os.listdir(dataset_dir)
        if os.path.isfile(os.path.join(dataset_dir, f))
    )

    if not log_files:
        return results, None, False

    file_idx = 0
    line_offset = 0

    if cursor:
        c = decode_cursor(cursor)
        file_idx = c["file_idx"]
        line_offset = c["line_offset"]

    for i in range(file_idx, len(log_files)):
        file_path = log_files[i]

        with open(file_path, "r") as f:
            for line_no, line in enumerate(f):
                if i == file_idx and line_no < line_offset:
                    continue

                event = parse_event_line(line)
                if not event:
                    continue

                if not within_time_range(event, start_time, end_time):
                    continue

                if not matches_query(event, query):
                    continue

                event["file"] = os.path.basename(file_path)
                results.append(event)

                if len(results) >= limit:
                    next_cursor = encode_cursor({
                        "file_idx": i,
                        "line_offset": line_no + 1,
                    })
                    has_more = True
                    return results, next_cursor, has_more

    return results, None, False
