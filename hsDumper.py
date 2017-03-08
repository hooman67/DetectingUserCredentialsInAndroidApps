import time, subprocess, socket, re

afttFile=open("AminPackageNames.txt", "r")

fileName=""
currentPackageName=""

window_dump=None
current_window=None

hsTe1 = '\nDONE.\n'
hsTe2 = 'DONE.\n'
hsTe3 = '\nDONE.\nDONE\n'
hsTe4 = 'DONE.\nDONE\n'
hsTe1 = hsTe1.encode(encoding='utf_8')
hsTe2 = hsTe2.encode(encoding='utf_8')
hsTe3 = hsTe3.encode(encoding='utf_8')
hsTe4 = hsTe4.encode(encoding='utf_8')


#command_start="adb shell am start -n "+currentPackageName

#command_dump="adb shell dumpsys window windows"
command_dump="adb shell dumpsys input_method"
port = 5939


###################################FUNCTIONS###########################################
#Function for executing adb shell command
def adb(command, input=None):
    if not isinstance(command,list): command=command.split()
    return subprocess.Popen(command, stdout=subprocess.PIPE, 
                        stderr=subprocess.STDOUT).communicate(input=input)[0]


#Function for getting current window hash id
def getWindowHash():

    window_dump=subprocess.Popen('adb shell dumpsys window windows', shell=False, stdout=subprocess.PIPE)
    window_dump=window_dump.stdout.read()

    regexp=re.compile('Window #\d+[:\s\r\n]+Window\{(?P<hash>[a-f\d]{8}) (?P<title>.*) paused=.*\}:?[\r\n]+(?P<attributes>(?:    .*[\r\n]+)+)', re.MULTILINE)

    # fetch current window
    m=re.search('mCurrentFocus=Window\{(?P<hash>\S+) (?P<title>\S*) \S+', str(window_dump))
    
    if m:
        current_window=m.groupdict()
        return [current_window][0]['hash']



############Read Packag Name & start the app###########
for line in afttFile:

    currentPackageName=line.strip("\n")
    command_start="adb shell monkey -p " + currentPackageName + " 1"
    print ("Current Package Name: "+currentPackageName)
    #print("Command to send:  "+ command_start)

    result=subprocess.Popen(command_start, shell=False, stdout=subprocess.PIPE)
    result=result.stdout.read()
    time.sleep(10)



###################communication start#############################################
    f=open("hsAFTT_"+currentPackageName+".txt", "w")

    dumResults=subprocess.Popen(command_dump, shell=False, stdout=subprocess.PIPE)
    dumResults=dumResults.stdout.read()
    time.sleep(3)
    hints = re.findall('hintText=\S*',str(dumResults))
    if hints != 0:
        f.write(hints[0] + "\n\n")
        print(hints[0] + "\n")


    print("communication start:")
    try:              
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        subprocess.Popen('adb shell service call window 2', shell=False, stdout=subprocess.PIPE)
        time.sleep(.5)
        subprocess.Popen('adb shell service call window 1 i32 4939', shell=False, stdout=subprocess.PIPE)
        time.sleep(.5)

        adb('adb forward tcp:%d tcp:4939' % port)
        s.connect(('127.0.0.1', port))
        print ("Port Used for Communication: %s" %port)


        hashId=getWindowHash()
        hsTe = 'DUMP %s\n'%hashId;  
        s.sendall(hsTe.encode(encoding='utf_8'))
        print ("dump Command sent")
    
        s.settimeout(360)
        data=''
        t0 = time.time()            
    
        print ("inside reading loop")
        while True:
            datum=s.recv(32*1024)
            #print ("Packet: "+str(datum))
            f.write(str(datum))


            if (datum.endswith(hsTe1) or datum.endswith(hsTe2) or datum.endswith(hsTe3) or datum.endswith(hsTe4)):
                print ("End of Packet ransfer")
                break 
            if datum == '':
                print ("Socket closed")
                raise socket.error('Socket closed')
            if time.time() - t0 > 360:
                print ("Timeout")
                raise socket.error('Timeout')  

                
            data+=str(datum)

    except socket.error:
        print ("connection failed checking for another port")
        subprocess.Popen(command+'service call window 2', shell=False, stdout=subprocess.PIPE)
        time.sleep(.5)
        subprocess.Popen(command+'service call window 1 i32 4939', shell=False, stdout=subprocess.PIPE)
        time.sleep(.5)
        s.close()

f.close()