import requests
import yaml

# LEG_CURRENT_URL

LEGISLATORS_CURRENT_URL = (
    "https://raw.githubusercontent.com/"
    "unitedstates/congress-legislators/main/"
    "legislators-current.yaml"
)

def fetch_term_dates(bioguide_id):
    # each representative is assigned a bioguide id
    # function will return a representative's start/end term date
    
    # downloading yaml file
    try:
        response = requests.get(LEGISLATORS_CURRENT_URL, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"})
        response.raise_for_status() # error handling for request
    except Exception as e:
        print(f"Error loading term-dates YAML: {e}")
        return None, None
    
    # parsing yaml data
    try:
        data = yaml.safe_load(response.text)
    except Exception as e:
        print(f"Error parsing YAML: {e}")
        return None, None
    
    # matchin input with bioguide_id parameter
    for member in data:
        ids = member.get('id', {})
        if ids.get("bioguide") == bioguide_id:
            terms = member.get('terms', [])
            if terms:
                current_term = terms[-1]  # assuming the last term is the current one
                start = current_term.get("start")
                end = current_term.get("end")
                return start, end
    return {"term_start": None, "term_end": None} # return None is match is not found.