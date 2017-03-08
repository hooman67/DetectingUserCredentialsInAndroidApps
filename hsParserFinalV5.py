import time, subprocess, socket, re

########################## FEATURES TO EXTRACT ########################################
featuresToExtract = [
"mID",
"mText",
"isClickable",
"isFocusable",
"hasFocus()",
"hasOverlappingRendering",
"getVisibility",
"mPrivateFlags",
"mViewFlags",
"getLocationOnScreen_x",
"getLocationOnScreen_y",
"layout:getWidth",
"drawing:getX",
"drawing:getY",
"drawing:getZ"]
#######################################################################################


########################### making split easier #######################################
srcFile=open("AFTT.txt", "r")
outFile=open("segmentedFile.txt","w")

#you  want  android.widget.EditText at the begining of the line
outFile.write(srcFile.read().replace(r' \n  ',"\n\n\n\n"))

srcFile.close()
outFile.close()
#######################################################################################


########### Loading The Whole File Into One String #####################################
f=open("segmentedFile.txt", "r")

wholeFile = ""
for line in f:
	wholeFile += line;

f.close()
#######################################################################################


##### Spliting The Whole_File_String BY Wideget Type Keeping Desired Features Only ####
outFile_full=open("outputFile.txt","w")
wholeFileArr = re.split('\n\s{4,}',wholeFile)

for ind in range(len(wholeFileArr)):
	if ind != 0:
		
		singleWidgetArr = re.split(' ', wholeFileArr[ind])
		for indk in range(len(singleWidgetArr)):
	
			if indk == 0 :
				outFile_full.write("hsWidType," + singleWidgetArr[indk] + "\n")
			else:
				if any(xxx in singleWidgetArr[indk] for xxx in featuresToExtract):
					outFile_full.write(singleWidgetArr[indk]+"\n")
		
		outFile_full.write("\n\n\n\n")

outFile_full.close()
#######################################################################################


############################### CREATING A CSV ########################################
outFile_csv=open("outputFile.csv","w")

for ind in range(len(wholeFileArr)):
	if ind != 0:
		
		singleWidgetArr = re.split(' ', wholeFileArr[ind])
		for indk in range(len(singleWidgetArr)):
			vals = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]

			if indk == 0 :
				w_type = singleWidgetArr[indk]
				if ("edit" in w_type or "Edit" in w_type) and ("text" in w_type or "Text" in w_type):
					vals[0] = w_type
				else:
					break
			else:
				if any(xxx in singleWidgetArr[indk] for xxx in featuresToExtract):
					
					#seperate out propertyName and value
					singleProp = re.split(',', singleWidgetArr[indk])
					value = singleProp[1]
					singleProp = re.split('=', singleWidgetArr[indk])
					prop = singleProp[0]

					#print("prop: " + prop + "\n")

					if prop == "mID" :
						vals[1] = value

					if prop == "getVisibility()" :
						if value == "VISIBLE" or value == "VIS'b'IBLE":
							vals[2] = 1
						else:
							vals[2] = 0

					if prop == "focus:hasFocus()" :
						if value == "true":
							vals[3] = 1
						else:
							vals[3] = 0

					if prop == "focus:isFocusable()" :
						if value == "true":
							vals[4] = 1
						else:
							vals[4] = 0

					if prop == "isClickable()" :
						if value == "true":
							vals[5] = 1
						else:
							vals[5] = 0

					if prop == "mViewFlags" :
						vals[6] = value

					if prop == "mPrivateFlags" :
						vals[7] = value

					if prop == "drawing:hasOverlappingRendering()" :
						if value == "true":
							vals[8] = 1
						else:
							vals[8] = 0

					if prop == "text:mText" :
						singleProp = re.split(',', singleWidgetArr[indk])
						singleProp = re.split('=', singleProp[0])
						if singleProp[1] == '0':
							vals[9] = 1
						else:
							vals[9] = 0

###########################ALWAYS 0####################################################
#			always 0		if prop == "mPrivateFlags_DRAWING_CACHE_INVALID" :
#						print(value + "\n")
#						vals[9] = value
					
########################not needed for classifications#################################					
#					if prop == "layout:getLocationOnScreen_x()" :
#						vals[9] = value

#					if prop == "layout:getLocationOnScreen_y()" :
#						vals[10] = value

#					if prop == "layout:getWidth()" :
#						vals[11] = value
					
#					if prop == "drawing:getX()" :
#						vals[12] = value

#					if prop == "drawing:getY()" :
#						vals[13] = value

#					if prop == "drawing:getZ()" :
#						vals[14] = value
#######################################################################################

###########THESE DONT WOORK because the numbers dont match: 8 against 30###############
					#if prop == "mPrivateFlags_DRAWN" :
						#vals[10] = value
					#if prop == "text:mText" :
						#vals[10] = value

#					if prop == "text:mText" :
#						singleProp = re.split(',', singleWidgetArr[indk])
#						singleProp = re.split('=', singleProp[0])
#						print(singleProp[1]+"\n")
#						if singleProp[1] == '0':
#							vals[9] = 1
#						else:
#							vals[9] = 0

#################################################
			
			for st in vals:
				if st != "":
					outFile_csv.write(str(st) + ',')
				#print("wrote")
		outFile_csv.write("\n")

outFile_csv.close()
#######################################################################################
