import requests
from utils import HEADERS
from filter_data import main, update_table
import datetime

class WiproJobs:

    BASE_URL = "https://careers.wipro.com/api/jobs"
    JOB_LIMIT = 10
    LOCATION = "India"

    def __init__(self) -> None:
        self.pgNo = 1
        self.total_pages = 0
        self.all_urls = set()
        self.session = requests.Session()

    @classmethod
    def get_url(cls, page):
        return f"{cls.BASE_URL}?limit={cls.JOB_LIMIT}&page={page}&sortBy=relevance&descending=false&internal=false&location={cls.LOCATION}"

    # Write the Test case for incorrect page
    def number_of_pages(self) -> bool:
        with self.session.get(self.get_url(self.pgNo), headers=HEADERS) as response:
            if response.status_code == 200:
                data_ = response.json()
                total_jobs = data_["totalCount"]
                self.total_pages = (total_jobs // self.JOB_LIMIT) + 1
                return bool(self.total_pages)
        return False

    def filter_data(self, job: dict) -> dict:
        self.job_data = {
            "company": "Wipro",
            "job_title": job.get("title", ""),
            "job_type": job.get("employment_type", ""),
            "location": job.get("full_location", ""),
            "date_posted": job.get("posted_date", ""),
            "job_description": job.get("description", ""),
            "job_url": job.get("apply_url", ""),
            "job_id": job.get("req_id", ""),
            "websites": "https://www.wipro.com/en-IN/",
            "twitter": "https://twitter.com/Wipro",
            "experience": job.get("tags4", [""])[0] if job.get("tags4", [""])[0] != "Refer" else "",
            "added": datetime.datetime.now(),
            "updated": datetime.datetime.now(),
            "qualification": "",
            "skills": "",
        }
        return self.job_data

    def get_data(self):
        for page in range(1, self.total_pages + 1):
            with self.session.get(self.get_url(page), headers=HEADERS) as response:
                if response.status_code == 200:
                    jobdata = response.json()
                    alljobs = jobdata["jobs"]
                    for jobs in alljobs:
                        url_ = jobs["data"].get("apply_url", "")
                        data_ = self.filter_data(jobs["data"])
                        status_scraped = {"company": "Wipro", "job_url": url_, "scraped": "NS"}
                        success = main(data=status_scraped)
                        if success:
                            data_added = main(company="Wipro", data=data_)
                            if data_added:
                                update_status = {"company": "Wipro", "job_url": url_, "scraped": "S"}
                                status_update = main(data=update_status)
                                self.all_urls.add(url_)

    def remove_expired_jobs(self):
        updated = update_table("Wipro", self.all_urls)
        if updated:
            print("Table is up to date!")
            self.all_urls.clear()
        else:
            print("something went wrong while updating")

if __name__ == "__main__":
    wiproscrapper = WiproJobs()
    pages = wiproscrapper.number_of_pages()
    if pages:
        wiproscrapper.get_data()
        wiproscrapper.remove_expired_jobs()
    else:
        print("Sorry there were no jobs or something went wrong!!")
