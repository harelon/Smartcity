ssh pi@192.168.31.199
python3 -r /MQTT/*
echo Starting client..
exit
ssh pi@192.168.31.200:
echo Starting Server
python3 -r /Server/*
echo Running completed.