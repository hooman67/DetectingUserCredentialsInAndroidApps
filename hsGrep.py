import re, sys

def grep(s,pattern):
    #return '\n'.join(re.findall(r'^.*%s.*?$'%pattern,s,flags=re.M))
    return re.findall(r'^.*%s.*?$'%pattern,s,flags=re.M)

ff = open("resultOf_dumpsys.txt", "r")
for line in ff:
	k = grep(line,"hintText");
	if k!=[]:
		print(k)