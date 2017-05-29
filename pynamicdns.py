from configuration import Configuration
from network import Network

print('PynamicDNS : https://github.com/1DC/PynamicDNS')
print('       Thanks for using PynamicDNS! :-)')

try:
    network = Network()
    config = Configuration()
    config.processConfiguration(
        config.getConfiguration(),
        network,
        lambda cloudflare, zone, hostname, ip, onFail, onSuccess: cloudflare.updateRecord(zone['zone_id'], hostname, ip, onFail, onSuccess),
        lambda failMsg: print(failMsg),
        lambda successMsg: print(successMsg)
    )
except (KeyboardInterrupt, SystemExit):
    print('CTRL+C detected - goodbye!')
