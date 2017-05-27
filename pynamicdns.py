import requests
import yaml
import json
import threading
import time

print('PynamicDNS : https://github.com/1DC/PynamicDNS')
print('       Thanks for using PynamicDNS! :-)')

cloudflareApi = 'https://api.cloudflare.com/client/v4'

def getConfiguration():
    config = open('pynamic.yml', 'r')
    yml = yaml.load(config.read())
    return yml

def fetchIp():
    return requests.get('https://api.ipify.org/').text

def testCloudflare(cloudflareEmail, cloudflareApiKey):
    response = requests.get(cloudflareApi + '/user', headers = {
        'X-Auth-Email': cloudflareEmail,
        'X-Auth-Key': cloudflareApiKey,
        'Content-Type': 'application/json'
    })
    return json.loads(response.text)['result']

def fetchIdentifier(cloudflareEmail, cloudflareApiKey, zoneId, hostname):
    response = requests.get(cloudflareApi + '/zones/' + zoneId + '/dns_records?type=A&name=' + hostname, headers = {
        'X-Auth-Email': cloudflareEmail,
        'X-Auth-Key': cloudflareApiKey,
        'Content-Type': 'application/json'
    })

    jsonResp = json.loads(response.text)
    if response.text is None or not jsonResp['success']:
        return None
    return jsonResp['result'][0]['id']

def updateRecord(cloudflareEmail, cloudflareApiKey, zoneId, hostname, ip):
    identifier = fetchIdentifier(cloudflareEmail, cloudflareApiKey, zoneId, hostname)
    if identifier is None:
        print('[Failed] Fetch Identifier :: Update Record: ' + zoneId + '->' + hostname)
        return

    response = requests.get(cloudflareApi + '/zones/' + zoneId + '/dns_records/' + identifier, headers = {
        'X-Auth-Email': cloudflareEmail,
        'X-Auth-Key': cloudflareApiKey,
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

def processZone(cloudflareEmail, cloudflareApiKey, zone, ip):
    for hostname in zone['hostnames']:
        updateRecord(cloudflareEmail, cloudflareApiKey, zone['zone_id'], hostname, ip)

def processZones(cloudflareEmail, cloudflareApiKey, zonesConfiguration):
    ip = fetchIp()
    if ip is None:
        print('Failed to fetch IP.')
        return

    for zone in zonesConfiguration:
        processZone(cloudflareEmail, cloudflareApiKey, zone, ip)

def processConfiguration(configuration):
    cloudflareEmail = configuration['cloudflare_email']
    cloudflareApiKey = configuration['cloudflare_api_key']
    emailKeyTest = testCloudflare(cloudflareEmail, cloudflareApiKey)
    if emailKeyTest is None:
        print('Failed to authenticate with Cloudflare.')
        return
    print('Authenticated with Cloudflare: ' + emailKeyTest['id'])

    timer = threading.Timer(configuration['update_delay_seconds'], lambda: processZones(cloudflareEmail, cloudflareApiKey, configuration['zones']))
    timer.daemon = True
    timer.start()
    processZones(cloudflareEmail, cloudflareApiKey, configuration['zones'])

    while True:
        time.sleep(1)

try:
    processConfiguration(getConfiguration())
except (KeyboardInterrupt, SystemExit):
    print('CTRL+C detected - goodbye!')
