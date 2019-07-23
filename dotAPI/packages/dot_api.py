########################################
# Analysys Stock                       #
########################################
import os
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
## import webbrowser
COMPONY_CODES = {}

## Reading CSV FILE OF COMPANY_CODE
from pathlib import Path as path
##import os

MY_PATH = os.path.dirname(os.path.abspath(__file__))
print(MY_PATH)
MY_PATH = path(MY_PATH)
## MY_PATH.parent
kospi_path = os.path.join(MY_PATH.parent, 'sources\Kospiu.csv')
kospi_path = path(kospi_path)
print(kospi_path)
DF = pd.read_csv(kospi_path, encoding='utf8')

for i in range(len(DF.회사명)):
    ## print(DF.종목코드[i])
    COMPONY_CODES[DF.회사명[i]] = DF.종목코드[i]
## print(COMPONY_CODES)

URL_MAIN = 'http://dart.fss.or.kr'
URL_AUTH = '/api/search.xml?auth='
API_KEY = '163049595a0c6281a6e58e9b248a7e7143b15b3d'
URL_CRP = '&crp_cd='
def getCompayCode(name):
    c_code = str(COMPONY_CODES[name])
    while len(c_code) != 6:
        c_code = '0' + c_code
    print(c_code)
    return (c_code)

COMPONY_CODE = getCompayCode('유한양행')
URL_DT = '&start_dt=19990101'
BSN_TP = '&bsn_tp=A001&bsn_tp=A002&bsn_tp=A003'


URL = URL_MAIN + URL_AUTH + API_KEY + URL_CRP + str(COMPONY_CODE) + URL_DT + BSN_TP
RESPONSE = requests.get(URL).text
SOUP = bs(RESPONSE, 'html.parser')


## Define Empty DataFrame
DATA = pd.DataFrame()

RESULTS = SOUP.select('list')

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
## print(RESULTS3)
