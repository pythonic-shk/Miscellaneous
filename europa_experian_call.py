import requests
import xml.etree.ElementTree as ET
import re
import datetime
from openpyxl import load_workbook
from openpyxl import Workbook

pricingWorkbook = load_workbook("C:\\Users\\sebastian.radola\\Desktop\\pricing_address_val\\2nd_check_1208.xlsx")
pricingWorksheet = pricingWorkbook.active

customerTable = pricingWorksheet.get_squared_range(1,1104,26,1211)

def xstr(s):
    if s is None:
        return ''
    return str(s).strip()

def europaCall(Line1, Line2, PostCode):
    europaResponseAddress = None
    
    Line1 = xstr(Line1)
    Line2 = xstr(Line1)
    PostCode = xstr(PostCode)

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
                   <postcode>"""+PostCode+"""</postcode>
                   <!--Optional:-->
                   <street>"""+Line1+"""</street>
                   <!--Optional:-->
                   <town>"""+Line2+"""</town>

                </PostalAddress>
                <!--Optional:-->
             </AddressGetPickListRequest>
          </v01:addressGetPickListRequest>
       </soapenv:Body>
    </soapenv:Envelope>"""

    response = requests.post(url,data=body,headers=headers)

    europaResponseRoot = ET.fromstring(str(response.content)[44:-1])
    AddressGetPickListResponse = europaResponseRoot.find('{http://schemas.xmlsoap.org/soap/envelope/}Body').find('{http://www.rsagroup.co.uk/pl/duckcreek/getAddressPickList/V01}addressGetPickListResponse/AddressGetPickListResponse')

    return AddressGetPickListResponse

def getEuropaStatus(AddressGetPickListResponse):
    return AddressGetPickListResponse.find('Status/code/value').text
    
def isSingleMatch(AddressGetPickListResponse):
    return AddressGetPickListResponse.find('Status/code/value').text == 'SingleMatch'

def getPostCode(AddressGetPickListResponse):
    return AddressGetPickListResponse.find('Address/PostalAddress/postcode').text
    
def getHouseNumber(AddressGetPickListResponse):
    houseNumber = ''
    houseNumberXmlElement = AddressGetPickListResponse.find('Address/PostalAddress/houseNumber') 
    
    if houseNumberXmlElement is not None:
        houseNumber = houseNumberXmlElement.text
    
    return houseNumber
    
def getHouseName(AddressGetPickListResponse):
    houseName = ''
    houseNameXmlElement = AddressGetPickListResponse.find('Address/PostalAddress/houseName') 
    
    if houseNameXmlElement is not None:
        houseName = houseNameXmlElement.text
    
    return houseName

def getFlatName(AddressGetPickListResponse):
    flatName = ''
    flatNameXmlElement = AddressGetPickListResponse.find('Address/PostalAddress/flatName') 
    
    if flatNameXmlElement is not None:
        flatName = flatNameXmlElement.text
    
    return flatName

def getStreet(AddressGetPickListResponse):
    street = ''
    streetXmlElement = AddressGetPickListResponse.find('Address/PostalAddress/street') 
    
    if streetXmlElement is not None:
        street = streetXmlElement.text
    
    return street

    
def getLatitude(AddressGetPickListResponse):
    return AddressGetPickListResponse.find('Address/GeographicCoordinate/latitude').text

def getLongtitude(AddressGetPickListResponse):
    return AddressGetPickListResponse.find('Address/GeographicCoordinate/longitude').text
    
def formatBirthDate(BirthDate):
    BirthDate = str(BirthDate)
    return BirthDate[:4]+"-"+BirthDate[4:6]+"-"+BirthDate[6:]


def experianCall(FirstName, LastName, BirthDate, HouseNumber, HouseName, FlatName, Street, PostCode):
    
    print("Exp: #FN: ",FirstName,"#LN: ", LastName,"#DOB: ", BirthDate,"#HouseNr: ", HouseNumber,"#HouseName: ", HouseName,"#FlatName: ", FlatName,"#Street: ", Street,"#PostCode: ", PostCode)
    url="http://10.119.184.43:5001/ws/rsa.cmr.duckcreek.customer.creditdetails.get.V01.web:customerCreditDetailsGet/rsa_cmr_duckcreek_customer_creditdetails_get_V01_web_customerCreditDetailsGet_Port"
    #headers = {'content-type': 'application/soap+xml'}
    headers = {'content-type': 'text/xml'}
    body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v01="http://www.rsagroup.co.uk/pl/duckcreek/getCustomerCreditDetails/V01">
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
                  <ns0:customerGetCreditDetailsRequest xmlns:ns0="http://www.rsagroup.co.uk/pl/duckcreek/getCustomerCreditDetails/V01">
                <CustomerGetCreditDetailsRequest>
                    <Person>
                        <birthDate>"""+BirthDate+"""</birthDate>
                        <firstForename>"""+FirstName+"""</firstForename>
                        <surname>"""+LastName+"""</surname>
                        <title>
                            <value>B53 004</value>
                        </title>
                    </Person>
                    <PostalAddress>
                        <county/>
                        <district/>
                        <flatName/>
                        <flatNumber>"""+FlatName+"""</flatNumber>
                        <houseName>"""+HouseName+"""</houseName>
                        <houseNumber>"""+HouseNumber+"""</houseNumber>
                        <postcode>"""+PostCode+"""</postcode>
                        <street>"""+Street+"""</street>
                        <town/>
                    </PostalAddress>
                    <Product>
                        <code>
                            <value>NBSH</value>
                        </code>
                    </Product>
                    <TransactionStatus>
                        <code>
                            <value>QI</value>
                        </code>
                    </TransactionStatus>
                    <CoverPeriod>
                        <start>2017-07-10</start>
                    </CoverPeriod>
                    <InsuredAsset/>
                    <HistoryId>47158</HistoryId>
                    <TransactionMessageTimestamp>2017-08-15 14:49:35.647</TransactionMessageTimestamp>
                </CustomerGetCreditDetailsRequest>

                  </ns0:customerGetCreditDetailsRequest>
               </soapenv:Body>
            </soapenv:Envelope>"""

    response = requests.post(url,data=body,headers=headers)
    #print(response.content)
    experianResponseRoot = ET.fromstring(str(response.content)[44:-1])
    
    CustomerGetCreditListResponse = experianResponseRoot.find('{http://schemas.xmlsoap.org/soap/envelope/}Body').find('{http://www.rsagroup.co.uk/pl/duckcreek/getCustomerCreditDetails/V01}customerGetCreditDetailsResponse/CustomerGetCreditDetailsResponse')
    
    return CustomerGetCreditListResponse
    
def getBuildingCreditScore(CustomerGetCreditListResponse):
    return CustomerGetCreditListResponse.find('CustomerAssessment/countyCourtJudgementSummary/count').text
    
def getContentCreditScore(CustomerGetCreditListResponse):
    return CustomerGetCreditListResponse.find('CustomerAssessment/countyCourtJudgementSummary/valueCode/value').text

def perilsCall(latitude, longtitude):
    url="http://10.119.184.43:5001/ws/rsa.cmr.duckcreek.address.perilscore.get.V01.web:addressPerilScoreGet/rsa_cmr_duckcreek_address_perilscore_get_V01_web_addressPerilScoreGet_Port"
    #headers = {'content-type': 'application/soap+xml'}
    headers = {'content-type': 'text/xml'}
    body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v01="http://www.rsagroup.co.uk/pl/duckcreek/getAddressPerilScore/V01">
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
                      <v01:addressGetPerilScoreRequest>
                         <AddressGetPerilScoreRequest>
                            <GeographicCoordinate>
                                <latitude>"""+latitude+"""</latitude>
                                <longitude>"""+longtitude+"""</longitude>
                            </GeographicCoordinate>
                            <RiskAssessment>
                                <peril>
                                    <code>
                                        <value>CWF</value>
                                    </code>
                                </peril>
                            </RiskAssessment>
                            <RiskAssessment>
                                <peril>
                                    <code>
                                        <value>RWF</value>
                                    </code>
                                </peril>
                            </RiskAssessment>
                            <RiskAssessment>
                                <peril>
                                    <code>
                                        <value>SWF</value>
                                    </code>
                                </peril>
                            </RiskAssessment>
                            <RiskAssessment>
                                <peril>
                                    <code>
                                        <value>SUB</value>
                                    </code>
                                </peril>
                            </RiskAssessment>
                            <RiskAssessment>
                                <peril>
                                    <code>
                                        <value>ARS</value>
                                    </code>
                                </peril>
                            </RiskAssessment>
                            <RiskAssessment>
                                <peril>
                                    <code>
                                        <value>CRM</value>
                                    </code>
                                </peril>
                            </RiskAssessment>
                         </AddressGetPerilScoreRequest>
                      </v01:addressGetPerilScoreRequest>
                   </soapenv:Body>
                </soapenv:Envelope>"""

    response = requests.post(url,data=body,headers=headers)
    #print(response.content)
    perilsResponseRoot = ET.fromstring(str(response.content)[44:-1])    
    AddressGetPerilScoreResponse = perilsResponseRoot.find('{http://schemas.xmlsoap.org/soap/envelope/}Body').find('{http://www.rsagroup.co.uk/pl/duckcreek/getAddressPerilScore/V01}addressGetPerilScoreResponse/AddressGetPerilScoreResponse')
    
    return AddressGetPerilScoreResponse

def getPerilScoreForCode(AddressGetPerilScoreResponse, code):
    result = ''
    
    if AddressGetPerilScoreResponse is not None :
        risks = AddressGetPerilScoreResponse.findall('RiskAssessment')
        for r in risks:
            if r.find('peril/code/value').text == code:
                result = r.find('score').text
                
    return result    
 
def floodReCall(houseNumber, houseName, flatName, postCode):
    url="http://10.119.184.43:5001/ws/rsa.cmr.duckcreek.address.premisesdetails.get.V01.web.addressPremisesDetails/rsa_cmr_duckcreek_address_premisesdetails_get_V01_web_addressPremisesDetails_Port"
    #headers = {'content-type': 'application/soap+xml'}
    headers = {'content-type': 'text/xml'}
    body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:v01="http://www.rsagroup.co.uk/pl/duckcreek/getAddressPremisesDetails/V01">
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
                      <ns0:addressGetPremisesDetailsRequest xmlns:ns0="http://www.rsagroup.co.uk/pl/duckcreek/getAddressPremisesDetails/V01">
                         <AddressGetPremisesDetailsRequest>
                            <PostalAddress>
                               <flatNumber>"""+flatName+"""</flatNumber>
                               <houseName>"""+houseName+"""</houseName>
                               <houseNumber>"""+houseNumber+"""</houseNumber>
                               <postcode>"""+postCode+"""</postcode>
                            </PostalAddress>
                         </AddressGetPremisesDetailsRequest>
                      </ns0:addressGetPremisesDetailsRequest>
                   </soapenv:Body>
                </soapenv:Envelope>"""
    
    response = requests.post(url,data=body,headers=headers)
    
    floodReResponseRoot = ET.fromstring(str(response.content)[44:-1])    
    AddressGetPremisesDetailsResponse = floodReResponseRoot.find('{http://schemas.xmlsoap.org/soap/envelope/}Body').find('{http://www.rsagroup.co.uk/pl/duckcreek/getAddressPremisesDetails/V01}addressGetPremisesDetailsResponse/AddressGetPremisesDetailsResponse')
    
    return AddressGetPremisesDetailsResponse
    
def getTaxBand(AddressGetPremisesDetailsResponse):
    result = ''
    if AddressGetPremisesDetailsResponse is not None :
        xmlElement = AddressGetPremisesDetailsResponse.find('Premises/pl/home/taxBanding/value')
        if xmlElement is not None:
            result = xmlElement.text
    return result
    
def get2009Indicator(AddressGetPremisesDetailsResponse):
    result = ''
    if AddressGetPremisesDetailsResponse is not None :
        xmlElement = AddressGetPremisesDetailsResponse.find('Premises/pl/home/reinsuranceSchemeEligibilityIndicator/value')
        if xmlElement is not None:
            result = xmlElement.text
    return result    
    
def getRegion(AddressGetPremisesDetailsResponse):
    result = ''
    if AddressGetPremisesDetailsResponse is not None :
        xmlElement = AddressGetPremisesDetailsResponse.find('PostalAddress/country/value')
        if xmlElement is not None:
            result = xmlElement.text
    return result 
    
def main():
    Line1 = 'Flat C,1 Ospringe Avenue'
    Line2 = 'London'
    PostCode = 'NW5 2JD'

    adres = europaCall(Line1, Line2, PostCode)
           
    for c in customerTable:
        print("TC :",c[4].value )
        correspondence_line1 = c[9].value
        correspondence_line2 = c[10].value
        correspondence_postcode = c[11].value
       
        risk_line1 = c[12].value
        risk_line2 = c[13].value
        risk_postcode = c[14].value
       
        firstName =  c[7].value
        lastName = c[6].value
        birthDate = formatBirthDate(c[8].value)
        corrPostCode = c[11].value
        corrHouseNumber = ''
        corrHouseName = ''
        corrFlatName = ''
        corrStreet = ''
        
        riskPostCode = c[14].value
        riskHouseNumber = ''
        riskHouseName = ''
        riskFlatName = ''
        riskLatitude = ''
        riskLongtitude = ''
        
        cor_res = europaCall(correspondence_line1,correspondence_line2,correspondence_postcode)
        risk_res = europaCall(risk_line1,risk_line2,risk_postcode)
       
        if isSingleMatch(cor_res):
            corrPostCode = getPostCode(cor_res)
            corrHouseNumber = getHouseNumber(cor_res)
            corrHouseName = getHouseName(cor_res)
            corrFlatNumber = getFlatName(cor_res)
            corrStreet = getStreet(cor_res)
                
        if isSingleMatch(risk_res):
            riskPostCode = getPostCode(risk_res)
            riskHouseNumber = getHouseNumber(risk_res)
            riskHouseName = getHouseName(risk_res)
            riskFlatName = getFlatName(risk_res)
            riskLatitude = getLatitude(risk_res)
            riskLongtitude = getLongtitude(risk_res)
        
        experianScores = experianCall(firstName,lastName,birthDate,corrHouseNumber, corrHouseName, corrFlatName, corrStreet, corrPostCode)
        
        perilsScores = perilsCall(riskLatitude, riskLongtitude)
        floodReScores = floodReCall(riskHouseNumber, riskHouseName, riskFlatName, riskPostCode)
       
        c[0].value = getEuropaStatus(cor_res)
        c[1].value = getEuropaStatus(risk_res)
        c[2].value = corrHouseNumber
        c[3].value = riskHouseNumber
        c[18].value = getBuildingCreditScore(experianScores)
        c[19].value = getContentCreditScore(experianScores)
        c[20].value = getPerilScoreForCode(perilsScores,'CWF')
        c[21].value = getPerilScoreForCode(perilsScores,'RWF')
        c[22].value = getPerilScoreForCode(perilsScores,'SWF')
        c[23].value = getTaxBand(floodReScores)
        c[24].value = get2009Indicator(floodReScores)
        c[25].value = getRegion(floodReScores)
#        except (AttributeError, TypeError):
#            if AttributeError:
#                print ("Attribute Error for TC: ",c[4].value)
#            elif TypeError:
#                print ("Type Error for TC: ",c[4].value)
#            #print(AttributeError)
#            #print(TypeError)
#            pass
        
       
    timestamp = str(datetime.datetime.utcnow()).replace(':','.')
    pricingWorkbook.save("C:\\Users\\sebastian.radola\\Desktop\\pricing_address_val\\""1208""+"+timestamp+"_check_300_pack.xlsx")
    
if __name__ == "__main__": main()
