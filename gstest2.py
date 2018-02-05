i = int(input("enter a number: "))
while(1):
	if i == 10:
		print("Power of Ten")
		break
	if i%10!=0 or i == 0:
		print("Not a Power of Ten")
		break
	i/= 10
	