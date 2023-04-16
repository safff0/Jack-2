import networkx as nx
#import matplotlib.pyplot as plt
import pickle


f = open('dataset.csv')
data = f.readlines()[1:]
edges = []
phone_id = dict()
mail_id = dict()
address_id = dict()
c = 0
labels = {}
colors = {}
alphas = {}
types = {}
for line in data:
#    print(line)
    ind, name, phones, mails, address = line.split(';')
    phones = phones.split(',')
    mails = mails.split(',')
    address = address.split('\t')
    c1 = c
    labels[c] = name
    types[c] = 'term'
    colors[c] = '#3058CF'
    alphas[c] = 1
    c += 1
    if len(phones[0]) > 3:
        for phone in phones:
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
    if len(mails[0]) > 3:
        for mail in mails:
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
    if len(address[0]) > 3:
        for addr in address:
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
    
g = nx.Graph()
for i in range(c):
    g.add_node(i)
g.add_edges_from(edges)
nx.set_node_attributes(g, labels, 'label')
nx.set_node_attributes(g, types, 'type')
nx.set_node_attributes(g, colors, 'color')
nx.set_node_attributes(g, alphas, 'alpha')
pickle.dump(g, open('graph.pickle', 'wb'))