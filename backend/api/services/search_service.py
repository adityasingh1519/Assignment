# api/services/search_service.py

import os
from concurrent.futures import ThreadPoolExecutor

from api.utils.event_parser import (
    parse_event_line,
    within_time_range,
    matches_query,
)


def search_file(file_path, query, start_time, end_time):
    matches = []

    file_name = os.path.basename(file_path)
    
    print(f"Searching in file: {file_name}")

    with open(file_path, "r") as f:
        for line in f:
            event = parse_event_line(line)
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


def search_dataset(dataset_dir, query, start_time, end_time):
    results = []

    log_files = [
        os.path.join(dataset_dir, f)
        for f in os.listdir(dataset_dir)
        if os.path.isfile(os.path.join(dataset_dir, f))
    ]
    print(f"Searching dataset directory: {dataset_dir}")
    print(f"Found {len(log_files)} log files in dataset.")

    if not log_files:
        return results

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [
            executor.submit(
                search_file,
                file_path,
                query,
                start_time,
                end_time,
            )
            for file_path in log_files
        ]

        for future in futures:
            results.extend(future.result())

    return results
