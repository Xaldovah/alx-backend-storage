#!/usr/bin/env python3
"""function that inserts a new document in a collection based on kwargs"""


def insert_school(mongo_collection, **kwargs):
    """
    Insert a new document into a MongoDB collection based on keyword arguments.

    Args:
        mongo_collection: pymongo collection object.
        **kwargs: Keyword arguments representing the document attributes.

    Returns:
        The new _id of the inserted document.
    """
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
