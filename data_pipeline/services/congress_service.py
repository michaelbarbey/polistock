# receives district and location objects, and returns official object
# potential function name: get_officials():
import requests
import json
from models.official import Official
from models.district import District
from utils.date_helpers import fetch_term_dates
from config.settings import CONGRESS_API_KEY, CONGRESS_API_URL, USER_AGENT

# in the module, this code will need to import Official class from the above code

class CongressMemberProfile(Official): # -> may not need the Official parameter
    
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            "User-Agent": USER_AGENT,
            "Accept-Language": "en-US,en;q=0.9",
        }
        self.api_key = CONGRESS_API_KEY
        self.base_url = CONGRESS_API_URL
        
    def get_congress_member(self, address):
        
        district_code = address.district_code
        city = address.city
        state_name = address.state_name
        state_code = address.state_code
        zipcode = address.zipcode
        
        url = f"{self.base_url}{state_code}/{district_code}?api_key={self.api_key}"
        
        params = {
        "API_KEY": self.api_key,
        "format": "json",
        "currentMember":"True",
        "limit": 3
        }
        
        try:
            response = requests.get(url, params=params, headers=self.headers)
            
            response.raise_for_status()  # raises an error for bad responses
            data = response.json()
        
            if "members" in data:
                members = data["members"]
                print(f"FOUND {len(members)} members for {state_code}:\n")
                for  member in members:
                    name = member.get("name")
                    bioguide_id = member.get("bioguideId")
                    party = member.get("partyName")
                    terms = member.get("terms")
                    items = terms.get("item")[0]
                    chamber = items.get("chamber")
                    term_start, term_end = fetch_term_dates(bioguide_id)
                    
                    official = Official(
                        firstname=name.split()[1],
                        lastname=name.split()[0],
                        fullname=name,
                        bioguide_id=bioguide_id,
                        party=party,
                        chamber=chamber,
                        term_start=term_start,
                        term_end=term_end,
                        photo_url=None,
                    )
                    official.officials_district(district_code, city, state_name, state_code, zipcode)
                    
                    print(f"member: {official.fullname}\n",
                          f"first name: {official.firstname}\n",
                          f"last name: {official.lastname}\n",
                          f"bioguide_id: {official.bioguide_id}\n",
                          f"party: {official.party}\n",
                          f"chamber: {official.chamber}\n",
                          f"district: {official.districts[0].district_code}\n",
                          f"city: {official.districts[0].city}\n",
                          f"state name: {official.districts[0].state_name}\n",
                          f"state code: {official.districts[0].state_code}\n",
                          f"zipcode: {official.districts[0].zipcode}\n",
                          f"start term: {official.term_start}\n",
                          f"end term: {official.term_end}\n",)
                    return official
            else:
                print("No members found")
        except requests.exceptions.RequestException as e:
            print(f"Error loading: {e}")