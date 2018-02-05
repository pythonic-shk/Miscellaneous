#add two fractions
def fraction(fractA,fractB):
	fractC = [0,0]
	if fractA[1]==fractB[1]:
		fractC[0] = fractA[0] + fractB[0]
		fractC[1] = fractA[1]
	elif fractA[1]%fractB[1]==0:
		fractC[1] = fractA[1]
		fractC[0] = fractA[0] + (int(fractA[1]/fractB[1])*fractB[0])
	elif fractB[1]%fractA[1]==0:
		fractC[1] = fractB[1]
		fractC[0] = fractB[0] + (int(fractB[1]/fractA[1])*fractA[0])
	else:
		fractC[1] = fractA[1]*fractB[1]
		fractC[0] = fractA[0]*fractB[1] + fractB[0]*fractA[1]

	
	return fractC
	
def main():
	fractA = input("Enter Numerator and Denominator separated by a space: ").split()
	fractA = [int(x) for x in fractA]
	fractB = input("Enter Numerator and Denominator separated by a space: ").split()
	fractB = [int(x) for x in fractB]
	fractC = fraction(fractA,fractB)
	print("The Addition of ",str(fractA[0]),"/",str(fractA[1])," and ",str(fractB[0]),"/",str(fractB[1])," is ",str(fractC[0]),"/",str(fractC[1]))
	
if __name__ == '__main__':
	main()