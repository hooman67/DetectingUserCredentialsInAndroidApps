import time, subprocess, socket, re

########################## FEATURES TO EXTRACT ########################################
class feature:
	#adminstrative features
	fId = ""
	ftype = ""
	classificationResult = -1 # class0: neither -- class 1: password -- class 2: username 
	xLocOnScreen = -1
	yLocOnScreen = -1
	layoutWidth = -1
	drawingX = -1
	drawingY = -1
	drawingZ = -1

	#features used for classification
	isTypeTextEdit = -1
	hasText = -1
	isClickable = -1
	isFocusable = -1
	isVisible = -1

	#other potential features
	hasOverlappingRendering = -1
	mPrivateFlags = -1
	mViewFlags = -1
	mPrivateFlags_DRAWN = -1
	hasFocus = -1


elementsFoundSoFar= []
	
featuresToKeep = [
"mID",
"mText",
"isClickable",
"isFocusable",
"hasFocus()",
"hasOverlappingRendering",
"getVisibility",
"mPrivateFlags",
"mViewFlags",
"mPrivateFlags_DRAWN",
"getLocationOnScreen_x",
"getLocationOnScreen_y",
"layout:getWidth",
"drawing:getX",
"drawing:getY",
"drawing:getZ"]
#######################################################################################


########################### segmenting the file #######################################
srcFile=open("AFTT.txt", "r")
outFile=open("segmentedFile.txt","w")

#you  want  android.widget.EditText at the begining of the line
outFile.write(srcFile.read().replace(r' \n  ',"\n\n\n\n"))

srcFile.close()
outFile.close()
#######################################################################################


########### Loading The Whole File Into One String ####################################
f=open("segmentedFile.txt", "r")

wholeFile = ""
for line in f:
	wholeFile += line;

f.close()
#######################################################################################


##### Spliting The Whole_File_String BY Wideget Type Keeping Desired Features Only ####
outFile_txt=open("outputFile.txt","w")
wholeFileArr = re.split('\n\s{4,}',wholeFile)

for ind in range(len(wholeFileArr)):
		
	singleWidgetArr = re.split(' ', wholeFileArr[ind])
	for indk in range(len(singleWidgetArr)):
	
		if indk == 0 :
			outFile_txt.write("hsWidType," + singleWidgetArr[indk] + "\n")
		else:
			if any(xxx in singleWidgetArr[indk] for xxx in featuresToKeep):
				outFile_txt.write(singleWidgetArr[indk]+"\n")
		
	outFile_txt.write("\n\n\n\n")

outFile_txt.close()
#######################################################################################


############################### CREATING A CSV ########################################
outFile_csv=open("outputFile.csv","w")

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

			else:
				if any(xxx in singleWidgetArr[indk] for xxx in featuresToKeep):
					
					#seperate out propertyName and value
					singleProp = re.split(',', singleWidgetArr[indk])
					value = singleProp[1]
					singleProp = re.split('=', singleWidgetArr[indk])
					prop = singleProp[0]

					#print("prop: " + prop + "\n")

					if prop == "mID" :
						curFit.fId = value

					if prop == "layout:getLocationOnScreen_x()" :
						curFit.xLocOnScreen = value

					if prop == "layout:getLocationOnScreen_y()" :
						curFit.yLocOnScreen = value

					if prop == "layout:getWidth()" :
						curFit.layoutWidth = value

					if prop == "drawing:getX()" :
						curFit.drawingX = value

					if prop == "drawing:getY()" :
						curFit.drawingY = value

					if prop == "drawing:getZ()" :
						curFit.drawingZ = value

					if prop == "mViewFlags" :
						curFit.mViewFlags = value

					if prop == "mPrivateFlags" :
						curFit.mPrivateFlags = value

					if prop == "mPrivateFlags_DRAWN" :
						curFit.mPrivateFlags_DRAWN = value


					if prop == "getVisibility()" :
						if value == "VISIBLE" or value == "VIS'b'IBLE":
							curFit.isVisible = 1
						else:
							curFit.isVisible = 0

					if prop == "focus:hasFocus()" :
						if value == "true":
							curFit.hasFocus = 1
						else:
							curFit.hasFocus = 0

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


#################### Writing the identified elements to File ##########################
outFile_csv.write("Label,Type,ID,xLoc,yLoc,width,drwaingLocX,drwaingLocY,drwaingLocZ,isTypeTextEdit,hasText,isVisible,isFocusable,isClickable,hasOverlappingRendering,mPrivateFlags,mViewFlags,mPrivateFlags_DRAWN,hasFocus" + '\n')
for el in elementsFoundSoFar:

	outFile_csv.write(str(el.classificationResult) + ',')
	outFile_csv.write(str(el.ftype) + ',')
	outFile_csv.write(str(el.fId) + ',')
	outFile_csv.write(str(el.xLocOnScreen) + ',')
	outFile_csv.write(str(el.yLocOnScreen) + ',')
	outFile_csv.write(str(el.layoutWidth) + ',')
	outFile_csv.write(str(el.drawingX) + ',')
	outFile_csv.write(str(el.drawingY) + ',')
	outFile_csv.write(str(el.drawingZ) + ',')
				
	outFile_csv.write(str(el.isTypeTextEdit) + ',')
	outFile_csv.write(str(el.hasText) + ',')
	outFile_csv.write(str(el.isVisible) + ',')
	outFile_csv.write(str(el.isFocusable) + ',')
	outFile_csv.write(str(el.isClickable) + ',')
				
	outFile_csv.write(str(el.hasOverlappingRendering) + ',')
	outFile_csv.write(str(el.mPrivateFlags) + ',')
	outFile_csv.write(str(el.mViewFlags) + ',')
	outFile_csv.write(str(el.mPrivateFlags_DRAWN) + ',')
	outFile_csv.write(str(el.hasFocus) + '\n')

outFile_csv.close()
#######################################################################################
