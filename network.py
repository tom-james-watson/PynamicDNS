import requests

class Network:
    def fetchIp():
        return requests.get('https://api.ipify.org/').text
