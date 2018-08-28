import requests
import json
from pynamicError import PynamicError

class Cloudflare:
    cloudflareApi = 'https://api.cloudflare.com/client/v4'

    def __init__(self, config):
        self.cloudflareEmail = config.config['cloudflare_email']
        self.cloudflareApiKey = config.config['cloudflare_api_key']
        self.output = config.output

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

        jsonResp = response.json()
        if response.text is None or not jsonResp['success']:
            return None
        return jsonResp['result'][0]['id']

    def updateRecord(self, zoneId, hostname, ip):
        identifier = self.fetchIdentifier(zoneId, hostname)
        if identifier is None:
            raise PynamicError('[Failed] Fetch Identifier :: Update Record: ' + zoneId + '->' + hostname)

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
            raise PynamicError('[Failed] Update Record: ' + zoneId + '->' + hostname)

        self.output('Updated Record: ' + zoneId + '->' + hostname)
