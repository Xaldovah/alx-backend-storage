#!/usr/bin/env python3
"""function that returns the list of school having a specific topic"""


def schools_by_topic(mongo_collection, topic):
    """
    Return a list of schools having a specific topic.

    Args:
        mongo_collection: pymongo collection object.
        topic (string): The topic to search.

    Returns:
        List of schools matching the specified topic.
    """
    schools = list(mongo_collection.find({"topics": topic}))
    return schools
