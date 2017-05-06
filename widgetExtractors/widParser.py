import time, subprocess, socket, re


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

wholeFileArr = re.split('\n\s{4,}',wholeFile)


outFile=open("outputFile.txt","w")
for ind in range(len(wholeFileArr)):
	if "EditText" in wholeFileArr[ind]: 
		#outFile.write(wholeFileArr[ind] +"\n\n")
		#print(str(len(wholeFileArr)))
		widg_id=re.compile(r'mID=\S*', re.MULTILINE).findall(wholeFileArr[ind])
		widg_xloc = re.compile(r'getLocationOnScreen_x\S*', re.MULTILINE).findall(wholeFileArr[ind])
		widg_yloc = re.compile(r'layout:getLocationOnScreen_y\S*', re.MULTILINE).findall(wholeFileArr[ind])

		for index in range(len(widg_id)):
			outFile.write("\n\n")
			outFile.write(widg_id[index] + "\n")
			outFile.write(widg_xloc[index] + "\n")
			outFile.write(widg_yloc[index] + "\n")

outFile.close()