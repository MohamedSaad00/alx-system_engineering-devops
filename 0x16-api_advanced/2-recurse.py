#!/usr/bin/python3
"""Recursive function that queries the Reddit API and returns
a list containing the titles of all hot articles for a given subreddit."""

import requests

def recurse(subreddit, hot_list=None, after=None, count=0):
    """Returns a list of titles of all hot posts on a given subreddit."""
    if hot_list is None:
        hot_list = []  # Initialize inside function to prevent mutable default issues
    
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    params = {
        "after": after,
        "count": count,
        "limit": 100
    }

    response = requests.get(url, headers=headers, params=params, allow_redirects=False)

    # Check if subreddit is invalid
    if response.status_code != 200:
        return None

    try:
        results = response.json().get("data", {})
        after = results.get("after")
        count += results.get("dist", 0)

        for child in results.get("children", []):
            hot_list.append(child["data"]["title"])

        if after is not None:
            return recurse(subreddit, hot_list, after, count)
    except ValueError:
        return None  # Handles cases where response is not JSON

    return hot_list
