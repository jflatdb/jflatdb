"""
Helper functions
"""

import random, string

def generate_id(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def match_query(item, query):
    return all(item.get(k) == v for k, v in query.items())

def deep_copy(data):
    if isinstance(data, dict):
        return {k: deep_copy(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [deep_copy(i) for i in data]
    return data
