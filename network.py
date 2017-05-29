import requests

class Network:
    def fetchIp(self):
        return requests.get('https://api.ipify.org/').text
