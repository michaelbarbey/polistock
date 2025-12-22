# congress terms
# fetches congress start and end term dates from the github repo 

from config.settings import LEG_CURRENT_URL
from datetime import datetime
import yaml
import requests

# Legislators YAML file
LEG_CURRENT_URL = (
    "https://raw.githubusercontent.com/"
    "unitedstates/congress-legislators/main/"
    "legislators-current.yaml"
)

def fetch_term_dates(bioguide_id):
    
    # with the bioguide parameter, the function will return the start and end dates of the congress term

    # downloding the YAML File 
    try:
        response = requests.get(LEG_CURRENT_URL, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"})
        response.raise_for_status()  # raises an error for bad responses
    except Exception as e:
        print(f"Error loading term-dates YAML: {e}")
        return None, None
    
    # parsing data
    try:
        data = yaml.safe_load(response.text)
    except Exception as e:
        print(f"Error parsing YAML: {e}")
        return None, None

    # findinf the match entry from the bioguide_id parameter
    for member in data:
        ids = member.get('id', {})
        if ids.get("bioguide") == bioguide_id:
            # extracting the terms
            terms = member.get('terms', [])
            if terms:
                # the last item in the list os the current term
                current_term = terms[-1]
                start = current_term.get("start")
                end   = current_term.get("end")
                return start, end
                
    return {"term_start": None, "term_end": None}  # returns None if no match is found

def format_date(date_str, input_format="%d %b %Y", output_format="%Y%m%d"):
    """
    Convert date from one format to another.
    
    Args:
        date_str (str): Date string to convert (e.g., "2 Dec 2025")
        input_format (str): Format of input date
        output_format (str): Desired output format
        
    Returns:
        str: Formatted date string (e.g., "20251202")
    """
    try:
        date_obj = datetime.strptime(date_str, input_format)
        return date_obj.strftime(output_format)
    except ValueError:
        return date_str