import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from tqdm import tqdm


def mystrip(s):
    s = s.strip()
    s = s.replace('\n', '')
    s = s.replace('\t', '')
    s = s.replace('"', '')
    return s


phone_regex = re.compile(r'[\+]?[78][(\s-]{0,2}[0-9]{3}[)\s-]{0,2}[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{2}[-\s\.]?[0-9]{2}')
email_regex = re.compile(r'[\w\.-]+@(?:[\w-]+\.)+(?:ru|com)')
address_regex = re.compile(r'[^\d,\n]+(?:, ){1}[^\d,]+(?:, ){1}(?:д.(?: )?)?(?:дом )?[0-9]{1,}')

df = pd.DataFrame({'name': [],
                   'phones': [],
                   'mails': [],
                   'address': []})

a = open('real_estate_domains.tsv')
a = a.readlines()[1:]
a = [e.strip() for e in a[:1000]]
a = list(dict.fromkeys(a))
for link in tqdm(a):
    try:
        page = requests.get(f'http://{link}', timeout=3)
    except Exception:
        continue
    soup = BeautifulSoup(page.content, "html.parser")
    soup.prettify()
    test = soup.text
    phones = phone_regex.findall(test)
    phones = [''.join(re.findall('\d+', e)) for e in phones]
    phones = list(set([f'8{e[1:]}' for e in phones]))
    mails = email_regex.findall(test)
    mails = list(set(mystrip(e) for e in mails))
    address = address_regex.findall(test)
    address = list(set(mystrip(e) for e in address if len(e) <= 60))
    list_row = [link, ','.join(phones), ','.join(mails), '\t'.join(address)]
    df.loc[len(df)] = list_row
df.to_csv('dataset.csv', sep=';')