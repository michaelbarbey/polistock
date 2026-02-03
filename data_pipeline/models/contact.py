'''
building official's contact information
'''

class Contact:
    def __init__(self,
                 city = None,
                 district = None,
                 office_address = None,
                 phone_number = None,
                 zip_code = None,
                 website = None,
                 email = None
    ):
        self.city = city
        self.district = district
        self.office_address = office_address
        self.phone_number = phone_number
        self.zip_code = zip_code
        self.website = website
        self.email = email
        
    def to_dict(self):
        return {
            "city": self.city,
            "district": self.district,
            "office_address": self.office_address,
            "phone_number": self.phone_number,
            "zip_code": self.zip_code,
            "website": self.website,
            "email": self.email
        }
        
    @classmethod
    def from_api_data(cls, api_data):
        return cls(
            city = api_data.get("city"),
            district = api_data.get("district"),
            office_address = api_data.get("office_address"),
            phone_number = api_data.get("phone_number"),
            zip_code = api_data.get("zip_code"),
            website = api_data.get("website") or api_data.get('url'),
            email = api_data.get("email")
        )
        
    def __repr__(self):
        return f"Contact(city={self.city}, district={self.district}, office_address={self.office_address}, phone_number={self.phone_number}, zip_code={self.zip_code}, website={self.website}, email={self.email})"