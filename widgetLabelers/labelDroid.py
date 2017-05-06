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
	hasFocus = -1

	#features used for classification
	rank = -1
	isTypeTextEdit = -1
	isTypeTextView = -1
	isTypeAutoComplete = -1
	isIdUsername = -1
	isIdPassword = -1
	isIdName = -1
	isIdNumber = -1
	isIdPhone = -1
	isIdEmail = -1
	isIdAccount = -1
	hasText = -1
	isClickable = -1
	isFocusable = -1
	isVisible = -1
	hasOverlappingRendering = -1
	mPrivateFlags = -1
	mViewFlags = -1
	mPrivateFlags_DRAWN = -1
	
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
"hasFocus()",
"layout:getWidth"]

userNameWords = [
"username","UserName","USERNAME",
"User","user","USER"
]

emailWords = ["email", "Email", "EMAIL","E-MAIL", "e-mail","E_MAIL","e_mail"]
phoneWords = ["Phone","phone","tel", "Tel", "TEL", "TELEPHONE", "telephone", "PHONE"]
accountWords = ["account","Account","ACCOUNT"]
nameWords = ["name","Name","NAME"]
numberWords = ["number", "Number","NUMBER","#"]

passwordWords = [
"pass","Pass","pin", "Pin","PIN","PASS","PASSWORD","PASSCODE","PINCODE"
"password","Password","passcode", "Passcode", "passCode", "pass_code"
]
#######################################################################################


###################################FUNCTIONS###########################################
#Function for executing adb shell command
def adb(command, input=None):
	if not isinstance(command,list): command=command.split()
	return subprocess.Popen(command, stdout=subprocess.PIPE, 
						stderr=subprocess.STDOUT).communicate(input=input)[0]


#Function for getting current window hash id
def getWindowHash():

	window_dump=subprocess.Popen('adb shell dumpsys window windows', shell=True, stdout=subprocess.PIPE)
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
	out = ""
	itemTypeLine = re.findall('mServedView=\S*',str(dumResults))
	if len(itemTypeLine) != 0:
		bracSplit = re.split('{',itemTypeLine[0])
		firstPartSplit = re.split('=',bracSplit[0])
		out = firstPartSplit[1] + '@' + bracSplit[1]
	return out



#######################################################################################
#********************** START OF THE APP**********************************************#
#######################################################################################

############Read Packag Names###########
for line in afttFile:

	currentPackageName=line.strip("\n")
	command_start="adb shell monkey -p " + currentPackageName + " 1"
	print ("\nCurrent Package Name: "+currentPackageName + "\n")

	result=subprocess.Popen(command_start, shell=True, stdout=subprocess.PIPE)
	result=result.stdout.read()

	while True:
	
		activityNb = input("Please enter activity depth: ")
		print("you entered: " + str(activityNb) + "\n")
		
		label = input("Please enter lable: 0 for nothing 1 for password 2 for username other for exit: ")
		
		if (label==0 or label==1 or label==2):

			###################communication start#############################################
			f=open(currentPackageName+".txt", "w")

			print("communication start:")
			try:              
				s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
				subprocess.Popen('adb shell service call window 2', shell=True, stdout=subprocess.PIPE)
				time.sleep(.5)
				subprocess.Popen('adb shell service call window 1 i32 4939', shell=True, stdout=subprocess.PIPE)
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
				subprocess.Popen(command+'service call window 2', shell=True, stdout=subprocess.PIPE)
				time.sleep(.5)
				subprocess.Popen(command+'service call window 1 i32 4939', shell=True, stdout=subprocess.PIPE)
				time.sleep(.5)
				s.close()

			f.close()





			#######################################################################################
			#********************** PARSING SECTION **********************************************#
			#######################################################################################
			elementsFoundSoFar=[]
			if currentPackageName == "":
				print("EROR: AFTT file was not created\n")
				exit()

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

			featuresNb = 0
			wholeFile = ""
		
			for line in f:
			   wholeFile += line;

			f.close()

			#######################################################################################


			############################### Parsing the Segmented File ############################
			outFile_csv=open("output_"+str(label) + "_"+ str(currentPackageName) +".csv","w")

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
								featuresNb += 1
								curFit.rank = featuresNb
							else:
								curFit.isTypeTextEdit = 0

							if ("view" in w_type_temp or "View" in w_type_temp) and ("text" in w_type_temp or "Text" in w_type_temp):
								curFit.isTypeTextView = 1
							else:
								curFit.isTypeTextView = 0

							if ("auto" in w_type_temp or "Auto" in w_type_temp) and ("complete" in w_type_temp or "Complete" in w_type_temp):
								curFit.isTypeAutoComplete = 1
								featuresNb += 1
								curFit.rank = featuresNb
							else:
								curFit.isTypeAutoComplete = 0

						else:
							if any(xxx in singleWidgetArr[indk] for xxx in featuresToKeep):

								#seperate out propertyName and value
								singleProp = re.split(',', singleWidgetArr[indk])
								value = singleProp[1]
								singleProp = re.split('=', singleWidgetArr[indk])
								prop = singleProp[0]


								if prop == "mID":
									curFit.fId = value

									if any(xx in value for xx in userNameWords):
										curFit.isIdUsername = 1
									else:
										curFit.isIdUsername = 0

									if any(x in value for x in passwordWords):
										curFit.isIdPassword = 1
									else:
										curFit.isIdPassword = 0

									if any(x in value for x in emailWords):
										curFit.isIdEmail = 1
									else:
										curFit.isIdEmail = 0

									if any(x in value for x in nameWords):
										curFit.isIdName = 1
									else:
										curFit.isIdName = 0

									if any(x in value for x in accountWords):
										curFit.isIdAccount = 1
									else:
										curFit.isIdAccount = 0

									if any(x in value for x in numberWords):
										curFit.isIdNumber = 1
									else:
										curFit.isIdNumber = 0

									if any(x in value for x in phoneWords):
										curFit.isIdPhone = 1
									else:
										curFit.isIdPhone = 0




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

								if prop == "focus:hasFocus()" :
									if value == "true":
										curFit.hasFocus = 1
									else:
										curFit.hasFocus = 0


					elementsFoundSoFar.append(curFit)
			#######################################################################################





			#######################################################################################
			#********************** Labeling SECTION *********************************************#
			#######################################################################################
#			for elem in elementsFoundSoFar:
#				if elem.hasFocus and elem.rank != -1:
#					elem.lebel = label

			#get screen dump
			dumResults=subprocess.Popen("adb shell dumpsys input_method", shell=True, stdout=subprocess.PIPE)
			dumResults=dumResults.stdout.read()
			dumResults = str(dumResults)
			time.sleep(3)

			if "@" in dumResults:
				print('labling method 1')
				fullItemType = getSelectedWidgetsID(dumResults)
				print(str(fullItemType))

				#find the element corresponding to the ID and mark the results
				if fullItemType != "":
					for elem in elementsFoundSoFar:
						if elem.ftype == fullItemType:
							elem.lebel = label
				else:
					print("could not find ID of selected wid")


			else:
				print('labling method 2')
				for elem in elementsFoundSoFar:
					if elem.hasFocus and elem.rank != -1:
						elem.lebel = label

  


	   

			#######################################################################################
			#********************** Writing the report********************************************#
			#######################################################################################
			print("Savings the results for " + currentPackageName + "\n")

			outFile_csv.write("Label,Type,ID,xLoc,yLoc,width,hasFocus,ActivityDepth,totalNbOfWidgets,Rank,isWidthZero,isTypeEditText,isTypeTextView,isTypeAutoComplete,isIdUsername,isIdPassword,isIdEmail,isIdAccount,isIdPhone,isIdNumber,isIdName,hasText,isVisible,isFocusable,isClickable,hasOverlappingRendering,mPrivateFlags,mViewFlags,mPrivateFlags_DRAWN" + '\n')
			for el in elementsFoundSoFar:

				outFile_csv.write(str(el.lebel) + ',')
				outFile_csv.write(str(el.ftype) + ',')
				outFile_csv.write(str(el.fId) + ',')
				outFile_csv.write(str(el.xLocOnScreen) + ',')
				outFile_csv.write(str(el.yLocOnScreen) + ',')
				outFile_csv.write(str(el.layoutWidth) + ',')
				outFile_csv.write(str(el.hasFocus) + ',')

				outFile_csv.write(str(activityNb) + ',')
				outFile_csv.write(str(featuresNb) + ',')
				outFile_csv.write(str(el.rank) + ',')
				outFile_csv.write(str(el.isWidthZero) + ',')
				outFile_csv.write(str(el.isTypeTextEdit) + ',')
				outFile_csv.write(str(el.isTypeTextView) + ',')
				outFile_csv.write(str(el.isTypeAutoComplete) + ',')
				outFile_csv.write(str(el.isIdUsername) + ',')
				outFile_csv.write(str(el.isIdPassword) + ',')
				outFile_csv.write(str(el.isIdEmail) + ',')
				outFile_csv.write(str(el.isIdAccount) + ',')
				outFile_csv.write(str(el.isIdPhone) + ',')
				outFile_csv.write(str(el.isIdNumber) + ',')
				outFile_csv.write(str(el.isIdName) + ',')
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
		else:
			break