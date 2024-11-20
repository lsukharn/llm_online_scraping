import os 
import requests

from dotenv import load_dotenv

load_dotenv()

def scrape_linkedin_profile(linkedin_profile_url: str = None, mock: bool = False):
    """scrape information from Linkedin profiles,
    Manually scrape the information from the Linkedin profiles
    """
    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/emarco177/0d6a3f93dd06634d95e46a2782ed7490/raw/78233eb934aa9850b689471a604465b188e761a0/eden-marco.json"
        # linkedin_profile_url = "https://gist.github.com/lsukharn/395adff66107162db6afe1c37b1a87de"
        response = requests.get(linkedin_profile_url,
                                timeout=10)
    else:
        headers = {'Authorization': f'Bearer {os.environ.get("PROXYCURL_API_KEY")}'}
        api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'

        response = requests.get(api_endpoint,
                                params={'url': linkedin_profile_url},
                                headers=headers)
        
    data = response.json()
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None)
        and k not in ["people_also_viewed", "certifications"]
    }
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")

    return data


if __name__ == "__main__":
    print(scrape_linkedin_profile(mock=True))