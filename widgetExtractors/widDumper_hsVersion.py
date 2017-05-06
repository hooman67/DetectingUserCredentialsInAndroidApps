#######################################################################################
#********************** DUMPING SECTION **********************************************#
#######################################################################################
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


#Function for retriving the typeID of the currently selected widget
def getSelectedWidgetsID(dumResults):
    #find selected widget's ID
    itemTypeLine = re.findall('mServedView=\S*',str(dumResults))
    out = ""
    if len(itemTypeLine) != 0:
    	bracSplit = re.split('{',itemTypeLine[0])
    	firstPartSplit = re.split('=',bracSplit[0])
    	out = firstPartSplit[1] + '@' + bracSplit[1]
    return out




############Read Packag Name & start the app###########
for line in afttFile:

    currentPackageName=line.strip("\n")
    command_start="adb shell monkey -p " + currentPackageName + " 1"
    print ("\nCurrent Package Name: "+currentPackageName + "\n")
    #print("Command to send:  "+ command_start)

    result=subprocess.Popen(command_start, shell=False, stdout=subprocess.PIPE)
    result=result.stdout.read()
    input("Ones happy with the opened window press Enter to continue...\n")


###################communication start#############################################
    f=open(currentPackageName+".txt", "w")

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
        print ("all dump Commands sent")
    
        s.settimeout(360)
        data=''
        t0 = time.time()            
    
        print ("Listening for replies")
        while True:
            datum=s.recv(32*1024)
            #print ("Packet: "+str(datum))
            f.write(str(datum))


            if (datum.endswith(hsTe1) or datum.endswith(hsTe2) or datum.endswith(hsTe3) or datum.endswith(hsTe4)):
                print ("End of Packet ransfer\n\n")
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





#######################################################################################
#********************** PARSING SECTION **********************************************#
#######################################################################################
if currentPackageName == "":
	print("EROR: AFTT file was not created\n")
	exit()


########################## FEATURES TO EXTRACT ########################################
class feature:
	#adminstrative features
	fId = ""
	ftype = ""
	lebel = 0 # class0: neither -- class 1: password -- class 2: username 
	xLocOnScreen = -1
	yLocOnScreen = -1
	layoutWidth = -1
	isWidthZero = -1
	hasInlineImage = 0
	hintText = "none"

	#features used for classification
	isTypeTextEdit = -1
	isTypeTextView = -1
	isTypeAutoComplete = -1
	isIdUsername = -1
	isIdPassword = -1
	hasText = -1
	isClickable = -1
	isFocusable = -1
	isVisible = -1
	hasOverlappingRendering = -1
	mPrivateFlags = -1
	mViewFlags = -1
	mPrivateFlags_DRAWN = -1



elementsFoundSoFar= []
	
featuresToKeep = [
"mID",
"mText",
"isClickable",
"isFocusable",
"hasOverlappingRendering",
"getVisibility",
"mPrivateFlags",
"mViewFlags",
"mPrivateFlags_DRAWN",
"getLocationOnScreen_x",
"getLocationOnScreen_y",
"layout:getWidth"]

userNameWords = [
"username","UserName",
"User","user",
"email","Email",
"account","Account",
"Phone","phone",
"login-id","login-ID","Login-Id","Login-ID",
"login-name","login-Name","Login-Name","Login-Name",
"login_id","login_ID","Login_Id","Login_ID",
"login_name","login_Name","Login_Name","Login_Name",
"loginName","LoginName",
"LoginID","loginID","LoginId","loginId"
]

passwordWords = [
"pass","Pass","pin", "Pin",
"password","Password","passcode", "Passcode", "passCode", "pass_code"
]
#######################################################################################


########################### segmenting the file #######################################
srcFile=open(currentPackageName+".txt", "r")
outFile=open("segmented_" + currentPackageName + ".txt","w")

#you  want  android.widget.EditText at the begining of the line
outFile.write(srcFile.read().replace(r' \n  ',"\n\n\n\n"))

srcFile.close()
outFile.close()
#######################################################################################


########### Loading The Whole File Into One String ####################################
f=open("segmented_" + currentPackageName + ".txt", "r")

wholeFile = ""
for line in f:
	wholeFile += line;

f.close()
#######################################################################################


############################### Parsing the Segmented File ############################
outFile_csv=open("output_"+ currentPackageName +".csv","w")

wholeFileArr = re.split('\n\s{4,}',wholeFile)

for ind in range(len(wholeFileArr)):
	if ind != 0:
		
		curFit = feature()
		singleWidgetArr = re.split(' ', wholeFileArr[ind])

		for indk in range(len(singleWidgetArr)):

			if indk == 0 :
				w_type_temp = singleWidgetArr[indk]
				curFit.ftype = w_type_temp

				if ("edit" in w_type_temp or "Edit" in w_type_temp) and ("text" in w_type_temp or "Text" in w_type_temp):
					curFit.isTypeTextEdit = 1
				else:
					curFit.isTypeTextEdit = 0

				if ("view" in w_type_temp or "View" in w_type_temp) and ("text" in w_type_temp or "Text" in w_type_temp):
					curFit.isTypeTextView = 1
				else:
					curFit.isTypeTextView = 0

				if ("auto" in w_type_temp or "Auto" in w_type_temp) and ("complete" in w_type_temp or "Complete" in w_type_temp):
					curFit.isTypeAutoComplete = 1
				else:
					curFit.isTypeAutoComplete = 0

			else:
				if any(xxx in singleWidgetArr[indk] for xxx in featuresToKeep):
					
					#seperate out propertyName and value
					singleProp = re.split(',', singleWidgetArr[indk])
					value = singleProp[1]
					singleProp = re.split('=', singleWidgetArr[indk])
					prop = singleProp[0]


					if prop == "mID" :
						curFit.fId = value

						if any(xx in value for xx in userNameWords):
							curFit.isIdUsername = 1
						else:
							curFit.isIdUsername = 0

						if any(x in value for x in passwordWords):
							curFit.isIdPassword = 1
						else:
							curFit.isIdPassword = 0


					if prop == "layout:getLocationOnScreen_x()" :
						curFit.xLocOnScreen = value

					if prop == "layout:getLocationOnScreen_y()" :
						curFit.yLocOnScreen = value

					if prop == "mViewFlags" :
						curFit.mViewFlags = value

					if prop == "mPrivateFlags" :
						curFit.mPrivateFlags = value

					if prop == "mPrivateFlags_DRAWN" :
						curFit.mPrivateFlags_DRAWN = value


					if prop == "layout:getWidth()" :
						curFit.layoutWidth = value
						if value is '0':
							curFit.isWidthZero = 1
						else:
							curFit.isWidthZero = 0

					if prop == "getVisibility()" :
						if value == "VISIBLE" or value == "VIS'b'IBLE":
							curFit.isVisible = 1
						else:
							curFit.isVisible = 0

					if prop == "focus:isFocusable()" :
						if value == "true":
							curFit.isFocusable = 1
						else:
							curFit.isFocusable = 0

					if prop == "isClickable()" :
						if value == "true":
							curFit.isClickable = 1
						else:
							curFit.isClickable = 0

					if prop == "drawing:hasOverlappingRendering()" :
						if value == "true":
							curFit.hasOverlappingRendering = 1
						else:
							curFit.hasOverlappingRendering = 0

					if prop == "text:mText" :
						singleProp = re.split(',', singleWidgetArr[indk])
						singleProp = re.split('=', singleProp[0])
						if singleProp[1] == '0':
							curFit.hasText = 0
						else:
							curFit.hasText = 1


		elementsFoundSoFar.append(curFit)
#######################################################################################





#######################################################################################
#********************** Labeling SECTION *********************************************#
#######################################################################################
input("Select the UserName field and press Enter to label it...")

#get screen dump
dumResults=subprocess.Popen("adb shell dumpsys input_method", shell=False, stdout=subprocess.PIPE)
dumResults=dumResults.stdout.read()
time.sleep(3)

hints = re.findall('hintText=\S*',str(dumResults))
if hints != 0:
	print("\nFound a hint: "+ hints[0] + "\n")

fullItemType = getSelectedWidgetsID(dumResults)

#find the element corresponding to the ID and mark the results
if fullItemType != "":
	for elem in elementsFoundSoFar:
		if elem.ftype == fullItemType:
			elem.lebel = 2
			hintsp = re.split('=',hints[0])
			if len(hintsp) > 0:
				elem.hintText = hintsp[1]


input("Select the Password field and press Enter to label it...")

#get screen dump
dumResults=subprocess.Popen("adb shell dumpsys input_method", shell=False, stdout=subprocess.PIPE)
dumResults=dumResults.stdout.read()
time.sleep(3)

hints = re.findall('hintText=\S*',str(dumResults))
if hints != 0:
	print("\nFound a hint: "+ hints[0] + "\n")

fullItemType = getSelectedWidgetsID(dumResults)

#find the element corresponding to the ID and mark the results
if fullItemType != "":
	for elem in elementsFoundSoFar:
		if elem.ftype == fullItemType:
			elem.lebel = 1
			hintsp = re.split('=',hints[0])
			if len(hintsp) > 0:
				elem.hintText = hintsp[1]


print("Savings the results for " + currentPackageName + "\n")

outFile_csv.write("Label,Type,ID,xLoc,yLoc,width,isWidthZero,hasInlineImage,hintText,isTypeEditText,isTypeTextView,isTypeAutoComplete,isIdUsername,isIdPassword,hasText,isVisible,isFocusable,isClickable,hasOverlappingRendering,mPrivateFlags,mViewFlags,mPrivateFlags_DRAWN" + '\n')
for el in elementsFoundSoFar:

	outFile_csv.write(str(el.lebel) + ',')
	outFile_csv.write(str(el.ftype) + ',')
	outFile_csv.write(str(el.fId) + ',')
	outFile_csv.write(str(el.xLocOnScreen) + ',')
	outFile_csv.write(str(el.yLocOnScreen) + ',')
	outFile_csv.write(str(el.layoutWidth) + ',')

	outFile_csv.write(str(el.isWidthZero) + ',')
	outFile_csv.write(str(el.hasInlineImage) + ',')
	outFile_csv.write(str(el.hintText) + ',')
	outFile_csv.write(str(el.isTypeTextEdit) + ',')
	outFile_csv.write(str(el.isTypeTextView) + ',')
	outFile_csv.write(str(el.isTypeAutoComplete) + ',')
	outFile_csv.write(str(el.isIdUsername) + ',')
	outFile_csv.write(str(el.isIdPassword) + ',')
	outFile_csv.write(str(el.hasText) + ',')
	outFile_csv.write(str(el.isVisible) + ',')
	outFile_csv.write(str(el.isFocusable) + ',')
	outFile_csv.write(str(el.isClickable) + ',')
	outFile_csv.write(str(el.hasOverlappingRendering) + ',')
	outFile_csv.write(str(el.mPrivateFlags) + ',')
	outFile_csv.write(str(el.mViewFlags) + ',')
	outFile_csv.write(str(el.mPrivateFlags_DRAWN) + ',')

	outFile_csv.write('\n')

outFile_csv.close()








