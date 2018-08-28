import yaml
import threading
from network import Network
from cloudflare import Cloudflare
from pynamicError import PynamicError

class Configuration:
    def __init__(self, filename, output):
        configFile = open(filename, 'r')
        self.config  = yaml.load(configFile.read())
        self.output = output
        self.ip = None

    def processZone(self, zone, action):
        for hostname in zone['hostnames']:
            action(zone, hostname, self)

    def processZones(self, action):
        for zone in self.config['zones']:
            self.processZone(zone, action)

    def process(self, action):
        self.cloudflare = Cloudflare(self)

        ip = Network.fetchIp()
        if ip is None:
            raise PynamicError('Failed to obtain IP address')

        if self.ip == ip:
            return
        self.ip = ip

        emailKeyTest = self.cloudflare.test()
        if emailKeyTest is None:
            raise PynamicError('Failed to authenticate with Cloudflare.')
        self.output('Authenticated with Cloudflare: ' + emailKeyTest['id'])

        self.processZones(action)
        return True
