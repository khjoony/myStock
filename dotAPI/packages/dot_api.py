import os
import csv
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import webbrowser
COMPONY_CODES = {
    '안국약품' : '001540',
    '한솔 케미칼' : '014680',
}

## Reading CSV FILE OF COMPANY_CODE
DF = pd.read_csv('..\\sources\\Kospi1.csv', encoding='utf8')
DF
URL_MAIN = 'http://dart.fss.or.kr'
URL_AUTH = '/api/search.xml?auth='
API_KEY = '163049595a0c6281a6e58e9b248a7e7143b15b3d'
URL_CRP = '&crp_cd='
COMPONY_CODE = COMPONY_CODES['안국약품']
URL_DT = '&start_dt=19990101'
BSN_TP = '&bsn_tp=A001&bsn_tp=A002&bsn_tp=A003'


URL = URL_MAIN + URL_AUTH + API_KEY + URL_CRP + COMPONY_CODE + URL_DT + BSN_TP
RESPONSE = requests.get(URL).text
soup = bs(RESPONSE, 'html.parser')


## Define Empty DataFrame
DATA = pd.DataFrame()

RESULTS = soup.select('list')

for result in RESULTS:
    temp = pd.DataFrame(([[result.crp_cls.string, result.crp_nm.string,\
        result.crp_cd.string, result.rpt_nm.string, result.rcp_no.string,\
        result.flr_nm.string, result.rcp_dt.string, result.rmk.string]]),\
        columns=['crp_cls', 'crp_nm', 'crp_cd','rpt_nm', 'rcp_no', 'flr_nm',\
            'rcp_dt', 'rmk'])
    DATA = pd.concat([DATA, temp])
DATA = DATA.reset_index(drop=True)

URL2 = URL_MAIN + '/dsaf001/main.do?rcpNo=' + DATA['rcp_no'][0]
print(URL2)
RESPONSE2 = requests.get(URL2).text
SOUP2 = bs(RESPONSE2, 'html.parser')
RESULTS2 = str(SOUP2.find('head'))
if len(RESULTS2.split(' 연결재무제표",')) > 1:
    RESULTS2 = RESULTS2.split(' 연결재무제표",')[1]
else:
    RESULTS2 = RESULTS2.split(' 재무제표",')[1]
RESULTS2 = RESULTS2.split('cnt++')[0]
RESULTS2 = RESULTS2.split('viewDoc(')[1]
RESULTS2 = RESULTS2.split(')')[0]
RESULTS2 = RESULTS2.split(', ')
RESULTS2 = [RESULTS2[i][1:-1]for i in range(len(RESULTS2))]
URL3 = '/report/viewer.do?rcpNo='
URL_FINAL = URL_MAIN + URL3 + RESULTS2[0] + '&dcmNo=' + RESULTS2[1] + '&eleId=' + RESULTS2[2]\
    + '&offset=' + RESULTS2[3] + '&length=' + RESULTS2[4]\
    + '&dtd=dart3.xsd'

print(URL_FINAL)

RESPONSE3 = requests.get(URL_FINAL).text
SOUP3 = bs(RESPONSE3, 'html.parser')
RESULTS3 = SOUP3.select('table')
##print(RESULTS3)
