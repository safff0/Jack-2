import networkx as nx
import matplotlib.pyplot as plt
import pickle
import argparse
from pyvis.network import Network
import pyautogui


screensize = pyautogui.size()

parser = argparse.ArgumentParser(
                    prog='GraphPrinter',
                    description='Prints GRAPH.pickle')
parser.add_argument(dest='filepath', type=str, help='Filepath to GRAPH.pickle')
parser.add_argument('-s', dest='scale', action='store', type=float, default=100, help='Set scale of the pyplot')
args = parser.parse_args()
sc = args.scale / 100

g = pickle.load(open(args.filepath, 'rb'))
G = Network(height=screensize[1] - 80, width=screensize[0] - 50, notebook=True)
G.from_nx(g)
G.toggle_hide_edges_on_drag(True)
G.show('graph.html')