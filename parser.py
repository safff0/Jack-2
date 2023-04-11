import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from tqdm import tqdm


phone_regex = re.compile(r'[\+]?[78][(\s-]{0,2}[0-9]{3}[)\s-]{0,2}[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{2}[-\s\.]?[0-9]{2}')

df = pd.DataFrame({'name': [],
                   'phones': []})

a = open('real_estate_domains.tsv')
a = a.readlines()[1:]
a = [e.strip() for e in a]
for link in tqdm(a[:1000]):
    try:
        page = requests.get(f'http://{link}', timeout=6)
    except Exception:
        continue
    soup = BeautifulSoup(page.content, "html.parser")
    soup.prettify()
    test = soup.text
    phones = phone_regex.findall(test)
    phones = [''.join(re.findall('\d+', e)) for e in phones]
    phones = list(set([f'8{e[1:]}' for e in phones]))
    list_row = [link, ','.join(phones)]
    df.loc[len(df)] = list_row
df.to_csv('dataset.csv', sep=';')