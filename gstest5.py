import sys
inparray = input("Enter numbers for array separated by a space: ").split()
intgr = int(input("Enter an Integer: "))
subarray = []
inparray = [int(x) for x in inparray]
inparray.sort(reverse=True)
for i in range(len(inparray)-1):
	for j in inparray[i:]:
		if j + sum(subarray) < intgr:
			subarray.append(j)
		elif j + sum(subarray)== intgr:
			subarray.append(j)
			print(subarray)
			sys.exit()
		elif j + sum(subarray) > intgr:
			pass
	subarray = []
print("The Shortest subarray whose length equals the given integer is: ",subarray)