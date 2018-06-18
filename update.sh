cd /mnt/c/Users/harel/Desktop/SmartCityAmi
echo Updating client..
scp -r client/* pi@192.168.31.199:MQTT/
echo Updating server..
scp -r server/* pi@192.168.31.200:Server/
echo Completed.
