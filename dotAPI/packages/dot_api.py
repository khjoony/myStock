import re
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs

URL_AUTH = 'http://dart.fss.or.kr/api/search.xml?auth='
API_KEY = '163049595a0c6281a6e58e9b248a7e7143b15b3d'
URL_CRP = '&crp_cd='
COMPONY_CODE = '005440'
URL_DT = '&start_dt=19990101'
BSN_TP = '&bsn_tp=A001&bsn_tp=A002&bsn_tp=A003'


URL = URL_AUTH + API_KEY + URL_CRP + COMPONY_CODE + URL_DT + BSN_TP
## print(URL)
RESPONSE = requests.get(URL).text
## print(RESPONSE)
soup = bs(RESPONSE, 'html.parser')
print(soup)
