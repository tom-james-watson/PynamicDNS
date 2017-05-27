# PynamicDNS
Cloudflare Dynamic DNS - Built in Python

## Usage
Using this is relatively simple, I think. The configuration is [YAML](http://yaml.org/).

You'll need Python (I used Python 3.6 to make this, so that's a good start), and pip. Run this command:

```
pip install -r requirements.txt
```

Then all that's left is to simply plop your Cloudflare email, API key, zone IDs and hostnames into their place within the config and fire up pynamicdns.py. That's it. Nothing else to do.

Make sure you rename pynamic.example.yml to pynamic.yml, by the way. :-)
