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
				vals[0] = w_type
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
						vals[2] = value

					if prop == "focus:hasFocus()" :
						vals[3] = value

					if prop == "focus:isFocusable()" :
						vals[4] = value

					if prop == "isClickable()" :
						vals[5] = value

					if prop == "mViewFlags" :
						vals[6] = value

					if prop == "mPrivateFlags" :
						vals[7] = value

					if prop == "drawing:hasOverlappingRendering()" :
						vals[8] = value

					if prop == "mPrivateFlags_DRAWING_CACHE_INVALID" :
						vals[9] = value
					
					if prop == "layout:getLocationOnScreen_x()" :
						vals[10] = value

					if prop == "layout:getLocationOnScreen_y()" :
						vals[11] = value

					if prop == "layout:getWidth()" :
						vals[12] = value
					
					if prop == "drawing:getX()" :
						vals[13] = value

					if prop == "drawing:getY()" :
						vals[14] = value

					if prop == "drawing:getZ()" :
						vals[15] = value


###########THESE DONT WOORK
					#if prop == "mPrivateFlags_DRAWN" :
						#vals[10] = value
					#if prop == "text:mText" :
						#vals[10] = value
#################################################
			
			for st in vals:
				if st != "":
					outFile_csv.write(st + ',')
				#print("wrote")
		outFile_csv.write("\n")

outFile_csv.close()
#######################################################################################
