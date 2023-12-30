from fake_useragent import UserAgent

useragent = UserAgent()

HEADERS = {
    "authority": "careers.wipro.com",
    "method": "GET",
    "path": "/api/jobs?limit=100&page=18&sortBy=relevance&descending=false&internal=false",
    "scheme": "https",
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-GB,en;q=0.8",
    "Cookie": "i18n=en-US; searchSource=external; session_id=aa3b43fb-043a-418e-88b1-d48858ee936b; jasession=s%3AH7ut18C3RRL0EN9Opj3GUMYf2N825g90.Sii1zcWmUT9XW%2FzGfAko8ktfANXeVHyv%2FV5YLJs%2FuBw; jrasession=603e5d8b-a6e9-4c15-9274-4278bc933356",
    "Referer": "https://careers.wipro.com/careers-home/jobs?limit=100&page=18",
    "Sec-Ch-Ua": '"Brave";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    "Sec-Ch-Ua-Mobile": "?1",
    "Sec-Ch-Ua-Platform": '"Android"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Gpc": "1",
    "User-Agent": useragent.random
}