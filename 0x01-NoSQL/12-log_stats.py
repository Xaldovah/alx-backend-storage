#!/usr/bin/env python3
"""script that provides some stats about Nginx logs stored in MongoDB"""

from pymongo import MongoClient


def log_stats(mongo_collection):
    """
    Display stats about Nginx logs stored in MongoDB.

    Args:
        mongo_collection: pymongo collection object.

    Returns:
        None
    """
    total_logs = mongo_collection.count_documents({})

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = {method: mongo_collection.count_documents(
        {"method": method}) for method in methods}

    status_check_count = mongo_collection.count_documents(
            {"method": "GET", "path": "/status"})

    print(f"{total_logs} logs")

    print("Methods:")
    for method, count in method_counts.items():
        print(f"\tmethod {method}: {count}")

    print(f"{status_check_count} status check")
