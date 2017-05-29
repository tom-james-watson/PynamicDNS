from configuration import Configuration

def main():
    print('PynamicDNS : https://github.com/1DC/PynamicDNS')
    print('       Thanks for using PynamicDNS! :-)')

    try:
        config = Configuration('pynamic.yml', lambda failMsg: print(failMsg), lambda successMsg: print(successMsg))
        config.process(lambda zone, hostname, config: config.cloudflare.updateRecord(zone['zone_id'], hostname, config.ip))
    except (KeyboardInterrupt, SystemExit):
        print('CTRL+C detected - goodbye!')

if __name__ == '__main__':
    main()
