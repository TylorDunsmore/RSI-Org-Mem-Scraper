from bs4 import BeautifulSoup as soup
from time import sleep
import json
import requests
import random
import csv
from datetime import datetime

#Created by Tylor Dunsmore

####################


# Organization section
def scrape_orgs(page_num, pages, min_org_size):

    while page_num <= pages:
        # web page with page_num, loads 32 orgs per page, sorted by organization size
        org_list_html = "https://robertsspaceindustries.com/community/orgs/listing?sort=size_desc&search=&pagesize=12&page=%s&" % page_num

        # open connection, grab page
        response = requests.get(org_list_html)
        page_html = response.text

        # html parsing
        page_soup = soup(page_html, "html.parser")

        # get all org-cells, one for each org on page
        org_soup_all = page_soup.findAll("div", {"class":"org-cell"})
        page_num += 1
        sleep(round(random.uniform(0.50, 0.99), 2))

        for orgloop in org_soup_all:
            # get org name
            org_name = orgloop.a.h3.text

            # get org initials
            org_initials = orgloop.find("span", {"class": "symbol"}).text

            # get org total # of members, searches for span value then splits u
            span_value = orgloop.findAll("span", {"class": "value"})
            org_total = str(span_value[5])
            org_total = org_total.split(">")
            org_total = str(org_total[1])
            org_total = org_total.split("<")
            org_total = int(org_total[0])
            if org_total < min_org_size:
                break

            temp_list = [org_name, org_initials, org_total]
            inside_org_list.append(temp_list)
            print(temp_list)

    return inside_org_list

####################

# Member section
inside_member_list = []
url = 'https://robertsspaceindustries.com/api/orgs/getOrgMembers'

def scrape_members(org, count):
    # json request header and payload
    page = 1
    page_total = int(count / 32)
    if int(count % 32) > 0:
        page_total += 1

    sleep(round(random.uniform(0.10, 0.49), 2))

    while page <= page_total:
        header = {'Content-Type': 'application/json'}
        payload = {"symbol":org,"search":"","pagesize":32,"page":page}
        r = requests.post(url, headers=header, data=json.dumps(payload))
        page += 1

        # get json information from response
        r_json = r.json()

        # get html information from json response
        member_html = r_json['data']['html']
        member_page_soup = soup(member_html, "html.parser")

        member_section_main = member_page_soup.findAll("li", {"class": "member-item js-member-item org-main org-visibility-V"})
        member_section_affiliate = member_page_soup.findAll("li", {"class": "member-item js-member-item org-visibility-V"})
        # print(member_section_main)
        # print(member_section_affiliate)

        # loop for main members
        for i in range(0, len(member_section_main)):
            member_section_temp = member_section_main[i].find("span", {"class": "trans-03s frontinfo"})
            member_section_temp = member_section_temp.text
            member_section_temp = member_section_temp.split("\n")

            # Record name
            # Record nickname / Handle name
            # Record org rank
            # Record org symbol
            # Record org affiliation, 1 = main
            member_section_return = [member_section_temp[2], member_section_temp[3], member_section_temp[10], org, 1]
            print(member_section_return)
            inside_member_list.append(member_section_return)

        # loop for affiliate members
        for i in range(0, len(member_section_affiliate)):
            member_section_temp = member_section_affiliate[i].find("span", {"class": "trans-03s frontinfo"})
            member_section_temp = member_section_temp.text
            member_section_temp = member_section_temp.split("\n")
            # Record name
            # Record nickname / Handle name
            # Record org rank
            # Record org symbol
            # Record org affiliation, 0 = affiliate
            member_section_return = [member_section_temp[2], member_section_temp[3], member_section_temp[10], org, 0]
            print(member_section_return)
            inside_member_list.append(member_section_return)
    return inside_member_list

####################

if __name__ == '__main__':
    time = datetime.now()
    time_s = time.strftime("%d-%m-%YT%H-%M-%S")
    dt_orgs = "ORG-SCAN-D" + time_s + ".csv"
    dt_members = "MEMBER-SCAN-D" + time_s + ".csv"
    org_header = ["NAME", "INITIALS", "SIZE"]
    member_header = ["NAME", "HANDLE", "RANK", "ORG", "AFFILIATION"]


    ########## STANDARD VARIABLES ##########

    # Starting organization page, ending organization page and minimum organization size
    # Organization scraping ends when max org page or minimum org size is reached
    input_start_page = 1
    input_max_org_pages = 20
    input_min_org_size = 100

    ####################

    inside_org_list = []

    member_list = []

    final_org_list = scrape_orgs(input_start_page, input_max_org_pages, input_min_org_size)

    with open(dt_orgs, 'w', newline='', encoding="utf-8") as file:
        org_writer = csv.writer(file, csv.QUOTE_NONE, delimiter=",")
        org_writer.writerow(org_header)
        for z in range(0, len(final_org_list)):
            org_writer.writerow(final_org_list[z])

    for y in range(0, len(final_org_list)):
        member_list.append(scrape_members(final_org_list[y][1], final_org_list[y][2]))

    with open(dt_members, 'w', newline='', encoding="utf-8") as file:
        member_writer = csv.writer(file, csv.QUOTE_NONE, delimiter=",")
        member_writer.writerow(member_header)
        print(len(member_list))
        print(len(member_list[0]))

        for x in range(0, len(member_list[0])):
            member_writer.writerow(member_list[0][x])