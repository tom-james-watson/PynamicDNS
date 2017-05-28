import requests
import yaml
import json
import threading
import time

print('PynamicDNS : https://github.com/1DC/PynamicDNS')
print('       Thanks for using PynamicDNS! :-)')

class Configuration:
    def getConfiguration(self):
        configFile = open('pynamic.yml', 'r')
        yml = yaml.load(configFile.read())
        return yml

class Cloudflare:
    cloudflareApi = 'https://api.cloudflare.com/client/v4'

    def __init__(self, cloudflareEmail, cloudflareApiKey):
        self.cloudflareEmail = cloudflareEmail
        self.cloudflareApiKey = cloudflareApiKey

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
            print('[Failed] Fetch Identifier :: Update Record: ' + zoneId + '->' + hostname)
            return

        response = requests.get(self.cloudflareApi + '/zones/' + zoneId + '/dns_records/' + identifier, headers = {
            'X-Auth-Email': self.cloudflareEmail,
            'X-Auth-Key': self.cloudflareApiKey,
            'Content-Type': 'application/json'
        }, data = {
            'type': 'A',
            'name': hostname,
            'content': ip,
            'proxied': 'true'
        })

        if response.text is None or not json.loads(response.text)['success']:
            print('[Failed] Update Record: ' + zoneId + '->' + hostname)
            return
        print('Updated Record: ' + zoneId + '->' + hostname)

def fetchIp():
    return requests.get('https://api.ipify.org/').text

def processZone(cloudflare, zone, ip):
    for hostname in zone['hostnames']:
        cloudflare.updateRecord(zone['zone_id'], hostname, ip)

def processZones(cloudflare, zonesConfiguration):
    ip = fetchIp()
    if ip is None:
        print('Failed to fetch IP.')
        return

    for zone in zonesConfiguration:
        processZone(cloudflare, zone, ip)

def processConfiguration(configuration):
    cloudflare = Cloudflare(configuration['cloudflare_email'], configuration['cloudflare_api_key'])

    emailKeyTest = cloudflare.test()
    if emailKeyTest is None:
        print('Failed to authenticate with Cloudflare.')
        return
    print('Authenticated with Cloudflare: ' + emailKeyTest['id'])

    timer = threading.Timer(configuration['update_delay_seconds'], lambda: processZones(cloudflare, configuration['zones']))
    timer.daemon = True
    timer.start()
    processZones(cloudflare, configuration['zones'])

    while True:
        time.sleep(1)

try:
    config = Configuration()
    processConfiguration(config.getConfiguration())
except (KeyboardInterrupt, SystemExit):
    print('CTRL+C detected - goodbye!')
