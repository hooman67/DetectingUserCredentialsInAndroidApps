import time, subprocess, socket, re

#####################FEATURES TO EXTRACT####################################
featuresToExtract = [
"mID",
"text:mText",
"isClickable",
"focus:isFocusable",
"focus:hasFocus()",
"drawing:hasOverlappingRendering",
"getVisibility",
"mPrivateFlags",
"mViewFlags",
"layout:getLocationOnScreen_x",
"layout:getLocationOnScreen_y",
"layout:getWidth",
"drawing:getX",
"drawing:getY",
"drawing:getZ"]

##########getting ready for split###########################################
srcFile=open("AFTT.txt", "r")
outFile=open("segmentedFile.txt","w")

#you  want  android.widget.EditText at the begining of the line
outFile.write(srcFile.read().replace(r' \n  ',"\n\n\n\n"))

srcFile.close()
outFile.close()
############################################################################



###########SPLITING THE FILE INTO AN STRING ARRAY###########################
f=open("segmentedFile.txt", "r")

wholeFile = ""
for line in f:
	wholeFile += line;

f.close()


outFile=open("outputFile.txt","w")
wholeFileArr = re.split('\n\s{4,}',wholeFile)

for ind in range(len(wholeFileArr)):
	if ind != 0:
		ktemp = re.split(' ', wholeFileArr[ind])
		for indk in range(len(ktemp)):
	
			if (indk == 0) or any(xxx in ktemp[indk] for xxx in featuresToExtract):
				outFile.write(ktemp[indk]+"\n")
		outFile.write("\n\n\n\n")
#	if "EditText" in wholeFileArr[ind]: 
#		widg_id=re.compile(r'mID=\S*', re.MULTILINE).findall(wholeFileArr[ind])
#		widg_xloc = re.compile(r'getLocationOnScreen_x\S*', re.MULTILINE).findall(wholeFileArr[ind])
#		widg_yloc = re.compile(r'layout:getLocationOnScreen_y\S*', re.MULTILINE).findall(wholeFileArr[ind])
#
#		for index in range(len(widg_id)):
#			outFile.write("\n\n")
#			if index < len(widg_type):
#				outFile.write(widg_type[index] + "\n")
#			else:
#				outFile.write("type:Other\n")
#			outFile.write(widg_id[index] + "\n")
#			outFile.write(widg_xloc[index] + "\n")
#			outFile.write(widg_yloc[index] + "\n")

outFile.close()