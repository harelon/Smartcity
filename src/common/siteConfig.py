import os
import json

class SiteConfig:

    def __init__(self):        
        siteJson =os.path.join(os.path.dirname(__file__),"site.json")
        with open(siteJson) as f:
            data = json.load(f)
        self.ServerIp = data["IPs"]["ServerIp"]
        self.ClientIp = data["IPs"]["ClientIp"]