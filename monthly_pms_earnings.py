from urllib.request import Request, urlopen
import urllib
from bs4 import BeautifulSoup
from datetime import datetime

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

def get_pms_earning_for_given_month_and_year(pmrId, year, month):
    url_data = "pmrID" + pmrId + "&year" + str(year) + "&month" + str(month)
    url_data = url_data.encode('ascii')

    queryurl = Request('https://www.sebi.gov.in/sebiweb/other/OtherAction.do?doPmr=yes', url_data)
    pms_earning_report = urlopen(queryurl).read()

    pms_earning_soup = BeautifulSoup(pms_earning_report, 'html.parser')
    
    discretionary_services_div = pms_earning_soup.find_all('div', attrs = {'class' : 'org-table-1'})[1]
    discretionary_services_td = discretionary_services_div.find_all('td')
    portfolio_perf_in_percentage = list(discretionary_services_td[3].children)[0]
    
    return portfolio_perf_in_percentage


def write_data_to_csv():
    pass

def main():
    report = get_sebi_report_page()
    pmrId_list = get_pmrids(report)
    
    currentMonth = datetime.now().month
    currentYear = datetime.now().year

    year = 2013                 ## First year for which data is available on the SEBI webpage

    for pmrId in pmrId_list:
        while year <= currentYear:
            month = 1
            if year == currentYear:
                while (month <= 12) or (month <= currentMonth):
                    portfolio_perf_in_percentage = get_pms_earning_for_given_month_and_year(pmrId, year, month)
                    month += 1
            else:
                while month <= 12:
                    portfolio_perf_in_percentage = get_pms_earning_for_given_month_and_year(pmrId, year, month)
                    month += 1
            year += 1

if __name__ == "__main__":
    main()