import requests
import json

class Cloudflare:
    cloudflareApi = 'https://api.cloudflare.com/client/v4'

    def __init__(self, config):
        self.cloudflareEmail = config.config['cloudflare_email']
        self.cloudflareApiKey = config.config['cloudflare_api_key']
        self.onFail = config.onFail
        self.onSuccess = config.onSuccess

    def test(self):
        response = requests.get(self.cloudflareApi + '/user', headers = {
            'X-Auth-Email': self.cloudflareEmail,
            'X-Auth-Key': self.cloudflareApiKey,
            'Content-Type': 'application/json'
        })
        return json.loads(response.text)['result']

    def fetchIdentifier(self, zoneId, hostname):
        response = requests.get(self.cloudflareApi + '/zones/' + zoneId + '/dns_records?type=A&name=' + hostname, headers = {
            'X-Auth-Email': self.cloudflareEmail,
            'X-Auth-Key': self.cloudflareApiKey,
            'Content-Type': 'application/json'
        })

        jsonResp = json.loads(response.text)
        if response.text is None or not jsonResp['success']:
            return None
        return jsonResp['result'][0]['id']

    def updateRecord(self, zoneId, hostname, ip):
        identifier = self.fetchIdentifier(zoneId, hostname)
        if identifier is None:
            self.onFail('[Failed] Fetch Identifier :: Update Record: ' + zoneId + '->' + hostname)
            return

        response = requests.put(self.cloudflareApi + '/zones/' + zoneId + '/dns_records/' + identifier, headers = {
            'X-Auth-Email': self.cloudflareEmail,
            'X-Auth-Key': self.cloudflareApiKey,
            'Content-Type': 'application/json'
        }, data = json.dumps({
            'type': 'A',
            'name': hostname,
            'content': ip,
            'proxied': True
        }))

        if response.text is None or not json.loads(response.text)['success']:
            self.onFail('[Failed] Update Record: ' + zoneId + '->' + hostname)
            return
        self.onSuccess('Updated Record: ' + zoneId + '->' + hostname)
