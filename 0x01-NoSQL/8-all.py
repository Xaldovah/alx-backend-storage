#!/usr/bin/env python3
"""Python function that lists all documents in a collection"""

import pprint


def list_all(mongo_collection):
    """
    List all documents in a MongoDB collection.

    Args:
        mongo_collection: pymongo collection object.

    Returns:
        List of documents in the collection.
    """
    documents = list(mongo_collection.find({}))
    return documents
