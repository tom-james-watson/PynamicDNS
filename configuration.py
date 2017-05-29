import yaml
import threading
import time
from network import Network
from cloudflare import Cloudflare

class Configuration:
    def __init__(self, filename):
        configFile = open(filename, 'r')
        self.config  = yaml.load(configFile.read())

    def processZone(self, cloudflare, zone, ip, action, onFail, onSuccess):
        for hostname in zone['hostnames']:
            action(cloudflare, zone, hostname, ip, onFail, onSuccess)

    def processZones(self, cloudflare, ip, action, onFail, onSuccess):
        for zone in self.config['zones']:
            self.processZone(cloudflare, zone, ip, action, onFail, onSuccess)

    def process(self, action, onFail, onSuccess):
        cloudflare = Cloudflare(self.config['cloudflare_email'], self.config['cloudflare_api_key'])

        ip = Network.fetchIp()
        if (ip is None):
            onFail('Failed to obtain IP address')
            return

        emailKeyTest = cloudflare.test()
        if emailKeyTest is None:
            onFail('Failed to authenticate with Cloudflare.')
            return
        onSuccess('Authenticated with Cloudflare: ' + emailKeyTest['id'])

        timer = threading.Timer(self.config['update_delay_seconds'], lambda: self.processZones(cloudflare, ip, action, onFail, onSuccess))
        timer.daemon = True
        timer.start()
        self.processZones(cloudflare, ip, action, onFail, onSuccess)

        while True:
            time.sleep(1)
