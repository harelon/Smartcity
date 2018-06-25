cd /mnt/c/Users/harel/Desktop/Smartcity
echo Updating client..
scp -r client/* pi@192.168.31.199:client/
echo Updating server..
scp -r server/* pi@192.168.31.105:server/
echo Completed.