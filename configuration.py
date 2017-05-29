import yaml
import threading
import time
from network import Network
from cloudflare import Cloudflare

class Configuration:
    def __init__(self, filename, onFail, onSuccess):
        configFile = open(filename, 'r')
        self.config  = yaml.load(configFile.read())
        self.onFail = onFail
        self.onSuccess = onSuccess

    def processZone(self, cloudflare, zone, ip, action):
        for hostname in zone['hostnames']:
            action(cloudflare, zone, hostname, ip, self.onFail, self.onSuccess)

    def processZones(self, cloudflare, ip, action):
        for zone in self.config['zones']:
            self.processZone(cloudflare, zone, ip, action)

    def process(self, action):
        cloudflare = Cloudflare(self.config['cloudflare_email'], self.config['cloudflare_api_key'], self.onFail, self.onSuccess)

        ip = Network.fetchIp()
        if (ip is None):
            self.onFail('Failed to obtain IP address')
            return

        emailKeyTest = cloudflare.test()
        if emailKeyTest is None:
            self.onFail('Failed to authenticate with Cloudflare.')
            return
        self.onSuccess('Authenticated with Cloudflare: ' + emailKeyTest['id'])

        timer = threading.Timer(self.config['update_delay_seconds'], lambda: self.processZones(cloudflare, ip, action))
        timer.daemon = True
        timer.start()
        self.processZones(cloudflare, ip, action)

        while True:
            time.sleep(1)
