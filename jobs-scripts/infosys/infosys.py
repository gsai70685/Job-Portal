from utilss import HEADERS
from filter_data import main
import requests
import datetime
class InfosysJobs():

    def __init__(self):
        self.session = requests.Session()
        self.total_pages = None
        self.url = "https://intapgateway.infosysapps.com/careersv2/search/intapjbsrch/getCareerSearchJobs?sourceId=1,21&searchText=ALL"

    def filter_data(self, job):
        job_data = dict()
        job_data["company"] = "Infosys Limited"
        job_data["job_title"] = job["postingTitle"]
        job_data["skills"] = job["preferredSkills"]
        job_data["job_id"] = job["postingId"]
        experience  = f'{job["minExperienceLevel"]} - {job["maxExperienceLevel"]}'
        job_data["experience"] = experience
        job_data["job_type"] = ""
        job_data["location"] = job["location"]
        job_data["date_posted"] = job["createdOn"]
        job_data["job_description"] = job["rolesResponsibilities"]
        job_data["twitter"] = "https://twitter.com/Infosys"
        job_data["websites"] = "https://www.infosys.com/"
        job_data["qualification"] = job["educationalRequirement"]
        job_data["job_url"] = f'https://career.infosys.com/jobdesc?jobReferenceCode={job["referenceCode"]}'
        job_data["added"] = datetime.datetime.now()
        job_data["updated"] = datetime.datetime.now()
        return job_data

    def get_data(self):
        response = requests.get(self.url, headers=HEADERS)
        if response.status_code == 200 and response.json():
            all_jobs = response.json()
        for job_ in all_jobs:
            url_ = f'https://career.infosys.com/jobdesc?jobReferenceCode={job_["referenceCode"]}'
            scraped_status = {"company":"Infosys Limited", "job_url":url_, "scraped":"NS"}
            result = main(data=scraped_status)
            if result:
                jobdata = self.filter_data(job_)
                added = main(company="Infosys Limited", data=jobdata)
                if added:
                    scraped_status = {"company":"Infosys Limited", "job_url":url_, "scraped":"S"}
                    status_updates = main(data=scraped_status)
            print("Job added")
            # print(self.job)
            jobdata.clear()

if __name__ == "__main__":
    Infosys_scrapper = InfosysJobs()
    Infosys_scrapper.get_data()