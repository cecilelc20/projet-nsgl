"""
Script simple d'exploration des données Facebook100
"""

import networkx as nx
import numpy as np
from pathlib import Path


def main():
    # Trouver le répertoire data
    possible_paths = [Path("../data"), Path("./data"), Path("../../data"), Path("/mnt/project")]
    
    data_dir = None
    for path in possible_paths:
        if path.exists() and list(path.glob("*.gml")):
            data_dir = path
            break
    
    if not data_dir:
        print("Répertoire data non trouvé!")
        return
    
    gml_files = sorted(list(data_dir.glob("*.gml")))
    
    print("=" * 80)
    print(f"FICHIERS TROUVÉS: {len(gml_files)} fichiers .gml")
    print("=" * 80)
    
    # Afficher 1 fichier complet en détail
    print("\n" + "=" * 80)
    print(f"ANALYSE DÉTAILLÉE: {gml_files[0].name}")
    print("=" * 80)
    
    G = nx.read_gml(gml_files[0])
    
    print(f"\nType: {type(G).__name__}")
    print(f"Orienté: {G.is_directed()}")
    print(f"Nœuds: {G.number_of_nodes()}")
    print(f"Arêtes: {G.number_of_edges()}")
    print(f"Densité: {nx.density(G):.6f}")
    
    # Composantes
    if G.is_directed():
        n_comp = nx.number_weakly_connected_components(G)
        lcc_size = len(max(nx.weakly_connected_components(G), key=len))
    else:
        n_comp = nx.number_connected_components(G)
        lcc_size = len(max(nx.connected_components(G), key=len))
    
    print(f"Composantes connexes: {n_comp}")
    print(f"Plus grande composante: {lcc_size}")
    
    # Attributs des nœuds
    print("\n--- ATTRIBUTS DES NŒUDS ---")
    sample_node = list(G.nodes())[0]
    attrs = G.nodes[sample_node]
    
    print(f"Attributs disponibles: {list(attrs.keys())}")
    print("\nDétails:")
    
    for attr_name in attrs.keys():
        values = [G.nodes[n].get(attr_name) for n in G.nodes() if G.nodes[n].get(attr_name) is not None]
        
        if not values:
            continue
        
        print(f"\n  {attr_name}:")
        print(f"    Type: {type(values[0]).__name__}")
        print(f"    Valeurs non-nulles: {len(values)}/{G.number_of_nodes()}")
        
        if isinstance(values[0], (int, float)):
            print(f"    Min: {min(values)}, Max: {max(values)}")
            print(f"    Moyenne: {np.mean(values):.2f}")
            unique = len(set(values))
            print(f"    Valeurs uniques: {unique}")
        else:
            unique = set(values)
            print(f"    Valeurs uniques: {len(unique)}")
            if len(unique) <= 10:
                print(f"    Valeurs: {sorted(unique)}")
    
    # 3 nœuds exemples
    print("\n--- 3 NŒUDS EXEMPLES ---")
    for node in list(G.nodes())[:3]:
        print(f"\nNœud {node}: degré={G.degree(node)}")
        for key, val in G.nodes[node].items():
            print(f"  {key}: {val}")
    
    # Stats globales rapides sur quelques fichiers
    print("\n" + "=" * 80)
    print("STATISTIQUES RAPIDES (10 premiers fichiers)")
    print("=" * 80)
    
    print(f"\n{'Fichier':<35} {'Nœuds':>8} {'Arêtes':>10} {'Densité':>10}")
    print("-" * 70)
    
    for f in gml_files[:10]:
        try:
            G_temp = nx.read_gml(f)
            print(f"{f.stem[:34]:<35} {G_temp.number_of_nodes():>8} {G_temp.number_of_edges():>10} {nx.density(G_temp):>10.6f}")
        except:
            print(f"{f.stem[:34]:<35} {'ERREUR':>8}")
    
    print("\n" + "=" * 80)
    print(f"Total: {len(gml_files)} fichiers disponibles")
    print("=" * 80)


if __name__ == "__main__":
    main()