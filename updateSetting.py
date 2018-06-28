import subprocess

updateScript=open("update.sh","w")
Ips=open("ips.txt","r")
lines = Ips.readlines()
ServerIp=lines[0].rstrip()
ClientIp=lines[1].rstrip()
updateScript.write(
"""cd /mnt/c/Users/harel/Desktop/Smartcity
echo Updating client..
scp -r client/* pi@"""+ClientIp+""":client/
echo Updating server..
scp -r server/* pi@"""+ServerIp+""":server/
echo Completed."""
)
updateScript.close()

runScript=open("Run.cmd","w")
runScript.write(
"""start c:\Windows\System32\\bash.exe -c "ssh pi@"""+ClientIp+ """ python3 client/motion_detector.py 1 4"
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

updateIps=open("ipUpdates.sh","w")
updateIps.write(
"""cd /mnt/c/Users/harel/Desktop/Smartcity
scp ips.txt pi@"""+ServerIp+""":server/
scp ips.txt pi@"""+ClientIp+""":client/
""")
updateIps.close()

process = subprocess.Popen('ipUpdates.sh', stdout=subprocess.PIPE , stderr=subprocess.PIPE, shell=True)
process.wait()
