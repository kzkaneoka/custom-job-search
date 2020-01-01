import requests
from bs4 import BeautifulSoup, element


class Indeed:
    def __init__(self, words, location, offset):
        self.url = "https://www.indeed.com/jobs?as_and={}&l={}&sort=date&start={}".format(
            "+".join(set(d.strip().lower() for d in words.split(",") if d)),
            "+".join(list(d.lower() for d in location.split(" ") if d)),
            int(offset),
        )

    def extract(self, soup):
        if not soup:
            return []
        jobs = []
        for tag in soup.find_all(name="div", attrs={"class": "jobsearch-SerpJobCard"}):
            job = {}
            for child in tag.children:
                if child and type(child) == element.Tag and child.attrs:
                    if child.attrs["class"][0] == "title":
                        job["title"] = child.get_text().strip()
                        for grandchild in child.find_all(name="a"):
                            if grandchild.has_attr("href"):
                                job["link"] = (
                                    "https://www.indeed.com" + grandchild["href"]
                                )
                    elif child.attrs["class"][0] == "sjcl":
                        lines = child.get_text().strip().split("\n")
                        job["company"] = lines[0]
                        job["location"] = lines[-1]
                    elif child.attrs["class"][0] == "jobsearch-SerpJobCard-footer":
                        job["date"] = "n/a"
                        for grandchild in child.find_all(
                            name="span", attrs={"class": "date"}
                        ):
                            job["date"] = grandchild.get_text()
            jobs.append(job)
        return jobs

    def fetch(self):
        soup = None
        try:
            r = requests.get(self.url)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "html.parser")
        finally:
            return soup

    def search(self):
        soup = self.fetch()
        jobs = self.extract(soup)
        return jobs
