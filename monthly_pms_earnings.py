from urllib.request import Request, urlopen
import urllib
from bs4 import BeautifulSoup

def get_sebi_report_page():
    queryurl = Request('https://www.sebi.gov.in/sebiweb/other/OtherAction.do?doPmr=yes')

    report = urlopen(queryurl).read()
    return report

def get_pmrids(report):
    soup = BeautifulSoup(report, 'html.parser')
    option_tag_list = soup.find_all('select', attrs = {'name' : 'pmrId'})[0].find_all('option')

    pmrId_list = []

    for option in option_tag_list:
        pmrId_list.append(option['value'])

    return pmrId_list

def get_pms_earning_for_given_month_and_year():
    pass

def write_data_to_csv():
    pass

def main():
    report = get_sebi_report_page()
    pmrId_list = get_pmrids(report)
    print(pmrId_list)

if __name__ == "__main__":
    main()