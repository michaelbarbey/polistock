# receives district and location objects, and returns official object
# potential function name: get_officials():

import requests
from models.official import Official
from models.district import District
from utils.date_helpers import fetch_term_dates
from config.settings import CONGRESS_API_KEY, CONGRESS_API_URL, USER_AGENT

# in the module, this code will need to import Official class from the above code

class CongressMemberProfile: #re-factored
    
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            "User-Agent": USER_AGENT,
            "Accept-Language": "en-US,en;q=0.9",
        }
        self.api_key = CONGRESS_API_KEY
        self.base_url = CONGRESS_API_URL
        
    def get_congress_member(self, district):
        
        try:
            district_code = district.district_code
            state_code = district.state_code
            print(f"extracting member - state:{state_code} | district: {district_code}")
            
            #url = f"{self.base_url}{state_code}/member/{district_code}?api_key={self.api_key}"
            url = f"{self.base_url}/member/{state_code}/{district_code}"
            
            params = {
                "API_KEY": self.api_key,
                "format": "json",
                "currentMember":"True",
                "limit": 3
            }
            response = requests.get(url, params=params, headers=self.headers, timeout=30)
            response.raise_for_status()  # raises an error for bad responses
            data = response.json()
            
            if "members" not in data or not data["members"]:
                print(f"no members found in state: {state_code} | district: {district_code}")
                return None
            
            members = data["members"]
            print(f"members found: {len(members)} | state: {state_code}:\n")
            
            # current representative
            member = members[0]
            name = member.get("name", "")
            bioguide_id = member.get("bioguideId", "")
            
            # political data
            party = member.get("partyName", "")
            terms = member.get("terms", {})
            items = terms.get("item", []) #[0] replace to index zero if not most recent
            chamber = items[0].get("chamber", "House of Representatives") if items else "House of Representatives"
            
            # fetching dates
            term_start, term_end = fetch_term_dates(bioguide_id)
            
            # fix name structure
            name_parts = name.split(", ")
            lastname = name_parts[0] if len(name_parts) > 0 else name
            firstname = name_parts[1] if len(name_parts) > 1 else name
            
            official = Official(
                firstname=firstname,
                lastname=lastname,
                fullname=name,
                bioguide_id=bioguide_id,
                party=party,
                chamber=chamber,
                term_start=term_start,
                term_end=term_end,
                photo_url=None
            )
            official.officials_district(district)
            print()
            print(f"member: {official.fullname}\n",
                  f"first name: {official.firstname}\n",
                  f"last name: {official.lastname}\n",
                  f"bioguide_id: {official.bioguide_id}\n",
                  f"party: {official.party}\n",
                  f"chamber: {official.chamber}\n",
                  f"district: {district.district_code}\n",
                  f"city: {district.city}\n",
                  f"state name: {district.state_name}\n",
                  f"state code: {district.state_code}\n",
                  f"zipcode: {district.zipcode}\n",
                  f"start term: {official.term_start}\n",
                  f"end term: {official.term_end}\n",)
            return official
        except requests.exceptions.RequestException as e:
            print(f"error calling congress api: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error in get_congress_member: {e}")
            import traceback
            traceback.print_exc()
            return None