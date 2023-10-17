#!/usr/bin/env python3
"""script that provides some stats about Nginx logs stored in MongoDB"""
from pymongo import MongoClient


def get_log_stats():
    # Connect to the MongoDB server and select the "logs" database
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs_db = client.logs

    # Access the "nginx" collection
    nginx_collection = logs_db.nginx

    # Count the total number of logs
    total_logs = nginx_collection.count_documents({})

    # Count the number of logs for each method
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = {}
    for method in methods:
        method_counts[method] = nginx_collection.count_documents({"method": method})

    # Count the number of logs with method=GET and path=/status
    status_check = nginx_collection.count_documents({"method": "GET", "path": "/status"})

    # Return the results as a dictionary
    results = {
        "total_logs": total_logs,
        "method_counts": method_counts,
        "status_check": status_check
    }
    return results

