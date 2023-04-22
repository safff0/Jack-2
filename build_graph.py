import networkx as nx
#import matplotlib.pyplot as plt
import pickle


f = open('dataset.csv')
data = f.readlines()[1:]
edges = []
phone_id = dict()
mail_id = dict()
address_id = dict()
comp_id = dict()
pep_id = dict()
inn_id = dict()
c = 0
labels = {}
colors = {}
alphas = {}
types = {}
for line in data:
#    print(line)
    ind, name, phones, mails, address, comp, pep, inn = line.split(';')
    phones = phones.split(',')
    mails = mails.split(',')
    address = address.split('\t')
    comp = comp.split('\t')
    pep = pep.split('\t')
    inn = inn.split(',')
    c1 = c
    labels[c] = name
    types[c] = 'term'
    colors[c] = '#3058CF'
    alphas[c] = 1
    c += 1
    for phone in phones:
        if len(phone) <= 3:
            continue
        if phone in phone_id:
            edges.append((c1, phone_id[phone]))
        else:
            edges.append((c1, c))
            phone_id[phone] = c
            labels[c] = phone
            colors[c] = '#CF3070'
            types[c] = 'phone'
            alphas[c] = 0.8
            c += 1  
    for mail in mails:
        if len(mail) <= 3:
            continue
        if mail in mail_id:
            edges.append((c1, mail_id[mail]))
        else:
            edges.append((c1, c))
            mail_id[mail] = c
            labels[c] = mail
            types[c] = 'mail'
            colors[c] = '#33FF55'
            alphas[c] = 0.8
            c += 1
    for addr in address:
        if len(addr) <= 3:
            continue
        if addr in address_id:
            edges.append((c1, address_id[addr]))
        else:
            edges.append((c1, c))
            address_id[addr] = c
            labels[c] = addr
            types[c] = 'address'
            colors[c] = '#FF34E6'
            alphas[c] = 0.8
            c += 1
    for addr in comp:
        if len(addr) > 1:
            if addr in comp_id:
                edges.append((c1, comp_id[addr]))
            else:
                edges.append((c1, c))
                comp_id[addr] = c
                labels[c] = addr
                types[c] = 'company_name'
                colors[c] = '#34DAFF'
                alphas[c] = 0.8
                c += 1
    for addr in pep:
        if len(addr) > 1:
            if addr in comp_id:
                edges.append((c1, pep_id[addr]))
            else:
                edges.append((c1, c))
                pep_id[addr] = c
                labels[c] = addr
                types[c] = 'person'
                colors[c] = '#FFF334'
                alphas[c] = 0.8
                c += 1
    for addr in inn:
        if len(addr) > 1:
            if addr in comp_id:
                edges.append((c1, inn_id[addr]))
            else:
                edges.append((c1, c))
                inn_id[addr] = c
                labels[c] = addr
                types[c] = 'inn'
                colors[c] = '#FF9D34'
                alphas[c] = 0.8
                c += 1

for key in comp_id:
    for key1 in comp_id:
        if key1 != key and key.lower().strip() in key1.lower().strip() and len(key.strip()) > 2:
            edges.append((comp_id[key], comp_id[key1]))
    
g = nx.Graph()
for i in range(c):
    g.add_node(i)
g.add_edges_from(edges)
nx.set_node_attributes(g, labels, 'label')
nx.set_node_attributes(g, types, 'type')
nx.set_node_attributes(g, colors, 'color')
nx.set_node_attributes(g, alphas, 'alpha')
pickle.dump(g, open('graph.pickle', 'wb'))