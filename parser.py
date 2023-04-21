import pandas as pd
import httplib2
from bs4 import BeautifulSoup, SoupStrainer
import re
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

def mystrip(s):
    s = s.strip()
    s = s.replace('\n', '')
    s = s.replace('\t', '')
    s = s.replace('"', '')
    return s


phone_regex = re.compile(r'[\+]?[78][(\s-]{0,2}[0-9]{3}[)\s-]{0,2}[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{2}[-\s\.]?[0-9]{2}')
email_regex = re.compile(r'[\w\.-]+@(?:[\w-]+\.)+(?:ru|com)')
company_regex = re.compile(r'(?:ООО ?|АО ?|ооо ?|ао ?)\"([\w -]{2,})\"')
address_regex = re.compile(r'[А-ЯA-Z]{1}[\w-]+(?:, ?){1}(?:(?:у|У)л\. ?|(?:у|У)лица ?|(?:у|У)л ?)[А-ЯA-Z]{1}[\w-]{1,}')
person_regex = re.compile(r'[А-Я]{1}[а-я]+ [А-Я]{1}\. [А-Я]{1}\.')
inn_regex = re.compile(r'\b[1-9]{1}[0-9]{9}\b')

df = pd.DataFrame({'name': [],
                   'phones': [],
                   'mails': [],
                   'address': [],
                   'company': [],
                   'people': [],
                   'inn': []})

http = httplib2.Http(timeout=1)
a = open('real_estate_domains.tsv')
a = a.readlines()[1:]
a = list(dict.fromkeys(a))
a = [e.strip() for e in a]
executor = ThreadPoolExecutor(1)

def mapper(link):
    try:
        status, page = http.request(f'http://{link}')
        return status, page
    except Exception:
        return 'rip', 'cringe'

def pret(sl, l):
    if len(sl) == 0:
        return l
    if sl[0] == '.':
        sl = sl[1:]
    if sl.startswith(f'http://{l}') or sl.startswith(f'https://{l}'):
        return sl
    if sl[0] != '/':
        sl = '/' + sl
    return 'http://' + l + sl

def mapper_sublinks(info):
    status, page = info[0]
    link = info[1]
    if status == 'rip':
        return []
    soup = BeautifulSoup(page, "html.parser")
    soup.prettify()
    test = soup.text
    sublinks = soup.select('a')
    sublinks = [e.get('href') for e in sublinks if (e.get('href') != None)]
    sublinks = [pret(e, link) for e in sublinks]
    sublinks.append(f'http://{link}')
    sublinks = list(set(sublinks))
    if len(sublinks) > 100:
        sublinks = sublinks[:50] + sublinks[-50:]
    return sublinks

def mapper_asks(sublinks):
    ans = []
    for sublink in sublinks:
        try:
            status1, page1 = http.request(sublink)
            ans.append((status1, page1))
        except Exception:
            continue
    return ans

print('Parsing links...')
res = list(tqdm(executor.map(mapper, a)))
res = [(res[i], a[i]) for i in range(len(a))]
print('Mapping sublinks...')
subs = list(tqdm(executor.map(mapper_sublinks, res)))
print('Parsing sublinks...')
subsresp = list(tqdm(executor.map(mapper_asks, subs)))

print('Building csv...')
for i in tqdm(range(len(a))):
    status, page = res[i][0]
    link = a[i]
    if status == 'rip':
        continue
    sublinks = subs[i]
    phones0 = set()
    mails0 = set()
    address0 = set()
    comp0 = set()
    p0 = set()
    inn0 = set()
    for status1, page1 in subsresp[i]:
        if len(page1) > 1e6:
            page1 = page1[:1000000]
        try:
            soup = BeautifulSoup(page1, "html.parser")
            soup.prettify()
        except Exception:
            continue
        test = soup.text
        phones = phone_regex.findall(test)
        phones = [''.join(re.findall('\d+', e)) for e in phones]
        phones = set([f'8{e[1:]}' for e in phones])
        mails = email_regex.findall(test)
        mails = set(mystrip(e) for e in mails)
        address = address_regex.findall(test)
        address = set(mystrip(e) for e in address if len(e) <= 45)
        comp = set(company_regex.findall(test))
        people = set(person_regex.findall(test))
        inn = set(inn_regex.findall(test))
        comp0 |= comp
        phones0 |= phones
        address0 |= address
        mails0 |= mails
        inn0 |= inn
        p0 |= people
    list_row = [link, ','.join(phones0), ','.join(mails0), '\t'.join(address0), '\t'.join(comp0), '\t'.join(p0), ','.join(inn0)]
    df.loc[len(df)] = list_row
df.to_csv('dataset.csv', sep=';')