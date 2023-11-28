import requests

def download_file(url):
    try:
        response =  requests.get(url, timeout=10)
    except Exception as e:
        raise e
    if response.status_code == 200:
        return response.text
    else:
        raise Exception(f"Bad status code: {response.status_code}")
    