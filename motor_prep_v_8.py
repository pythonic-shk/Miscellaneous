import xml.etree.ElementTree as ET
from xml.etree.ElementTree import SubElement
from xml.etree.ElementTree import ParseError
import sys
import datetime
import easygui
import os
import random
import requests
import re

###############################
# function defs
###############################

def setPolicyType(xmlRoot):
        elements = xmlRoot.findall('Policy/row/PolicyType')

        for i, el in enumerate(elements,1):
                el.text = str("Renewal")


def createAccountAffinity(xmlRoot):
        elements = xmlRoot.findall('Account/row')

        for i, el in enumerate(elements,1):
                affinity = SubElement(el, 'AccountAffinity')
                affinity.text = 'MoreThan'

def createAffinity(xmlRoot):
        elements = xmlRoot.findall('Policy/row')

        for i, el in enumerate(elements,1):
                affinity = SubElement(el, 'Affinity')
                row = SubElement(affinity, 'row',{'id':'1'})
                brand = SubElement(row, 'BrandIdentifier')
                brand.text = 'MoreThan'
                brand2 = SubElement(row, 'BrandOwner')
                brand2.text = 'RSA'

def createSelectAndBreakdownCoverAndRemoveCov(xmlRoot):
        elements = xmlRoot.findall('Policy/row/Vehicle/row/Packages')
        
        # iter per policy
        for i, el in enumerate(elements,1):
            packages = el.findall('row')
            selectBreakdownCover = SubElement(el, 'SelectBreakdownCover')
            breakdownCover = SubElement(el, 'BreakdownCover')
            # iter per package
            for p in packages:
                # by default I assume there is no breakdown cover
                selectBreakdownCover.text = '0'
                
                ##########################################
                # !!!!! to be removed after BizTalk deployment
                ##########################################
                selectBreakdownCoverPackageLevel = SubElement(p, 'SelectBreakdownCover')
                selectBreakdownCoverPackageLevel.text = '0'
                
                # removing space from coverage name
                renewalPackageNode = p.find('RenewalPackageName')
                packageNameWithoutSpaces = str(renewalPackageNode.text).replace(" ","")
                renewalPackageNode.text = packageNameWithoutSpaces
                if "Breakdown" in packageNameWithoutSpaces:
                    # but when breakdown cover is found then I set values accordingly
                    selectBreakdownCover.text = '1'
                    breakdownCover.text = packageNameWithoutSpaces
                    
                # iter through coverages and remove "Cov" from name
                covers = p.findall('Coverages/row/Type')
                for c in covers:
                    c.text = str(c.text).replace("Cov","")
                
                    


def replaceTitle(xmlRoot):
        elements = xmlRoot.findall('Account/row/Title')

        for i, el in enumerate(elements,1):
                el.text = str("B53 003")

def replaceProfessionallyFittedTracker(xmlRoot):
        elements = xmlRoot.findall('Policy/row/Vehicle/row/ProfessionallyFittedTracker')

        for i, el in enumerate(elements, 1):
                el.text = str("T5")


def replacePaymentpreference(xmlRoot):
    elements = xmlRoot.findall('Policy/row/Paymentpreference')

    for i, el in enumerate(elements, 1):
        el.text = str("Annualy")

def replaceIsSelected(xmlRoot):
    elements = xmlRoot.findall('Policy/row/Vehicle/row/Packages/row/Coverages/row/IsSelected')

    for i, el in enumerate(elements, 1):
        el.text = str("1")

def replaceXPath(xmlRoot, xpath):
        elements = xmlRoot.findall(xpath)
        for i, el in enumerate(elements,1):
                el.text = str("XXXXXXXXXX")

'''added the function replacename to replace masked data for first name and last name in the migration data
   If email exists it extracts first and last name from the first occurence of email.
   If not, then it randomly allots a first name and last name from a pre-populated list.
   Added by Shakeel Javed. Dated 12/7/2017.
'''
def replacename(xmlRoot):
	m_fname_lt = ['John','Mike','Thomas','Tom','David','Dam','Paul','Roger','Oliver','Jack','Harry','Jacob','Charlie','George','James','Henry','Joseph','Freddie','Samuel','Daniel','Benjamin','Edward','Dylan','Harley']
	f_fname_lt = ['Amelia','Olivia','Emily','Isabella','Jessica','Sophie','Grace','Sophia','Mia','Scarlett','Chloe','Daisy','Alice','Millie','Lucy','Evelyn','Rosie','Matilda','Elizabeth','Layla','Maya','Eliza','Georgia','Esme','Rose','Martha','Zara']
	lname_lt = ['Smith','Jones','Williams','Taylor','Davies','Brown','Wilson','Evans','Johnson','Wright']
	try :
		account = xmlRoot.find('Account')
		drivers = xmlRoot.findall('.//Drivers/row')
		email = account.find('.//EmailAddress').text
		if email == None:
			raise Exception
		else:
			fn = email.split('@')[0]
			#fname = fname.replace('.','')
			fname = ''.join([i for i in fn if i.isalpha()])
			split = -( ( -len(fname) )//2 )
			ft_name, lt_name = fname[:split][:10],fname[split:][:9]
			first_name = account.find('.//FirstName')
			first_name.text = ft_name
			last_name = account.find('.//Name')
			last_name.text = lt_name
			last_name = account.find('.//Surname')
			last_name.text = lt_name
			md_name = account.find('.//MiddleName')
			md_name.text = ''
			for i,d in enumerate(drivers):
				if i > 0:
					gender = d.find('.//Gender').text
					if gender == 'M':
						ft_name = random.choice(m_fname_lt)
					elif gender == 'F':
						ft_name = random.choice(f_fname_lt)
					lt_name = random.choice(lname_lt)
				first_name = d.find('.//FirstName')
				first_name.text = ft_name
				last_name = d.find('.//Surname')
				last_name.text = lt_name
				md_name = d.find('.//MiddleName')
				md_name.text = ''
				
		
	except:
		gender = account.find('.//Gender').text
		if gender == 'M':
			first_name = account.find('.//FirstName')
			ft_name = random.choice(m_fname_lt)
			first_name.text = ft_name
		elif gender == 'F':
			first_name = account.find('.//FirstName')
			ft_name = random.choice(f_fname_lt)
			first_name.text = ft_name
		last_name = account.find('.//Name')
		#mgnum = xmlRoot.find('.//MigratedPolicyNumber').text
		#lt_name = mgnum.replace('RSAP','')
		lt_name = random.choice(lname_lt)
		last_name.text = lt_name
		last_name = account.find('.//Surname')
		last_name.text = lt_name
		md_name = account.find('.//MiddleName')
		md_name.text = ''
		for i,d in enumerate(drivers):
			if i > 0:
				gender = d.find('.//Gender').text
				if gender == 'M':
					ft_name = random.choice(m_fname_lt)
				elif gender == 'F':
					ft_name = random.choice(f_fname_lt)
				lt_name = random.choice(lname_lt)
			first_name = d.find('.//FirstName')
			first_name.text = ft_name
			last_name = d.find('.//Surname')
			last_name.text = lt_name
			md_name = d.find('.//MiddleName')
			md_name.text = ''
"""
Added three underlying functions (getpostcode,getadresslist,replaceaddress) to get the post 
code and prepare a soap request with post code to get address (housenumber,street,housename,village etc) through webservice.
Finally to update the address in the parent xml unmasking the address. Added by Shakeel Javed Dated 12/12/2017.
update: dated 01/02/2018: Added error handling in the function replaceaddress to get the web services response again if no response is got.
"""

def getpostcode(xmlRoot):
	address = xmlRoot.find('Account//Addresses')
	town = address.find('.//Town').text.title()
	postcode = address.find('.//PostCode').text
	return town,postcode

def getadresslist(postcode,housename='',housenum='',flatname=''):
	url="http://10.119.184.43:5001/ws/rsa.cmr.duckcreek.address.picklist.get.V01.web.addressPickListGet/rsa_cmr_duckcreek_address_picklist_get_V01_web_addressPickListGet_Port"
	#headers = {'content-type': 'application/soap+xml'}
	headers = {'content-type': 'text/xml'}
	body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v01="http://www.rsagroup.co.uk/pl/duckcreek/getAddressPickList/V01">
		<soapenv:Header>
		  <wsse:Security soapenv:mustUnderstand="1" xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">
			 <wsse:UsernameToken wsu:Id="UsernameToken-1">
				<wsse:Username>BizTalkTech</wsse:Username>
				<wsse:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText">BizTalkTech</wsse:Password>
				<wsu:Created>2014-05-22T07:26:37.833Z</wsu:Created>
			 </wsse:UsernameToken>
		  </wsse:Security>
	   </soapenv:Header>
	   <soapenv:Body>
		  <v01:addressGetPickListRequest>
			 <AddressGetPickListRequest>
				<!--Optional:-->
				<PostalAddress>
				   <!--Optional:-->
				   <county></county>
				   <!--Optional:-->
				   <district></district>
				   <!--Optional:-->
				   <village></village>
				   <!--Optional:-->
				   <region></region>
				   <!--Optional:-->
				   <subregion></subregion>
				   <!--Optional:-->
				   <flatName></flatName>
				   <!--Optional:-->
				   <flatNumber></flatNumber>
				   <!--Optional:-->
				   <houseName></houseName>
				   <!--Optional:-->
				   <houseNumber></houseNumber>
				   <!--Optional:-->
				   <postcode>"""+postcode+"""</postcode>
				   <!--Optional:-->
				   <street></street>
				   <!--Optional:-->
				   <town></town>

				</PostalAddress>
				<!--Optional:-->
			 </AddressGetPickListRequest>
		  </v01:addressGetPickListRequest>
	   </soapenv:Body>
	</soapenv:Envelope>"""
	if housename != '':
		body = body.replace('<houseName></houseName>','<houseName>'+housename+'</houseName>')
	if flatname != '':
		body = body.replace('<flatNumber></flatNumber>','<flatNumber>'+flatname+'</flatNumber>')
		body = body.replace('<flatName></flatName>','<flatName>'+flatname+'</flatName>')
	if housenum != '':
		body = body.replace('<houseNumber></houseNumber>','<houseNumber>'+housenum+'</houseNumber>')
	response = requests.post(url,data=body,headers=headers)
	ResponseSoap = ET.fromstring(str(response.content)[44:-1])
	return ResponseSoap

def replaceaddress(xmlRoot,responseroot,town,postcode):
	try:
		status = responseroot.find('.//Status//value')
	except:
		try:
			responseroot = getadresslist(postcode)
			status = responseroot.find('.//Status//value')
		except:
			print("Some problem with the web service")
	address = xmlRoot.find('Account//Addresses')
	if status.text == "PickList":
		adresslist = []
		descres = responseroot.findall('.//queryResult')
		for desc in descres:
			adresslist.append(desc.find('description').text)
		rawadress = random.choice(adresslist)
		if rawadress.find(town):
			rawadress = rawadress.split(town)[0]
			criterion = re.compile(r"^\d\d\d\D|^\d\d\d|^\d\d\D|^\d\d|^\d\D|^\d|,\s\d\d\d\D|,\s\d\d\d|,\s\d\d\D|,\s\d\d|,\s\d\D|,\s\d")
			try:
				housenum = ''.join(str(e) for e in criterion.findall(rawadress)[0] if e.isalpha() or e.isdigit())
				#rawsplit = rawadress.split(housenum)[1]
				housename = rawadress.split(housenum)[0].replace(',','').strip()
				#street = rawsplit.replace(',','').strip()
			except:
				housenum = ''
				housename = rawadress.split(',')[0].strip()
				# if len(rawadress.split(',')) == 2:
					# street = rawadress.split(',')[-2].strip()
				# elif len(rawadress.split(',')) == 4:
					# street = rawadress.split(',')[-3].strip()
					# village = rawadress.split(',')[-2].strip()
					
		else:
			pcode = re.compile(r"\D\D\d\D\s\d\D\D$|\D\D\d\d\s\d\D\D$|\D\d\D\s\d\D\D$|\D\d\d\s\d\D\D$|\D\D\d\s\d\D\D$|\D\d\s\d\D\D$")
			criterion = re.compile(r"^\d\d\d\D|^\d\d\d|^\d\d\D|^\d\d|^\d\D|^\d|,\s\d\d\d\D|,\s\d\d\d|,\s\d\d\D|,\s\d\d|,\s\d\D|,\s\d")
			rawadress = re.compile(pcode).split(rawadress)[0]
			town = rawadress.split(',')[-1].strip()
			rawadress = rawadress.split(town)[0].strip()
			try:
				housenum = ''.join(str(e) for e in criterion.findall(rawadress)[0] if e.isalpha() or e.isdigit())
				#rawsplit = rawadress.split(housenum)[1]
				housename = rawadress.split(housenum)[0].replace(',','').strip()
				#street = rawsplit.replace(',','').strip()
			except:
				housenum = ''
				housename = rawadress.split(',')[0].strip()
				#street = rawadress.split(',')[-2].strip()	
		sresproot = getadresslist(postcode,housename,housenum,'')
		status = sresproot.find('.//Status//value')
		if status.text == "PickList":
			fresproot = getadresslist(postcode,'',housenum,housename)
			status = fresproot.find('.//Status//value')
	if status.text == "SingleMatch":
		try:
			destaddress = fresproot.find('.//Address/PostalAddress')
		except:
			try:
				destaddress = sresproot.find('.//Address/PostalAddress')
			except:
				destaddress = responseroot.find('.//Address/PostalAddress')
		try:
			address.find('.//District').text = destaddress.find('district').text
		except:
			address.find('.//District').text = ''
		try:
			address.find('.//FlatName').text = destaddress.find('flatName').text
		except:
			address.find('.//FlatName').text = ''
		try:
			address.find('.//FlatNumber').text = destaddress.find('flatNumber').text
		except:
			address.find('.//FlatNumber').text = ''
		try:
			address.find('.//HouseName').text = destaddress.find('houseName').text
		except:
			address.find('.//HouseName').text = ''
		try:
			address.find('.//Village').text = destaddress.find('village').text
		except:
			address.find('.//Village').text = ''
		try:
			address.find('.//HouseNumber').text = destaddress.find('houseNumber').text
		except:
			address.find('.//HouseNumber').text = ''
		address.find('.//Street').text = destaddress.find('street').text
		address.find('.//Town').text = destaddress.find('town').text
	else:
		address.find('.//HouseNumber').text = '28'
		address.find('.//Street').text = 'White Road'
		address.find('.//Town').text = 'Birmingham'
		address.find('.//Village').text = 'Quinton'
		address.find('.//PostCode').text = 'B32 2AE'
		address.find('.//FlatNumber').text = ''
		address.find('.//HouseName').text = ''
		address.find('.//District').text = ''

''' Added two functions createsubelement and updateClaims. 
The former will create element wherever specified in the xml and sets it with or without a text.
The Latter will make some changes in the Claims Node of the record.
Added By Shakeel Javed. Dated 12/15/2017
'''
def createsubelement(xmlRoot,xpath,element,text=''):
	try:
		elementcreate = xmlRoot.findall(xpath)
		for e in elementcreate:
			subelmt = ET.SubElement(e, element)
			subelmt.text = text
	except:
		print("Path not found to create sub element")
def updateClaims(xmlRoot):
	claims = xmlRoot.findall('.//Claims/row')
	for c in claims:
		timestmp = c.find('MessageTimeStamp').text
		e = '%Y%m%d%H%M%S%f'
		try:
			d = datetime.datetime.strptime(timestmp, e)
			#c.find('MessageTimeStamp').text = datetime.datetime.strftime(d, '%Y-%m-%dT%H:%M:%S.%f0+01.00')
			c.find('MessageTimeStamp').text = datetime.datetime.strftime(d, '%Y-%m-%d')
		except:
			c.find('MessageTimeStamp').text = ''
		c.find('ExpensesNetAmount').text = '0.00'
		c.find('ExpensesVATAmount').text = '0.00'
	createsubelement(xmlRoot,'.//Claims/row','SOIVehicle','Y')
	name = xmlRoot.find('Account/row')
	fname = name.find('FirstName').text
	lname = name.find('Surname').text
	createsubelement(xmlRoot,'.//Claims/row','PolicyholderName',fname+' '+lname)
	address = xmlRoot.find('Account//Addresses/row')
	pcode = address.find('PostCode').text
	createsubelement(xmlRoot,'.//Claims/row','PolicyholderPostcode',pcode)

''' 
added the function updatePolicy to update one the subelements text to 'NoAccessToOtherVehicle'
added by Shakeel Javed
dated 12/15/2017
'''
def updatePolicy(xmlRoot):
	policy = xmlRoot.findall('Policy/row')
	for p in policy:
		driver = p.findall('Drivers/row')
		for d in driver:
			d.find('UseOfOtherVehicles').text = 'NoAccessToOtherVehicle'

'''
added the function copypastenodes to copy nodes from breakdown1,2,4 and paste it to Independent node under Packages/Coverage.
added by Shakeel Javed
dated 12/20/2017
'''
def copypastenodes(xmlRoot):
	policy = xmlRoot.findall('.//Policy/row')
	for vehicles in policy:
		packages = vehicles.findall('.//Vehicle/row')
		for p in packages:
			rpackage = p.findall('.//Packages/row')
			for r in rpackage:
				try:
					if r.find('RenewalPackageName').text.replace(' ','') in ['Breakdown1','Breakdown2','Breakdown4']:
						copynode = r.find('Coverages')
						r.remove(copynode)
						try:
							rem = r.find('SelectBreakdownCover')
							r.remove(rem)
						except:
							pass
					else:
						copynode = ''
				except:
					pass
	for p in packages:
		for r in rpackage:
			try:
				if r.find('RenewalPackageName').text == 'Independent':
					icopynode = r.find('Coverages')
					r.remove(icopynode)
					rem = r.find('SelectBreakdownCover')
					r.remove(rem)
			except:
				pass
	
	createsubelement(xmlRoot,'.//Policy/row/Vehicle/row/Packages/row','IsSelected','1')	
	
	for p in packages:
		for r in rpackage:
			try:
				if r.find('RenewalPackageName').text == 'Independent':
					for c in icopynode:
						r.append(c)
					pasteloc = r.find('Coverages')
					for c in copynode.findall('row'):
						pasteloc.append(c)				
			except:
				pass
'''
added function updatephone to default phone number to a value.
added by shakeel javed
dated 12/21/2017
update: dated 01/02/2018, randomized the phone number instead of a default value.
'''	
def updatephone(xmlRoot):
	phone = xmlRoot.findall('.//PhoneNumbers/row/PhoneNumber')
	for p in phone:
		rand1=str(random.randint(0,999))
		rand2=str(random.randint(0,99))
		rand3=str(random.randint(0,99))
		rand4=str(random.randint(0,99))
		p.text = '07'+rand2+rand3+rand4+rand1
'''
Added function setvehicleattribs to conditionally set attributs of vehicles.
added by shakeel javed
dated 01/03/2017
'''
def setvehicleattribs(xmlRoot):
	vehicle = xmlRoot.findall('.//Policy/row/Vehicle/row')
	#print(vehicle)
	for v in vehicle:
		addtrack = v.find('AdditionalTrackingOrSecurityDevice')
		#print(addtrack)
		if addtrack.text == '1':
			v.find('Thatchamalarmorimmobiliser').text = 'T1'
			v.find('ProfessionallyFittedTracker').text = '9999'
		if addtrack.text == '0':
			v.find('Thatchamalarmorimmobiliser').text = 'NoSecurity'
			v.find('ProfessionallyFittedTracker').text = '0'
def main():
	print("\n############################################")
	print("### Welcome to the automated data prep tool.")
	print("############################################\n")

	print("### Please select the input file in dialog box. \n")


	inputFilename = easygui.fileopenbox()

	outputFilename = input("### Please provide requested output file name (without spaces) :")
	print("\n")

	outputFile = open('C:\AMOTOR_DP\OUTPUT\IDMF_dcmtm_'+outputFilename+'.txt','w')
	doneFile = open('C:\AMOTOR_DP\OUTPUT\IDMF_MTM.done','w')
	inputFile = open(inputFilename,'r')

	for i,line in enumerate(inputFile,1):
		try :
			idmfTree = ET.ElementTree(ET.fromstring(line))
			idmfRoot = idmfTree.getroot()
		except ParseError:
			print("### Parse exception : Policy in line ",i," is not a valid XML - policy skipped from processing")
			continue
		#print(result.getroot().tag)

		maskedFields = []
		maskedFields.append('Account/row/FirstName')
		maskedFields.append('Account/row/MiddleName')
		maskedFields.append('Account/row/Name')
		maskedFields.append('Account/row/Surname')
		maskedFields.append('Account/row/Addresses/row/FlatNumber')
		maskedFields.append('Account/row/Addresses/row/HouseName')
		maskedFields.append('Account/row/Addresses/row/Street')
		maskedFields.append('Account/row/Addresses/row/District')
		maskedFields.append('Policy/row/Drivers/row/FirstName')
		maskedFields.append('Policy/row/Drivers/row/MiddleName')
		maskedFields.append('Policy/row/Drivers/row/Surname')
		maskedFields.append('Policy/row/Drivers/row/FirstName')
		maskedFields.append('Policy/row/Drivers/row/Surname')
		maskedFields.append('Account/row/PhoneNumbers/row/PhoneNumber')
		for mf in maskedFields:
			replaceXPath(idmfRoot, mf)
		#added to replace masked data from first, last and middle name 
		replacename(idmfRoot)
		#added to get town and postcode
		town,postcode = getpostcode(idmfRoot)
		#to get the address by passing postcode via web service
		responseRoot = getadresslist(postcode)
		#update the parent XML with the received address
		replaceaddress(idmfRoot,responseRoot,town,postcode)
		#update the Claims section of the XML
		updateClaims(idmfRoot)
		#update the sub element of Policy
		updatePolicy(idmfRoot)
		replaceProfessionallyFittedTracker(idmfRoot)
		createAffinity(idmfRoot)
		createAccountAffinity(idmfRoot)
		replaceTitle(idmfRoot)
		replaceIsSelected(idmfRoot)
		createSelectAndBreakdownCoverAndRemoveCov(idmfRoot)
		#to copy and paste RenwalPackage nodes
		copypastenodes(idmfRoot)
		#to default phone number#randomize the phone number
		updatephone(idmfRoot)
		#to set vehicle attribs
		setvehicleattribs(idmfRoot)
		timestamp = str(datetime.datetime.utcnow()).replace(':', '.')
		resultLine = str(ET.tostring(idmfRoot, encoding='unicode', method='xml'))
		outputFile.write(resultLine+"\n")
		print("### Policy line number : ",i, " successfully processed.")

	outputFile.close()
	doneFile.close()
	print("\n### Output file :",'IDMF_dcmtm_'+outputFilename+'.txt'," succesfully created")
        

if __name__ == "__main__": main()


