# receives district and location objects, and returns official object
# potential function name: get_officials():

import requests
from models.official import Official
from models.district import District
from models.contact import Contact
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
        
    def get_member_details(self, bioguide_id): # replaced district
        
        try:
            url = f"https://api.congress.gov/v3/member/{bioguide_id}"
            params = {
                "format": "json",
                "API_KEY": self.api_key,
                # "currentMember":"True", --> not needed if queried by bioguide_id
            }
            
            response = requests.get(url, params=params, headers=self.headers, timeout=30)
            response.raise_for_status()  # raises an error for bad responses
            data = response.json()
            
            return data.get("member", {})
        except Exception as e:
            print(f"Error fetching congress member with bID: {bioguide_id} | {e}")
            return {}
        
    def get_congress_member(self, district):
        
        try:
            # congress member profile
            district_code = district.district_code
            state_code = district.state_code
            print(f"extracting member - state:{state_code} | district: {district_code}")
            url = f"{self.base_url}/member/{state_code}/{district_code}" 
            params = {
                "API_KEY": self.api_key,
                "format": "json",
                "currentMember": "true",
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
            bioguide_id = member.get("bioguideId", "")
            
            # member detail data
            member_details = self.get_member_details(bioguide_id)
            
            # member profile data
            firstname = member_details.get("firstName", "")
            lastname = member_details.get("lastName", "")
            fullname = member_details.get("directOrderName", "") or f"{firstname} {lastname}"
            
            # political data
            party = member.get("partyName", "")
            terms = member.get("terms", {})
            items = terms.get("item", []) #[0] replace to index zero if not most recent
            chamber = items[0].get("chamber", "House of Representatives") if items else "House of Representatives"
            
            # fetching dates
            term_start, term_end = fetch_term_dates(bioguide_id)
            
            # contact information
            contact_info = None
            address_info = member_details.get("addressInformation", {})
            if address_info:
                contact_info = Contact(
                    city=address_info.get("city"),
                    district=address_info.get("district"),
                    office_address=address_info.get("officeAddress"),
                    phone_number=address_info.get("phoneNumber"),
                    zip_code=address_info.get("zipCode"),
                    website = member_details.get("officialWebsiteUrl") or member.get("url"),
                    email = None,
                )
            
            official = Official(
                firstname=firstname,
                lastname=lastname,
                fullname=fullname,
                bioguide_id=bioguide_id,
                party=party,
                chamber=chamber,
                term_start=term_start,
                term_end=term_end,
                photo_url=None,
            )
            
            if contact_info:
                print(f"contact info found for {official.fullname}")
                print()
                print(contact_info)
                official.contact = contact_info
                
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
            if contact_info:
                print(f"contact info:\n",
                      f" office: {contact_info.office_address}\n",
                      f" phone: {contact_info.phone_number}\n",
                      f" website: {contact_info.website}\n",
                      )
            return official
        except requests.exceptions.RequestException as e:
            print(f"error calling congress api: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error in get_congress_member: {e}")
            import traceback
            traceback.print_exc()
            return None
