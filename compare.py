import sys, termcolor
f1 = sys.argv[1]
f2 = sys.argv[2]

with open(f1, "r") as f:
	x = f.read()
with open(f2, "r") as f:
	y = f.read()

if "-lines" in sys.argv:
	y = y.split("\n")

for line in x.split("\n"):
	if line.replace(" ", "").replace("\t", "") == "": continue
	if line in y:
		print(termcolor.RESET + termcolor.colored("Match   :", "green") + termcolor.RESET + line)
	else:
		print(termcolor.RESET + termcolor.colored("No match:", "red") + termcolor.RESET + line)

