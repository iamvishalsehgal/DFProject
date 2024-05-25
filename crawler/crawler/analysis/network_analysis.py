import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Load the data

data = pd.read_csv("crawler/crawler/output/big_results.csv")

# Create the graph
G = nx.Graph()
for index, row in data.iterrows():
    seller = row['seller']
    discord = row['discord']
    telegram = row['telegram']
    
    if pd.notnull(discord):
        G.add_edge(seller, discord, relation='uses')
    if pd.notnull(telegram):
        G.add_edge(seller, telegram, relation='uses')

# Plot the graph
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1500, edge_color='#cccccc', font_size=10)
plt.title('Network Graph of Sellers and Communication Channels')
plt.show()