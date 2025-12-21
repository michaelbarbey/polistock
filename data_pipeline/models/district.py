# member's congressional area values
class District:
    def __init__(
        self, 
        district_code,
        city,
        state_name,
        state_code,
        zipcode
        ):
        self.district_code = district_code
        self.city = city
        self.state_name = state_name
        self.state_code = state_code
        self.zipcode = zipcode
        
        # state_name, district_code, city, state_code, zipcode
        # CORRECT ORDER: district, city, state_name, state_code, zipcode
        # district: ny, city:3, state name: east williston, state code: ny, zip code: 11596