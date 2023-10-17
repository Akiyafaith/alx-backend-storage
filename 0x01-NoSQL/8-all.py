#!/usr/bin/env python3
"""List all documents"""


def list_all(mongo_collection):
    """ List all documents in a MongoDB collection"""
    documents = list(mongo_collection.find())
    return documents
