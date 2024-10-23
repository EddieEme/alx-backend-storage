#!/usr/bin/env python3
"""
Python script that provides stats about Nginx logs stored in MongoDB
"""
from pymongo import MongoClient


def log_stats():
    """
    Provides stats about Nginx logs stored in MongoDB
    """
    # Connect to MongoDB
    client = MongoClient('mongodb://127.0.0.1:27017')
    
    # Get the logs database
    logs_collection = client.logs.nginx
    
    # Get total number of documents
    total_logs = logs_collection.count_documents({})
    
    # Get counts for each HTTP method
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = {method: logs_collection.count_documents({"method": method}) 
                    for method in methods}
    
    # Get count of status check
    status_check = logs_collection.count_documents(
        {"method": "GET", "path": "/status"}
    )
    
    # Print results in specified format
    print(f"{total_logs} logs")
    print("Methods:")
    for method in methods:
        print(f"\tmethod {method}: {method_counts[method]}")
    print(f"{status_check} status check")


if __name__ == "__main__":
    log_stats()
