"""
Fonctions utilitaires pour l'analyse des réseaux Facebook100
"""

import networkx as nx
import numpy as np


def load_facebook_network(filepath):
    """
    Charge un réseau Facebook depuis un fichier .gml
    
    Parameters
    ----------
    filepath : str or Path
        Chemin vers le fichier .gml
        
    Returns
    -------
    G : networkx.Graph
        Graphe non-orienté avec attributs des noeuds
    """
    G = nx.read_gml(filepath)
    return G


def get_largest_connected_component(G):
    """
    Retourne la plus grande composante connexe du graphe
    
    Parameters
    ----------
    G : networkx.Graph
        Graphe d'entrée
        
    Returns
    -------
    G_lcc : networkx.Graph
        Plus grande composante connexe
    """
    if nx.is_connected(G):
        return G
    
    # Trouver toutes les composantes connexes
    components = nx.connected_components(G)
    
    # Récupérer la plus grande
    largest_component = max(components, key=len)
    
    # Créer un sous-graphe avec cette composante
    G_lcc = G.subgraph(largest_component).copy()
    
    return G_lcc


def compute_basic_stats(G):
    """
    Calcule les statistiques de base d'un graphe
    
    Parameters
    ----------
    G : networkx.Graph
        Graphe à analyser
        
    Returns
    -------
    stats : dict
        Dictionnaire des statistiques
    """
    stats = {
        'num_nodes': G.number_of_nodes(),
        'num_edges': G.number_of_edges(),
        'density': nx.density(G),
        'avg_degree': 2 * G.number_of_edges() / G.number_of_nodes()
    }
    
    return stats


def compute_degree_distribution(G):
    """
    Calcule la distribution des degrés
    
    Parameters
    ----------
    G : networkx.Graph
        Graphe à analyser
        
    Returns
    -------
    degrees : list
        Liste des degrés de tous les noeuds
    degree_counts : dict
        Dictionnaire {degré: nombre de noeuds avec ce degré}
    """
    degrees = [degree for node, degree in G.degree()]
    
    # Compter les occurrences de chaque degré
    degree_counts = {}
    for d in degrees:
        degree_counts[d] = degree_counts.get(d, 0) + 1
    
    return degrees, degree_counts


def compute_clustering_metrics(G):
    """
    Calcule les métriques de clustering
    
    Parameters
    ----------
    G : networkx.Graph
        Graphe à analyser
        
    Returns
    -------
    metrics : dict
        Dictionnaire contenant:
        - global_clustering: coefficient de clustering global (transitivité)
        - mean_local_clustering: moyenne des coefficients locaux
        - local_clustering: dict {node: clustering_coefficient}
    """
    # Clustering global (transitivité)
    global_clustering = nx.transitivity(G)
    
    # Clustering local pour chaque noeud
    local_clustering = nx.clustering(G)
    
    # Moyenne des clustering locaux
    mean_local_clustering = np.mean(list(local_clustering.values()))
    
    metrics = {
        'global_clustering': global_clustering,
        'mean_local_clustering': mean_local_clustering,
        'local_clustering': local_clustering
    }
    
    return metrics


def get_degree_clustering_data(G):
    """
    Prépare les données pour le scatter plot degré vs clustering
    
    Parameters
    ----------
    G : networkx.Graph
        Graphe à analyser
        
    Returns
    -------
    degrees : list
        Liste des degrés
    clusterings : list
        Liste des coefficients de clustering correspondants
    """
    degree_dict = dict(G.degree())
    clustering_dict = nx.clustering(G)
    
    nodes = list(G.nodes())
    degrees = [degree_dict[node] for node in nodes]
    clusterings = [clustering_dict[node] for node in nodes]
    
    return degrees, clusterings