import requests

def download_file(url):
    try:
        response =  requests.get(url, timeout=5)
    except Exception as e:
        raise e
    if response.status_code == 200:
        return response.text
    else:
        raise Exception("Invalid Streamlit app URL")
    