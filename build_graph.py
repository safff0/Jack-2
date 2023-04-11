import networkx as nx
import matplotlib.pyplot as plt
import pickle


f = open('dataset.csv')
data = f.readlines()[1:]
edges = []
phone_id = dict()
c = 0
labels = {}
colors = []
alphas = []
for line in data:
    ind, name, phones = line.split(';')
    phones0 = phones[:]
    phones = phones.split(',')
    c1 = c
    labels[c] = name
    colors.append('#3058cf')
    alphas.append(1)
    c += 1
    if phones0 == '\n':
        continue
    for phone in phones:
        if phone in phone_id:
            edges.append((c1, phone_id[phone]))
        else:
            edges.append((c1, c))
            phone_id[phone] = c
            labels[c] = phone
            colors.append('#cf3070')
            alphas.append(0.8)
            c += 1
g = nx.Graph()
for i in range(c):
    g.add_node(i)
nx.set_node_attributes(g, labels, 'labels')
g.add_edges_from(edges)
pos = nx.spring_layout(g)
nx.draw_networkx_nodes(g, pos=pos, node_color=colors, alpha=alphas)
nx.draw_networkx_edges(g, pos, edges)
nx.draw_networkx_labels(g, pos, labels, font_size=6)
plt.show()
pickle.dump(g, open('graph.pickle', 'wb'))