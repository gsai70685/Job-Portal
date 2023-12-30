import requests
from utils import headers, cookies, prod_headers
from filter_data import main
import datetime
import re


class AppleJobScraper:

    def __init__(self) -> None:
        self.url = 'https://jobs.apple.com/api/v1/search/page?location=india-INDC'
        self.totalPages = 0
        self.session = requests.Session()

    def calculate_total_pages(self) -> int:
        response = self.session.get(self.url, headers=headers,
                                    cookies=cookies)
        if response.status_code == 200:
            data = response.json()
            total_jobs = data.get("totalRecords","")
            if total_jobs:
                jobs_on_one_page  = 20
                self.totalPages = (int(total_jobs) // jobs_on_one_page)+1
            return True
        else:
            return False

    def get_job_data(self, apiurl, normalurl) -> dict:
        try:
            headers["referer"] = normalurl
            response = self.session.get(apiurl, headers=prod_headers,
                                        cookies=cookies)
            if response.status_code == 200:
                job = response.json()
                job_data = dict()
                job_data["company"] = "Apple"
                job_data["job_title"] = job["postingTitle"]
                job_data["skills"] = job.get("preferredSkills","")
                job_data["job_id"] = job["id"]
                job_data["experience"] = ""
                qualifications = job.get("keyQualifications", "")
                if qualifications:
                    pattern = re.compile(r'\b\d+(\.\d+)?\s*-?\s*\d+(\.\d+)?\s*years\b')
                    search_ = pattern.search(qualifications.strip().replace("\n",""))
                    if search_:
                        job_data["experience"] = search_.group()
                job_data["job_type"] = job["jobType"]
                locations = job["locations"]
                city = locations[0].get("city", "")
                country = locations[0]["countryName"]
                loc = f"{city} {country}"
                job_data["location"] = loc
                job_data["date_posted"] = job["postingDateMeta"]
                job_data["job_description"] = job["description"]
                job_data["twitter"] = "https://twitter.com/Apple"
                job_data["websites"] = "https://www.apple.com/in/"
                job_data["qualification"] = job.get("educationAndExperience","")
                job_data["job_url"] = normalurl
                job_data["added"] = datetime.datetime.now()
                job_data["updated"] = datetime.datetime.now()
                return job_data
        except Exception as e:
            print("Error occured in fetching job data: ", e)

    def iterate_over_data(self):
        for pagenumber in range(1,self.totalPages+1):
            if pagenumber == 1:
                url = self.url
            else:
                url  = f"{self.url}&page={pagenumber}"
            response = self.session.get(url, headers=headers,
                                        cookies=cookies)
            if response.status_code == 200:
                data = response.json()
                all_jobs = data["searchResults"]
                for job in all_jobs:
                    transformed_title = job["transformedPostingTitle"]
                    job_id = job["id"].split("-")[-1].strip()
                    team_id = job["team"]["teamCode"]
                    job_url = f"https://jobs.apple.com/en-in/details/{job_id}/{transformed_title}?team={team_id}"
                    scrapped_data = {"company":"Apple", "job_url":job_url, "scraped":"NS"}
                    scraped_result = main(data=scrapped_data)
                    if scraped_result:
                        job_api_url = f"https://jobs.apple.com/api/role/detail/{job_id}?languageCd=en-in"
                        data_ready = self.get_job_data(job_api_url, job_url)
                        if data_ready:
                            data_added = main(company="Apple", data=data_ready)
                            if data_added:
                                updated_scrapped_data = {"company":"Apple", "job_url":job_url, "scraped":"S"}
                                updated_scraped_result = main(data=updated_scrapped_data)
                    print("Job Added")
                    data_ready.clear()

if __name__ == "__main__":
    applescrapper = AppleJobScraper()
    signal = applescrapper.calculate_total_pages()
    if signal:
        applescrapper.iterate_over_data()



