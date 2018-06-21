start c:\Windows\System32\bash.exe -c "ssh pi@192.168.31.199 python3 motion_detector.py md1 4"
start c:\Windows\System32\bash.exe -c "ssh pi@192.168.31.199 python3 light_detector.py" 

start c:\Windows\System32\bash.exe -c "ssh pi@192.168.31.105 python3 logic.py" 
start c:\Windows\System32\bash.exe -c "ssh pi@192.168.31.105 python3 light_bulb.py sonoff" 
