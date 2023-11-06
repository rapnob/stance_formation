import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('input_nodepath', type=str)
    parser.add_argument('span', type=str)
    parser.add_argument('output_graphml', type=str)
    parser.add_argument("--log", default="WARNING")
    return parser.parse_args()

args = parse_arguments()



import numpy as np
import pandas as pd
import networkx as nx
import logging
import collections

fmt = "%(asctime)s %(levelname)s %(name)s :%(message)s"
logging.basicConfig(level=args.log, format=fmt)


OUT_THRESHOLD=30
IN_THRESHOLD=30

path = args.input_nodepath
logging.info('Loading node data...')

nodes=pd.read_csv(path, index_col="id")
nodes=nodes[nodes['Label'].isnull()!=True]

# #top_clusters=[x[0] for x in collections.Counter(nodes['modularity_class'].to_list()).most_common(3)]
# #nodes=nodes.query('modularity_class==@top_clusters[0] | modularity_class==@top_clusters[1] | modularity_class==@top_clusters[2]')
nodes_id=nodes.index

span = args.span


if span in ["06-1-10","06-11-20","06-21-30","07-1-10","07-11-20","07-21-31","08-1-10","08-11-20","08-21-31"]:
    span2 = "06to08"
elif span in ["09-1-10","09-11-20","09-21-30","10-1-10","10-11-20","10-21-31"]:
    span2 = "09to10"
else:
    raise ValueError(span + ' is invalid.')
    

path = "/data/str01_03/twitter/hisamits/data/youtube/2021-"+span2+"_RMQ_tlg/edges/2021-"+span+"_edges.csv"

logging.info('Loading edge data...')

df=pd.read_csv(path)
df=df[df['source'].isin(nodes_id)]
df=df[df['target'].isin(nodes_id)]
df.loc[:,['source','target']]

lines=df['source'].astype(str).str.cat(df['target'].astype(str), sep=' ').to_list()
cnt=collections.Counter(lines)
lines=[x+" "+str(cnt[x]) for x in lines]

Graphtype = nx.DiGraph() # 有向グラフ
G = nx.read_weighted_edgelist(lines, create_using=Graphtype,nodetype=int)
# nx.set_node_attributes(G, dict(nodes['s_avg']), "stance")
nx.set_node_attributes(G, dict(nodes['s']), "stance")
nx.set_node_attributes(G, dict(nodes['s_cs']), "stance_cs")

G.remove_nodes_from(list(set([key for key in dict(G.nodes(data=True)).keys()]) - (set([key for key in dict(G.nodes(data=True)).keys()  if G.in_degree[key]>=IN_THRESHOLD]) | set([key for key in dict(G.nodes(data=True)).keys() if G.out_degree[key]>=OUT_THRESHOLD]))))

#top_clusters=[x[0] for x in collections.Counter([value['modularity_class'] for value in dict(G.nodes(data=True)).values()]).most_common(3)]
#G.remove_nodes_from([key for key in dict(G.nodes(data=True)).keys() if G.nodes(data=True)[key]['modularity_class'] not in top_clusters])
path = args.output_graphml

logging.info('Wrigint graphml...')

nx.write_graphml(G, path)
logging.info('Finished.')
