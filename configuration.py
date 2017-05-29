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
        self.ip = None

    def processZone(self, zone, action):
        for hostname in zone['hostnames']:
            action(zone, hostname, self)

    def processZones(self, cloudflare, ip, action):
        for zone in self.config['zones']:
            self.processZone(zone, action)

    def process(self, action):
        self.cloudflare = Cloudflare(self)

        ip = Network.fetchIp()
        if ip is None:
            self.onFail('Failed to obtain IP address')
            return

        if self.ip == ip:
            return
        self.ip = ip

        emailKeyTest = self.cloudflare.test()
        if emailKeyTest is None:
            self.onFail('Failed to authenticate with Cloudflare.')
            return
        self.onSuccess('Authenticated with Cloudflare: ' + emailKeyTest['id'])

        timer = threading.Timer(self.config['update_delay_seconds'], lambda: self.processZones(self.cloudflare, ip, action))
        timer.daemon = True
        timer.start()
        self.processZones(self.cloudflare, ip, action)

        while True:
            time.sleep(1)
