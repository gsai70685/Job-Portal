import requests
from bs4 import BeautifulSoup
import pymongo

HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-GB,en;q=0.9',
    'Cache-Control': 'max-age=0',
    'Cookie': 'SEARCH_SAMESITE=CgQItZkB; SOCS=CAESHAgBEhJnd3NfMjAyMzA2MTItMF9SQzIaAmZpIAEaBgiAzK6kBg; NID=511=HLGsk8RqncJJYPCpsBBxbOsSNuGUSh9tzHrnVin-qJTXtPLZYgo8c41JJKkJPIZBRz1Z7R9qxiHeKRzMsrFndrA8W6NmgP6Km5n46nBfQYeb63jSNuvLUZo8gXbyrmD7hSC8NHL9X8XIDW7ka5_Fa4SpkvCUrC6XjwIUdqwefpV71b1TovYNJcZrhLU5b6p4wwc0uKPw8upkPiSKXcbjAqzfUPZCBlzQkugO74ZNgN3cKAS6Slgljmy59BA3P_-723siWEK3ImkKiXOaJmU-YDIsI6PH2TyiyvrnhmN2LuJEiyDZIbA7fIuiQM9UUmSc4End3x7b0fcLjBDek758tnmuRMHOd6hpvbw2isawSYfBYgPCanPA7m7R5QoPxa6gcpoSsiyspXdNAVjpVqbf5-n12aI3qnl-bjUFGg5ola4gLyR23ySWmuL_AzgXju6kUxQrT3VyKD8frNEuecvYpBLFjOX1VX228rLdfffyp2I6h5ZyPZtSFbKanVWEGTMDdWebwiRL4AyheZxXTQMHCr_6id_LORkGLaZXew792gS5_QLjVd_U-kCszxeH1FwvBpbfKYNICLsxqBeI4gIofP3RZ0qQs-3_qnz2-V-s0AvRSjcQ_a6VFjkj_WmxZVBK2a0NdqftRufN1PKsiVBWrXAP7-ZkqacSj79DpepIyTvb9UMhx_FDMWwtsdGAvtT3WKs; SID=dQi5n_7B9L-qcdauTsLWQQ_Npa7DVHhInKFsZXlFsGECv_xMYwEaHpc_zrz9RjciX3-Q-A.; __Secure-1PSID=dQi5n_7B9L-qcdauTsLWQQ_Npa7DVHhInKFsZXlFsGECv_xMdckEk64GM6eIJ2VBODt3fg.; __Secure-3PSID=dQi5n_7B9L-qcdauTsLWQQ_Npa7DVHhInKFsZXlFsGECv_xMS8a1e8PzVmwwHHzw-wMnYg.; HSID=AyTT889LdTrOKc7cO; SSID=AOSDMdb9YzyUrOtvU; APISID=QZMNRnTWqsGj3jc9/A1WgH5HugyAb8bw_u; SAPISID=PkUxWDGZ3SKWf1RP/AkOHYpoMV83KPjKxI; __Secure-1PAPISID=PkUxWDGZ3SKWf1RP/AkOHYpoMV83KPjKxI; __Secure-3PAPISID=PkUxWDGZ3SKWf1RP/AkOHYpoMV83KPjKxI; OTZ=7318688_34_34__34_; 1P_JAR=2023-12-04-16; AEC=Ackid1RQ60mp6UkJCKOCSHcB3yHlSeC9KH2LnNV-MsnAqRYQTtn2KP1Lfg; __Secure-ENID=16.SE=XnNmv2nMxObA7IYK2ABjO_qmZ582kohKRs2y3En7Pj3Hccws0cPcZ80UjJfagi_xkWZ9kULIXpAtZ_y8e7y2s178OGRJYZic6Cj8Ni4gS8XTOUcuHJD6YAsGF0A4uMdyWS7fMfnQNOuQKw7OljNkaUriDQUOrEsEATC3He-v99K2z8S-nmbBd2Y7fBzfDhkQG8enjPGCjot2GenAKO6tdiKgGOzSOoBkUzr48N0TxxtFADuflZ59h3BIlnblYUze3krdzb09lW1Z98QgypzIhO7ILrwo9dsULNpMJmgPyNQjMyAPe8lQEmDaZIN3C_t3kwGGI38ePUiC-Mnw0LsOAbEmqnPhpKEEUatqSc4kKhM_yTFoHRbbSM87Bw; __Secure-1PSIDTS=sidts-CjEBPVxjSqFMyigk3bqFJtLqQ_-utpjdKPbYsWD3kq1QO0ut5gmMFgmRC9C9Au14uPvQEAA; __Secure-3PSIDTS=sidts-CjEBPVxjSqFMyigk3bqFJtLqQ_-utpjdKPbYsWD3kq1QO0ut5gmMFgmRC9C9Au14uPvQEAA; SIDCC=ACA-OxPOqwtheePVRcotUAr-mj9yVKHfXv5rQJXBybUOGqYYd7ocWKncac89nfsIHNUdp4ebOJ5l; __Secure-1PSIDCC=ACA-OxPVwGR63iMGuzY5tovqIfPU5Ew_BlF9oI6lB01QQ-NsqcE0Sy-zeMo-4XYDIp_vrqpryxuW; __Secure-3PSIDCC=ACA-OxPUudFzJhCslkHciYCLaA03rIuOsfsEhnrX9uDZrnLd3dQUa4zt5fUJN2VWdtMAbOdQJwE',
    'Sec-Ch-Ua': '"Brave";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'Sec-Ch-Ua-Mobile': '?1',
    'Sec-Ch-Ua-Model': '"Nexus 5"',
    'Sec-Ch-Ua-Platform': '"Android"',
    'Sec-Ch-Ua-Platform-Version': '"6.0"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Sec-Gpc': '1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36'
}

client = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = client["Rivan-Jobs"]
gjobs = mydb["google-jobs"]

class FullTime:
    def __init__(self) -> None:
        self.pgNo = 1
        self.full_time_url = "https://www.google.com/about/careers/applications/jobs/results?employment_type=FULL_TIME&page={}".format(self.pgNo)

    def alter_url(self):
        self.pgNo = self.pgNo + 1
        self.full_time_url = "https://www.google.com/about/careers/applications/jobs/results?employment_type=FULL_TIME&page={}".format(self.pgNo)

    def get_url(self):
        return self.full_time_url

class PartTime:
    def __init__(self) -> None:
        self.pgNo = 1
        self.part_time_url = "https://www.google.com/about/careers/applications/jobs/results?employment_type=PART_TIME&page={}".format(self.pgNo)

    def alter_url(self):
        self.pgNo += 1
        self.part_time_url = "https://www.google.com/about/careers/applications/jobs/results?employment_type=PART_TIME&page={}".format(self.pgNo)

    def get_url(self):
        return self.part_time_url

class Intern:
    def __init__(self) -> None:
        self.pgNo = 1
        self.intern_url = "https://www.google.com/about/careers/applications/jobs/results?employment_type=INTERN&page={}".format(self.pgNo)

    def alter_url(self):
        self.pgNo += 1
        self.intern_url = "https://www.google.com/about/careers/applications/jobs/results?employment_type=INTERN&page={}".format(self.pgNo)

    def get_url(self):
        return self.intern_url

class Temporary:
    def __init__(self) -> None:
        self.pgNo = 1
        self.temporary_url = "https://www.google.com/about/careers/applications/jobs/results?employment_type=TEMPORARY&page={}".format(self.pgNo)

    def alter_url(self):
        self.pgNo += 1
        self.temporary_url = "https://www.google.com/about/careers/applications/jobs/results?employment_type=TEMPORARY&page={}".format(self.pgNo)

    def get_url(self):
        return self.temporary_url

class GoogleJobs:
    def __init__(self) -> None:
        self.ft = FullTime()
        self.pt = PartTime()
        self.int = Intern()
        self.tmp = Temporary()

        self.obj = dict()

    def get_data(self):
        for i in range(4):
            if i == 0:
                self.work_url = self.ft.get_url()
            elif i == 1:
                self.work_url = self.pt.get_url()
            elif i ==2:
                self.work_url = self.int.get_url()
            else:
                self.work_url = self.tmp.get_url()

            b = True
            while b:
                html_content = requests.get(self.ft.get_url(), headers=HEADERS)
                soup = BeautifulSoup(html_content.text, 'html.parser')

                if not soup.find("ul", class_="spHGqe"):
                    self.apply_links = soup.find_all("a", class_="WpHeLc VfPpkd-mRLv6 VfPpkd-RLmnJb")
                    self.locs = soup.find_all("span", class_="r0wTof")
                    self.qualifications = soup.find_all("div", class_="Xsxa1e")
                    self.titles = soup.find_all("h3", class_="QJPWVe")

                    for self.cur_no in range(len(self.apply_links)):
                        self.obj["Company"] = "Google"
                        self.obj["Title"] = self.titles[self.cur_no].text
                        self.obj["apply-url"] = "https://www.google.com/about/careers/applications/" + self.apply_links[self.cur_no]["href"]
                        self.obj["primary-location"] = self.locs[self.cur_no].text
                        self.obj["min-qualifications"] = self.qualifications[self.cur_no].text[23:]

                        self.job_html_cnt = requests.get(self.obj["apply-url"], headers=HEADERS)
                        self.soup2 = BeautifulSoup(self.job_html_cnt.text, 'html.parser')

                        self.obj["responsibilities"] = (self.soup2.find("div", class_="BDNOWe").text)[17:]
                        self.obj["job-description"] = (self.soup2.find("div", class_="aG5W3").text)[13:]

                        result = gjobs.insert_one(self.obj)
                        print("Document inserted with ID:", result.inserted_id)
                        # print(self.obj)

                    if i == 0:
                        self.ft.alter_url()
                        self.work_url = self.ft.get_url()
                    elif i == 1:
                        self.pt.alter_url()
                        self.work_url = self.pt.get_url()
                    elif i ==2:
                        self.int.alter_url()
                        self.work_url = self.int.get_url()
                    else:
                        self.tmp.alter_url()
                        self.work_url = self.tmp.get_url()
                else:
                    b = False

k = GoogleJobs()
k.get_data()