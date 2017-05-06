import time, subprocess, socket, re

afttFile=open("ApplicationPackage.DOC", "r")

fileName=""
packageName=""
activityName=""
packageFile=None

window_dump=None
current_window=None
windows=None
kos=4


#Function for executing adb shell command
def adb(command, input=None):
    if not isinstance(command,list): command=command.split()
    return subprocess.Popen(command, stdout=subprocess.PIPE, 
                        stderr=subprocess.STDOUT).communicate(input=input)[0]


#Function for getting current window hash id
def getWindowHash():
    command='adb shell ' 

    window_dump=subprocess.Popen(command+'dumpsys window windows', shell=False, stdout=subprocess.PIPE)
    window_dump=window_dump.stdout.read()

    regexp=re.compile(b'Window #\d+[:\s\r\n]+Window\{(?P<hash>[a-f\d]{8}) (?P<title>.*) paused=.*\}:?[\r\n]+(?P<attributes>(?:    .*[\r\n]+)+)', re.MULTILINE)

    windows=[ m.groupdict() for m in regexp.finditer(window_dump) ]

    # fetch current window
    m=re.search(b'mCurrentFocus=Window\{(?P<hash>\S+) (?P<title>\S*) \S+', window_dump)
    
    if m:
        current_window=m.groupdict()
        #print (str(current_window))
    else:
        current_window=None

    for window in windows:
 #       if window['hash']==current_window['hash']:
         return [window][0]['hash']


#Read Packag Name & Corresponding Activity Name from Provided file

for line in afttFile:
    #print line
    if len(line.split("."))==3:
        if packageFile!=None:
            packageFile.flush()
            packageFile.close()
            print ("File with name: "+fileName+" closed")

        packageName=line.strip("\n")
        print ("Package Name: "+packageName)
        fileName=line.split(".")[2].strip("\n")+".txt"
        #print fileName
        #Create file with corresponding package name
        packageFile=open(fileName, "a")

        #packageFile.flush()
        #packageFile.close()
    else:
        activityName=line.strip("\n")
        print ("Activity Name: "+activityName)
        ## if packageName=="com.android.browser":
             ## #print packageName
             ## ommand="adb -s emulator-5554 shell am start -a android.intent.MAIN -n "+packageName+"/"+activityName
             ## print command
             ## ## result=subprocess.Popen(command, shell=False, stdout=subprocess.PIPE)
             ## ## result=result.stdout.read()

        #print packageName
        #"com.android.mms":
        
        if kos == 4:         
            command="adb shell am start -n "+packageName+"/"+activityName
            print (command)
            result=subprocess.Popen(command, shell=False, stdout=subprocess.PIPE)
            result=result.stdout.read()
            time.sleep(10)

            print ("Parsing has been started")
            f=open("AFTT.txt", "w")

            command='adb shell '      
            comm='adb '

            for port in range(5939,5979,2):   
                try:              
                    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
                    subprocess.Popen(command+'service call window 2', shell=False, stdout=subprocess.PIPE)
                    time.sleep(.5)
                    subprocess.Popen(command+'service call window 1 i32 4939', shell=False, stdout=subprocess.PIPE)
                    time.sleep(.5)

                    adb(comm+' forward tcp:%d tcp:4939' % port)
                    print ("forwarding done")

                    s.connect(('127.0.0.1', port))
                    #print "Connection Made"
                    print ("Port Used for Communication: %s" %port)
                    hashId=getWindowHash()
                    k='b202f808'
                    print ("Window Hash_Id: %s" %hashId)
                    hsTe = 'DUMP %s\n'%k;
                    s.sendall(hsTe.encode(encoding='utf_8'))
                    print ("Command sent")
                    s.settimeout(360)
                    data=''
                    i=0
                    t0 = time.time()            
                    print ("Starting loop")
                    while True:
                        datum=s.recv(32*1024)
                        #print datum
                        #print 'Received %d bytes' % len(datum)        
                        #print "\n"
                        print ("Packet: "+str(datum))
                        f.write(str(datum))

                        hsTe1 = '\nDONE.\n'
                        hsTe2 = 'DONE.\n'
                        hsTe3 = '\nDONE.\nDONE\n'
                        hsTe4 = 'DONE.\nDONE\n'
                        hsTe1 = hsTe1.encode(encoding='utf_8')
                        hsTe2 = hsTe2.encode(encoding='utf_8')
                        hsTe3 = hsTe3.encode(encoding='utf_8')
                        hsTe4 = hsTe4.encode(encoding='utf_8')
                        if (datum.endswith(hsTe1) or datum.endswith(hsTe2) or datum.endswith(hsTe3) or datum.endswith(hsTe4)):
                            #print "End of Packet ransfer"
                            break 

                        if datum == '':
                            #print "Socket closed"
                            raise socket.error('Socket closed')

                        data+=str(datum)

                        if time.time() - t0 > 360:
                            #print "Timeout"
                            raise socket.error('Timeout')                
                        i=i+1
                    break

                except socket.error:
                    #print "Checking for another port"
                    subprocess.Popen(command+'service call window 2', shell=False, stdout=subprocess.PIPE)
                    time.sleep(.5)
                    subprocess.Popen(command+'service call window 1 i32 4939', shell=False, stdout=subprocess.PIPE)
                    time.sleep(.5)
                    #f.close()
                    s.close()
                    #print "Server restarted"

            #Open File for Parsing UI Elements
            f=open("AFTT.txt", "r")
            #package=open("Package.txt", "w")
            for line in f:
                widg_id=re.compile(r'mID=\S*', re.MULTILINE).findall(line)
                widg_text=re.compile(r'mText=\d*,[a-zA-Z\W\d]*', re.MULTILINE).findall(line)

                if len(widg_id)!=0 or len(widg_text)!=0:
                    ##################################################################
                    #Parse Widget Id
                    if len(widg_id)!=0:
                        widg_id=widg_id[0]        
                        widg_id=str(widg_id) 
                        widg_id=widg_id.strip("[]'")
                        if 'id' in widg_id:
                            widg_id=widg_id.split(",")[1].split("/")[1]
                        else:
                            widg_id=widg_id.split(",")[1]   
                        packageFile.write(widg_id+"->")
                    else:
                        packageFile.write("None->")

                    ##################################################################    
                    #Parse Widget Text
                    if len(widg_text)!=0:
                        widg_text=str(widg_text)
                        #Remove unncessary characters from String
                        widg_text=widg_text.strip("[]'")

                        #Get the second element that is excluding 'mText'
                        widg_text=widg_text.split(",")[1]

                        #SPlit text on basis of space
                        widg_text_ls=widg_text.split(" ")

                        widg_text=""
                        #Remove one element from last
                        widg_text_ls.pop()        
                        #Create new STring by joining list
                        widg_text=" ".join(widg_text_ls)       

                        if len(widg_text)==0:
                            packageFile.write("None->")
                        else:
                            packageFile.write(widg_text+"->")
                    else:
                        packageFile.write("None->")

                    ##################################################################    
                    #Parse Widget Type
                    widg_type=str(line.split("@")[0])
                    widg_type=widg_type.strip(" ")
                    packageFile.write(widg_type)
                    packageFile.write("\n")
            f.close()    
afttFile.close()