import json
import requests
import bs4


ROOT = "https://cloud.google.com"
SKILLS_ROOT = "https://www.cloudskillsboost.google"
ROLES = [
    "Cloud Architect",
    "Cloud Database Engineer",
    "Cloud Developer",
    "Data Engineer",
    "Cloud DevOps Engineer",
    "Cloud Security Engineer",
    "Cloud Network Engineer",
    "Google Workspace Administrator",
    "Machine Learning Engineer",
]


def main():
    for role, courses in scrape_roles():
        print(json.dumps({"role": role, "courses": courses}))


def scrape_roles():
    root_html = requests.get(f"{ROOT}/certification").text
    root_soup = bs4.BeautifulSoup(root_html, "html.parser")
    tracks = root_soup.select_one("div.track-list-module__container")
    for role in ROLES:
        role_link = tracks.find("a", string=lambda s: s if s.strip() == role else None)
        yield role, get_courses_for_role_url(f'{ROOT}{role_link.get("href")}')


def get_courses_for_role_url(href):
    role_page = requests.get(href).text
    role_page_soup = bs4.BeautifulSoup(role_page, "html.parser")
    courses_page = role_page_soup.find("a", href=lambda s: s if (s and "cloudskillsboost.google/paths" in s) else None).get("href")
    courses = fetch_courses(courses_page)
    return courses


def fetch_courses(url):
    courses_page = requests.get(url).text
    courses_soup = bs4.BeautifulSoup(courses_page, "html.parser").find("ol", class_=lambda c: c if (c and c == "learning-plan-activities") else None)
    courses = courses_soup.find_all("ql-activity-card")
    names = []
    for course in courses:
        names.append({"url": f"{SKILLS_ROOT}{course.get('path')}",
                      "type": course.get("type"),
                      "name": course.get("name")})
    return names


if __name__ == "__main__":
    main()
