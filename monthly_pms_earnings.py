from urllib.request import Request, urlopen
import urllib
from bs4 import BeautifulSoup
from datetime import datetime
import csv

def get_sebi_report_page():
    queryurl = Request('https://www.sebi.gov.in/sebiweb/other/OtherAction.do?doPmr=yes')

    report = urlopen(queryurl).read()
    return report

def get_pmrids(report):
    soup = BeautifulSoup(report, 'html.parser')
    option_tag_list = soup.find_all('select', attrs = {'name' : 'pmrId'})[0].find_all('option')

    pmrId_list = []

    for option in option_tag_list:
        if option['value'] != '':
            pmrId_list.append(option['value'])
        else:
            pass
        
    return pmrId_list

def get_pms_earning_for_given_month_and_year(pmrId, year, month):
    url_data = "pmrId=" + pmrId + "&year=" + str(year) + "&month=" + str(month)
    url_data = url_data.encode('ascii')

    queryurl = Request('https://www.sebi.gov.in/sebiweb/other/OtherAction.do?doPmr=yes', url_data)
    pms_earning_report = urlopen(queryurl).read()

    pms_earning_soup = BeautifulSoup(pms_earning_report, 'html.parser')

    try:
        particulars_div = pms_earning_soup.find_all('div', attrs = {'class' : 'org-table-1'})[1]
        particulars_td = particulars_div.find_all('td')
        portfolio_perf_in_percentage = list(particulars_td[3].children)[0]
    except IndexError:
        portfolio_perf_in_percentage = None

    print(portfolio_perf_in_percentage)
    return portfolio_perf_in_percentage


def write_data_to_csv(pmrId, year, month, portfolio_perf_in_percentage):
    pmsname = pmrId.split('@@')[2]
    row = [pmsname, year, month, portfolio_perf_in_percentage]
    
    print(row)
    with open('pms_earnings.csv', 'a') as writefile:
        writer = csv.writer(writefile)
        writer.writerow(row)

    writefile.close()

def main():
    report = get_sebi_report_page()
    print("Report collected")

    pmrId_list = get_pmrids(report)
    print("Collected the list of pmrIds")
    
    currentMonth = datetime.now().month
    currentYear = datetime.now().year

    for pmrId in pmrId_list:
        year = 2013         ## First year for which data is available on the SEBI webpage
        while year <= currentYear:
            month = 1
            if year == currentYear:
                while (month <= 12) and (month <= currentMonth):
                    portfolio_perf_in_percentage = get_pms_earning_for_given_month_and_year(pmrId, year, month)
                    print(pmrId, year, month)
                    if portfolio_perf_in_percentage != None:
                        write_data_to_csv(pmrId, year, month, portfolio_perf_in_percentage)
                    else:
                        pass
                    month += 1
            else:
                while month <= 12:
                    portfolio_perf_in_percentage = get_pms_earning_for_given_month_and_year(pmrId, year, month)
                    print(pmrId, year, month)
                    if portfolio_perf_in_percentage != None:
                        write_data_to_csv(pmrId, year, month, portfolio_perf_in_percentage)
                    else:
                        pass
                    month += 1
            year += 1

if __name__ == "__main__":
    main()