# api/services/search_service.py

import os
from concurrent.futures import ThreadPoolExecutor
MAX_RESULTS = 100  

from api.utils.event_parser import (
    parse_event_line,
    within_time_range,
    matches_query,
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


def search_dataset(dataset_dir, query, start_time, end_time):
    results = []

    log_files = [
        os.path.join(dataset_dir, f)
        for f in os.listdir(dataset_dir)
        if os.path.isfile(os.path.join(dataset_dir, f))
    ]

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
        file_results = future.result()

        for event in file_results:
            results.append(event)

            if len(results) >= MAX_RESULTS:
                    return results

    return results
