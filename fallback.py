import requests

def is_server_alive(endpoint):
    if not endpoint:
        return False
    try:
        r = requests.get(endpoint + "/minio/health/live", timeout=2)
        return r.status_code == 200
    except:
        return False