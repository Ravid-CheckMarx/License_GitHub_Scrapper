import requests
from bs4 import BeautifulSoup
from utils import GitHub_base_license_search_url
from pprint import pprint
import re
import matplotlib.pyplot as plt
import numpy as np
from prettytable import PrettyTable
invalid_license = False
count_repos = 0

# list of license names = ["afl-3.0", "agpl-3.0","apache-2.0", "artistic-2.0", "bsd-2-clause", "bsd-3-clause","bsd-3-clause-clear",
# "bsd-4-clause", "bsl-1.0", "cc-by-4.0", "cc-by-sa-4.0", "cc0-1.0", "epl-1.0", "epl-2.0", "eupl-1.1", "eupl-1.2",
# "gpl-2.0", "gpl-3.0", "isc", "lgpl-2.1", "lgpl-3.0", "lppl-1.3c", "mit", "mit-0", "mpl-2.0", "wtfpl", "zlib"]


license_name = "mit"
search_qury = GitHub_base_license_search_url + license_name
page = requests.get(search_qury)

print("The search query is: " +search_qury)
soup = BeautifulSoup(page.content, "html.parser")
check_page = soup.findAll('p')

for p in check_page:
    if invalid_license == False:
        if "An invalid license was specified." in p:
            invalid_license = True
if not invalid_license:

    inputs = soup.find_all('span', class_='ml-1 js-codesearch-count Counter Counter--primary')
    if inputs:
        for input in inputs:
            if input['data-search-type']:
                names = input['data-search-type']
                if names == 'Repositories':
                    count_repos +=1
                if count_repos < 2:
                    print(names)
                    value = input.text
                    print(value)
    disterbution_count = soup.find_all('span', class_='count')
    disterbution_names = soup.find_all('a', class_='filter-item')

    names_list = []
    count_list = []
    for dist in disterbution_names:
        names = str(dist.text).rsplit()
        count = names[0]
        count_list.append(count)
        name = names[1]
        names_list.append(name)


    table = PrettyTable(['Name', 'Count'])
    for name, count in zip(names_list, count_list):
        table.add_row([name,count])
    print(table)

    repo_list = []
    repo_names = soup.find_all('a', class_='v-align-middle')
    for name in repo_names:
        repo_list.append(name.text)

    stars_list = []
    repo_stars = soup.find_all('a', class_='Link--muted')
    for star in repo_stars:
        grade = str(star.text).rsplit()
        if "k" in grade[0]:
            stars_list.append(grade[0])

    table = PrettyTable(['Repo name', 'Stars'])
    for name, stars in zip(repo_list, stars_list):
        table.add_row([name,stars])
    print(table)
else:
    print(license_name + "is not a valid license name, try again")





