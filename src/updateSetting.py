import subprocess
import argparse
import json

parser = argparse.ArgumentParser(description='Start updating ips')
parser.add_argument('site', help='The location you are in')

args = parser.parse_args()

siteJson ="../config/" + args.site + ".json"

with open(siteJson) as f:
    data = json.load(f)

ServerIp=data["IPs"]["ServerIp"]
ClientIp=data["IPs"]["ClientIp"]

updateScript=open("update.sh","w")

updateScript.write(
"""echo Updating client..
scp -r ../src/client/* pi@"""+ClientIp+""":client/
scp -r ../src/common/* pi@"""+ClientIp+""":client/
echo Updating server..
scp -r ../src/server/* pi@"""+ServerIp+""":server/
scp -r ../src/common/* pi@"""+ServerIp+""":server/
echo Completed."""
)
updateScript.close()

runScript=open("Run.cmd","w")
runScript.write(
"""start c:\Windows\System32\\bash.exe -c "ssh pi@"""+ClientIp+ """ python3 client/motion_detector.py sonoff 4"
start c:\Windows\System32\\bash.exe -c "ssh pi@"""+ClientIp+ """ python3 client/light_detector.py" 

start c:\Windows\System32\\bash.exe -c "ssh pi@"""+ServerIp+""" python3 server/logic.py"
start c:\Windows\System32\\bash.exe -c "ssh pi@"""+ServerIp+""" python3 server/light_bulb.py sonoff"
"""
)
runScript.close()

killScript=open("killCommand.cmd","w")
killScript.write(
"""start c:\Windows\System32\\bash.exe -c "ssh pi@"""+ClientIp+""" sh client/clientKill.sh"                                   
start c:\Windows\System32\\bash.exe -c "ssh pi@"""+ServerIp+""" sh server/serverKill.sh"
"""
) 
killScript.close()

process = subprocess.call(["scp",siteJson,"pi@"+ServerIp+":server/site.json"])
process = subprocess.call(["scp",siteJson,"pi@"+ClientIp+":client/site.json"])