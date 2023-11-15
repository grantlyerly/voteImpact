import requests
from app.methods.config import API_KEY

def queryRep(address):
    """
    Queries Google API to return representative info based on an address.
    """
    
    response = requests.get(f'https://www.googleapis.com/civicinfo/v2/representatives?address={address}&key={API_KEY}')
    
    if response.status_code == 200:
        return response.json()

    else:
        return None


def checkCD(data):
    """
    Simple function to identify if returned divion data contains address's congressional district.
    """

    for key in data['divisions'].keys():
        if "/cd:" in key: 
            return key
    
    return None


def voteInfo_address(zip:int, line1:str="", city:str="", state:str=""):
    """
    Basic function to return usable information about an address's voting divisions. 
    Can take a full address or pieces of one.

    Returns a dictionary {'code':, 'data':} 
    
    Codes designations: 2 = All info found | 1 = No congressional district | 0 = No info at all.

    Data Package: {state:, cd:}
    """
    
    # Set up return packet:
    ret = {'code':0, 'data':{}}

    # Clean up address
    if len(line1)>1:
        line1 = line1 + ". "
    if len(city)>1:
        city = city + ", "
    if len(state)>1:
        state = state + " "
    fullAddress: str = line1 + city + state + str(zip)
    
    # Query API
    data = queryRep(fullAddress)

    # Check for data
    if data:

        # Check for Congressional District Data
        code = 0
        cdString = checkCD(data)
        if cdString:
            code = 2
        else:
            code = 1
        
        ret['code'] = code
        
        """
        Parse data for use elsewhere. 
        Currently, tool will only use state and congressional district (hopefully expanded in future)
        Different processes for whether district is identifiable.
        """
        if code == 2:
            parts = cdString.split('/')
            st = parts[2].split(':')[1].upper()
            cd = int(parts[3].split(':')[1])

            retData = {'state':st, 'cd':cd}
        
        elif code ==1:
            divs = data['divisions'].keys()
            for key in divs:
                if "/state:" in key:
                    parts = key.split('/')
                    st = parts[2].split(':')[1].upper()

                    retData = {'state':st}
                    break

        # Package final ret
        ret['data']=retData
        return ret

    # Return code 0
    return ret

"""
Initial Testing Code

address = '27514'

response1 = requests.get(f'https://www.googleapis.com/civicinfo/v2/representatives?address={address}&key={API_KEY}')

# If the request was successful, response status code will be 200
if response1.status_code == 200:
    data = response1.json()  # Parse the data from the response

    k = data['divisions'].keys()
    ret = False
    for key in k:
        if "/cd:" in key: 
            print(True)
            ret = True
    if not ret:
        print(False)
    

else:
    print('Access Failed')
"""