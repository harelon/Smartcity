start c:\Windows\System32\bash.exe -c "ssh pi@192.168.31.199 python3 client/motion_detector.py 1 4"
start c:\Windows\System32\bash.exe -c "ssh pi@192.168.31.199 python3 client/light_detector.py" 

start c:\Windows\System32\bash.exe -c "ssh pi@192.168.31.105 python3 server/logic.py"
start c:\Windows\System32\bash.exe -c "ssh pi@192.168.31.105 python3 server/light_bulb.py sonoff"
