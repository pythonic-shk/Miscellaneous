
import os
initial1 = 1
initial2 = 1
while(1):
	os.system('cls')
	n = input("Enter n to find the nth Fibonacci Number: ")
	series = []
	series.extend([initial1,initial2])
	try:
		if int(n) <=2 and int(n) > 0:
			print("Nth Fibonacci Number is 1")
			print("Fib Series is ",series)
			resp = input("Do you want to exit (y/n) ")
			if resp.upper() == 'Y':
				break
			else:
				continue
		else:
			print("Only Positive Integers")
			resp = input("Do you want to exit (y/n) ")
			if resp.upper() == 'Y':
				break
			else:
				continue
	except:
		print("You need to enter only Integers.")
		resp = input("Do you want to exit (y/n) ")
		if resp.upper() == 'Y':
			break
		else:
			continue
	for i in range(int(n)-2):
		temp = initial2
		initial2 = initial1 + initial2
		initial1 = temp
		series.append(initial2)
	print("Nth Fibonacci Number is ",initial2)
	print("Fib Series is ",series)
	resp = input("Do you want to exit (y/n) ")
	if resp.upper() == 'Y':
		break
	else:
		continue