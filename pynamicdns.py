from configuration import Configuration

def main():
    print('PynamicDNS : https://github.com/1DC/PynamicDNS')
    print('       Thanks for using PynamicDNS! :-)')

    try:
        config = Configuration('pynamic.yml')
        config.process(
            lambda cloudflare, zone, hostname, ip, onFail, onSuccess: cloudflare.updateRecord(zone['zone_id'], hostname, ip, onFail, onSuccess),
            lambda failMsg: print(failMsg),
            lambda successMsg: print(successMsg)
        )
    except (KeyboardInterrupt, SystemExit):
        print('CTRL+C detected - goodbye!')

if __name__ == '__main__':
    main()
