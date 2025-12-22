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
    
    # for debugging
    def __repr__(self):
        return (f"District(district_code={self.district_code!r}, "
                f"city={self.city!r}, state={self.state_name!r})")
    
    # quick output
    def __str__(self):
        return f"{self.city}, {self.state_name} - District {self.district_code}"