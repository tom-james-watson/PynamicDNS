import yaml
import threading
import time
from cloudflare import Cloudflare

class Configuration:
    def getConfiguration(self):
        configFile = open('pynamic.yml', 'r')
        yml = yaml.load(configFile.read())
        return yml

    def processZone(self, cloudflare, zone, ip, action, onFail, onSuccess):
        for hostname in zone['hostnames']:
            action(cloudflare, zone, hostname, ip, onFail, onSuccess)

    def processZones(self, cloudflare, zonesConfiguration, ip, action, onFail, onSuccess):
        for zone in zonesConfiguration:
            self.processZone(cloudflare, zone, ip, action, onFail, onSuccess)

    def processConfiguration(self, configuration, network, action, onFail, onSuccess):
        cloudflare = Cloudflare(configuration['cloudflare_email'], configuration['cloudflare_api_key'])

        ip = network.fetchIp()
        if (ip is None):
            onFail('Failed to obtain IP address')
            return

        emailKeyTest = cloudflare.test()
        if emailKeyTest is None:
            onFail('Failed to authenticate with Cloudflare.')
            return
        onSuccess('Authenticated with Cloudflare: ' + emailKeyTest['id'])

        timer = threading.Timer(configuration['update_delay_seconds'], lambda: self.processZones(cloudflare, configuration['zones'], ip, action, onFail, onSuccess))
        timer.daemon = True
        timer.start()
        self.processZones(cloudflare, configuration['zones'], ip, action, onFail, onSuccess)

        while True:
            time.sleep(1)
