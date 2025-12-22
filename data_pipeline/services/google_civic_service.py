import requests
#import urllib.parse
from models.district import District
import os
from dotenv import load_dotenv

load_dotenv()

class GoogleCivicDistrictValue:
    
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_CIVIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "GOOGLE_CIVIC_API_KEY not found in environment variables. "
                "Please add it to your .env file."
            )
        self.google_url = "https://civicinfo.googleapis.com/civicinfo/v2/divisionsByAddress"
        self.session = requests.Session()
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/605.1.15 (KHTML, like Gecko) "
                "Version/26.1 Safari/605.1.15"
            ),
            "Accept-Language": "en-US,en;q=0.9",
        }
        
        
        #self.base_url = "https://civicinfo.googleapis.com/civicinfo/v2/representatives"
        # to debug
        print(f"Google Civic API Key loaded: {self.api_key[:10]}...")
    
    def _fetch_ocd_id(self, street, city, state_name, zipcode):
        
        try:
            address = f"{street},{city},{state_name},{zipcode}"
            
            params = {
                "key": self.api_key,
                "address": address
            }
            
            if not self.api_key:
                raise ValueError(
                    "GOOGLE_CIVIC_API_KEY not found in environment variables. "
                    "Please add it to your .env file."
                )
            
            print(f"Calling Google Civic API with address: {address}")
            print(f"API Key (first 10 chars): {self.api_key[:10]}")
            
            response = requests.get(self.google_url, params=params)
            
            print(f"Response status: {response.status_code}")
            
            if response.status_code != 200:
                print(f"Error response: {response.text}")
                return None
            
            data = response.json()
            print(f"Response data: {data}")
            
            # Parse divisions to find district
            divisions = data.get('divisions', {})
            
            district_code = None
            state_code = None
            
            for ocd_id in divisions.keys():
                # Example: "ocd-division/country:us/state:ny/cd:3"
                if '/cd:' in ocd_id:
                    district_code = ocd_id.split('/cd:')[-1]
                if '/state:' in ocd_id:
                    state_code = ocd_id.split('/state:')[-1].split('/')[0].upper()
            
            if not district_code:
                print("Could not find district code in response")
                return None
            
            print(f"Found district: {district_code}, state: {state_code}")
            
            district = District(
                district_code=district_code,
                city=city,
                state_name=state_name,
                state_code=state_code or "NY",
                zipcode=zipcode
            )
            
            return district
            
        except Exception as e:
            print(f"Error in _fetch_ocd_id: {e}")
            import traceback
            traceback.print_exc()
            return None
        
        # street = street
        # city = city
        # state_name = state_name
        # zipcode = zipcode
        
        # full_address = f"{street},{city},{state_name},{zipcode}"
        # params = {
        #     "key": self.api_key,
        #     "address": full_address
        # }
        
        # try:
        #     google_response = requests.get(self.google_url, params=params)
        #     google_response.raise_for_status()
        #     google_data = google_response.json()
            
        #     found_state = None
        #     found_district = None
            
        #     # trying to find the ocd id, which the district id
        #     if "divisions" in google_data:
        #         for ocd_id in google_data["divisions"].keys():
        #             if "/cd:" in ocd_id:
        #                 parts = ocd_id.split('/')
        #                 for part in parts:
        #                     if part.startswith("state:"):
        #                         found_state = part.split(":")[1].upper()
        #                     if part.startswith("cd:"):
        #                         found_district = part.split(":")[1]
        #                         # district -> updated variable name
        #                         district = District(
        #                             city = city,
        #                             state_name = state_name,
        #                             state_code = found_state,
        #                             district_code = found_district,
        #                             zipcode = zipcode
        #                         ) # state_name, district_code, city, state_code, zipcode
        #                         # current debugger, will create a logs system later
        #                         # print(
        #                         #     f"district: {address.district_code}\n"
        #                         #     f"city: {address.city}\n"
        #                         #     f"state name: {address.state_name}\n"
        #                         #     f"state code: {found_state}\n"
        #                         #     f"zipcode: {address.zipcode}\n"
        #                         #     )
        #                         return district
        #                     # state_name, district_code, city, state_code, zipcode
        #     if not found_district:
        #         print(f"no representative found on zip code: {zipcode}")
        #         return
            
        # except Exception as e:
        #     print(f"error: {e}")
        