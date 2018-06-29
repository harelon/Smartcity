echo Updating client..
scp -r ../src/client/* pi@10.0.0.199:client/
scp -r ../src/common/* pi@10.0.0.199:client/
echo Updating server..
scp -r ../src/server/* pi@10.0.0.105:server/
scp -r ../src/common/* pi@10.0.0.105:server/
echo Completed.