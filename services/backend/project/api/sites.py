import requests
from bs4 import BeautifulSoup, element


class Indeed:
    def __init__(self, words, location, offset):
        self.offset = int(offset)
        self.step = 10
        self.url = "https://www.indeed.com/jobs?as_and={}&l={}&sort=date&start=".format(
            "+".join(set(d.strip().lower() for d in words.split(",") if d)),
            "+".join(list(d.lower() for d in location.split(" ") if d)),
        )

    def extract(self, soup):
        if not soup:
            return []
        jobs = []
        for tag in soup.find_all(name="div", attrs={"class": "jobsearch-SerpJobCard"}):
            for child in tag.children:
                if child and type(child) == element.Tag and child.attrs:
                    if child.attrs["class"][0] == "title":
                        title = child.get_text().strip()
                        for grandchild in child.find_all(name="a"):
                            if grandchild.has_attr("href"):
                                link = "https://www.indeed.com" + grandchild["href"]
                    elif child.attrs["class"][0] == "sjcl":
                        lines = child.get_text().strip().split("\n")
                        company = lines[0]
                        location = lines[-1]
                    elif child.attrs["class"][0] == "jobsearch-SerpJobCard-footer":
                        date = None
                        for grandchild in child.find_all(
                            name="span", attrs={"class": "date"}
                        ):
                            date = grandchild.get_text()
            if date:
                jobs.append([company, title, location, date, link])
            else:
                jobs.append([company, title, location, "n/a", link])
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

    def increment_offset(self):
        self.offset += self.step

    def decrement_offset(self):
        self.offset -= self.step
