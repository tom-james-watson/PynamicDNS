# PynamicDNS
[Cloudflare](https://cloudflare.com/) [Dynamic DNS](https://en.wikipedia.org/wiki/Dynamic_DNS) - Built in [Python](https://python.org/)

Goals:
- Make it work and serve its purpose (to update DNS on Cloudflare dynamically)
- Teach me some Python ready for university
- Be linked to by [this blog post](https://blog.preprocess.uk/home-hosted-websites/)

## Usage
Using this is relatively simple, I think. The configuration is [YAML](http://yaml.org/).

You'll need Python (I used Python 3.6 to make this, so that's a good start), and pip. Run this command:

```
pip install -r requirements.txt
```

Then all that's left is to simply plop your Cloudflare email, API key, zone IDs and hostnames into their place within the config and fire up pynamicdns.py. That's it. Nothing else to do.

Make sure you rename pynamic.example.yml to pynamic.yml, by the way. :-)
