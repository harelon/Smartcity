start c:\Windows\System32\bash.exe -c "ssh pi@10.0.0.199 python3 client/motion_detector.py sonoff 4"
start c:\Windows\System32\bash.exe -c "ssh pi@10.0.0.199 python3 client/light_detector.py" 

start c:\Windows\System32\bash.exe -c "ssh pi@10.0.0.105 python3 server/logic.py"
start c:\Windows\System32\bash.exe -c "ssh pi@10.0.0.105 python3 server/light_bulb.py sonoff"
