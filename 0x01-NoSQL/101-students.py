#!/usr/bin/env python3
"""Python function that returns all students sorted by average score"""


def top_students(mongo_collection):
    """
    Returns all students sorted by average score.

    Args:
        mongo_collection: pymongo collection object.

    Returns:
        List of students with average score.
    """
    pipeline = [
        {
            "$project": {
                "name": 1,
                "topics": 1,
                "averageScore": {
                    "$avg": "$topics.score"
                }
            }
        },
        {
            "$sort": {
                "averageScore": -1
            }
        }
    ]

    top_students = list(mongo_collection.aggregate(pipeline))
    return top_students
