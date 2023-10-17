#!/usr/bin/env python3
""" function that returns all students sorted by average score"""


def top_students(mongo_collection):
    """returns  A list of students with an additional "averageScore" key"""
    pipeline = [
        {
            "$addFields": {
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

    students = list(mongo_collection.aggregate(pipeline))
    return students
