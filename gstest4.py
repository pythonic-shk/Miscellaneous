strg = 'aabcabcacccccccccbcbcbdaaaaa'
count = 1
prevcount = 0
subseq = ''
prevsubseq = ''
for i,s in enumerate(strg):
	#print(i)
	#print(s)
	if count > prevcount:
		prevcount = count
		prevsubseq = subseq
	count = 1
	subseq = ''
	subseq +=s
	for l in strg[i+1:]:
		#print(l)
		if s!=l:
			break
		else:
			count+=1
			subseq+=l


print(prevcount)
print(prevsubseq)
