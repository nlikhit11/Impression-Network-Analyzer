import random
import networkx as nx
import numpy as np
import pandas as pd

# Read CSV file
f = pd.read_csv('impressions.csv')

# Create a directed graph
G = nx.DiGraph()

# Iterate through rows of each column,take source node as element of email address column(1st 11 characters in upper case) and
#target node as element of impressions columns(last 11 characters in upper case)
for _, row in f.iterrows():
    source_node = str(row['Email Address'])[:11].upper()
    for col in f.columns[2:]:  # Skip column 1
        target_node = str(row[col])[-11:].upper()
        if target_node != source_node and target_node != 'NAN': #only add edges if source and target are not same
            #to by pass the case of target element to be blank, I used != NAN
            G.add_edge(source_node, target_node)
print(G)    #print graph
def random_walk(G):     #random walk function which returns random walk points upon taking 100000 iterations
    nodes = list(G.nodes())
    RW_points = [0 for _ in range(len(nodes))]
    r = random.choice(nodes)
    RW_points[nodes.index(r)] += 1
    out = list(G.out_edges(r))

    c = 0
    while c != 100000:
        if not out:
            focus = random.choice(nodes)
        else:
            r1 = random.choice(out)
            focus = r1[1]
        RW_points[nodes.index(focus)] += 1
        out = list(G.out_edges(focus))
        c += 1

    return RW_points

RW_points = random_walk(G)

def nodes_sorted_by_RW_points(RW_points):   #sorts nodes based on random walk points by using a dictionary
    nodes = list(G.nodes())
    nodes_dict = {node: RW_points[nodes.index(node)] for node in nodes}
    sorted_nodes = sorted(nodes_dict, key=nodes_dict.get)  # Sort by RW points
    return sorted_nodes

nodes_sorted = nodes_sorted_by_RW_points(RW_points)
print(nodes_sorted[len(nodes_sorted)-1])        #print the sorted nodes list's last element as he is top leader

'''3a)Find the number of transitive triangles in the graph'''
def count_transitive_triangles(G): #function checks that if an edge exists between a node in the graph and the neighbour's neighbour of that node.
    #If so it increments the count to 1
  num_transitive_triangles = 0
  for node1 in G.nodes():
      for node2 in G.neighbors(node1):
          for node3 in G.neighbors(node2):
              if G.has_edge(node1, node3):
                  num_transitive_triangles += 1
  return num_transitive_triangles // 2  # Divide by 2 to avoid double counting

transitive_triangles_count = count_transitive_triangles(G)
print("Number of transitive triangles:", transitive_triangles_count)

'''3b)Upon picking an edge,how probable is it that edge turns out to be unidirectional'''
def count_unidirectional_relations(G): #by picking a node's edge, then checking if reverse edge involving those nodes exists in the edges of the graph
  unidirectional_count = 0
  for edge in list(G.edges()):
      reversed_edge = edge[::-1]
      if reversed_edge not in G.in_edges(edge[0]):
          unidirectional_count += 1 #if true then increment
  return unidirectional_count

unidirectional_relations_count = count_unidirectional_relations(G)
print("Number of unidirectional relations:", unidirectional_relations_count)

def probability_of_finding_unidirectional_relation(G): #the above count is divide by total edges in the graph to find prob.
  total_edges = len(list(G.edges()))
  unidirectional_count = count_unidirectional_relations(G)
  return unidirectional_count / total_edges
print("Probability of finding an unidirectional relation:", probability_of_finding_unidirectional_relation(G))
'''Q2) Missing links'''
'''Common neighbour matrix of the graph'''
def common_neighbour_matrix(G): #matrix which gives info on no. of common neighbours b/w two nodes
    nodes = list(G.nodes())
    num_nodes = len(G.nodes())
    common_neighbour_matrix = np.zeros((num_nodes, num_nodes), dtype=int)   # initialize a zero entry matrix
    for i in range(num_nodes):
        for j in range(num_nodes):
            if nodes[i] != nodes[j]:            #if not the same node
                common_neighbours = len(set(G.neighbors(nodes[i])) & set(G.neighbors(nodes[j])))#intersection of neighbours of both of them
                common_neighbour_matrix[i, j] = common_neighbours
    return common_neighbour_matrix

def missing_links(G, common_neighbour_matrix):  #gives the missing links, if two nodes have common neighbours greater than 10
    num_nodes = len(G.nodes())
    nodes = list(G.nodes())
    missing_links_result = []

    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            node1, node2 = nodes[i], nodes[j]
            if not G.has_edge(node1, node2) and common_neighbour_matrix[i, j] > 10: # if edge doesn't exist b/w 2 nodes and com. neighbours > 10
                missing_links_result.append([node1, node2]) # append the link to missing links list

    return missing_links_result

missing_links_result = missing_links(G, common_neighbour_matrix(G))
print("Missing links with common neighbors greater than 10:")
for link in missing_links_result:
    print(link)         #print the links one by one
print('There are',len(missing_links_result),'missing links with common neighbors greater than ten')