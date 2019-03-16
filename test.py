import subprocess
import sys
import os
import hashlib
import time
import signal

#os.system('rm -f tmp.txt')

#Setup I/O (Green = 45, Red = 60)
#Door = 44

os.system('echo 44 > /sys/class/gpio/export')
os.system('echo out > /sys/class/gpio/gpio44/direction')
os.system('echo 0 > /sys/class/gpio/gpio44/value')

os.system('echo 45 > /sys/class/gpio/export')
os.system('echo out > /sys/class/gpio/gpio45/direction')
os.system('echo 0 > /sys/class/gpio/gpio45/value')

os.system('echo 60 > /sys/class/gpio/export')
os.system('echo out > /sys/class/gpio/gpio60/direction')
os.system('echo 1 > /sys/class/gpio/gpio60/value')



#if there's a valid file here, delete it
os.system('rm -f valid.txt')
#in a while loop, compare current tmp.txt QR hash with the approved hash from the web


while (1):
	os.system('wget --quiet https://raw.githubusercontent.com/edwardzxy/qrtest/master/valid.txt')
    
	approved = subprocess.check_output(["tail", "-n", "1", "valid.txt"])
	print "Approved Hash from Web: %s" % approved
	os.system('rm valid.txt')
    #
    os.system("raspistill -w 320 -h 240 -o image.jpg -t 2")
    zbarcam=subprocess.Popen("zbarimg --raw image.jpg", stdout=subprocess.PIPE, shell=True,preexec_fn=os.setsid)
    qrcodetext=zbarcam.stdout.readline()
    os.system('rm image.jpg')
    #
	if approved in qrcodetext:
        print "QR Code Accepted"
        os.system('echo 1 > /sys/class/gpio/gpio45/value')
        os.system('echo 1 > /sys/class/gpio/gpio44/value')
        os.system('echo 0 > /sys/class/gpio/gpio60/value')
        time.sleep(10)
        os.system('echo 0 > /sys/class/gpio/gpio45/value')
        os.system('echo 0 > /sys/class/gpio/gpio44/value')
        os.system('echo 1 > /sys/class/gpio/gpio60/value')
	else:
        print "No Valid Code Presented"
        mode=0
        os.system('echo 1 > /sys/class/gpio/gpio60/value')
        os.system('echo 0 > /sys/class/gpio/gpio44/value')
        os.system('echo 0 > /sys/class/gpio/gpio45/value')
