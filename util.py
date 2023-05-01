import requests

def post_event(url, event):
    print(requests.post(url, json=event))

    return "Nice!"