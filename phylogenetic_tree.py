import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram
from scipy.spatial.distance import squareform

def calculate_taxonomic_distance(species1, species2):   
    if species1['species'] == species2['species']:
        return 0
    if species1['genus'] == species2['genus']:
        return 1
    if species1['family'] == species2['family']:
        return 2
    if species1['order'] == species2['order']:
        return 3
    if species1['class'] == species2['class']:
        return 4
    return 5

def create_pairwise_distance_matrix(csv_name):
    df = pd.read_csv(csv_name)
    n_species = len(df)
    
    distance_matrix = np.zeros((n_species, n_species))
    
    # Calculate distances
    for i in range(n_species):
        for j in range(i + 1, n_species):
            distance = calculate_taxonomic_distance(df.iloc[i], df.iloc[j])
            distance_matrix[i, j] = distance
            distance_matrix[j, i] = distance
    
    return distance_matrix, df['species'].tolist()

# Usage
location = "Data/FilteredPhylogeneticTreeData.csv"
distance_matrix, species_names = create_pairwise_distance_matrix(location)

def create_tree_from_distance_matrix(csv_name, distance_matrix, species_names):

    df = pd.read_csv(csv_name)    

    condensed_distances = squareform(distance_matrix)
    linkage_matrix = linkage(condensed_distances, method='complete')
    
    plt.figure(figsize=(16, 12))
    dend = dendrogram(
        linkage_matrix,
        labels=species_names,
        orientation='right',
        leaf_font_size=10
    )
    
    # Get the actual x-axis limits to understand the dendrogram scale
    ax = plt.gca()
    x_min, x_max = ax.get_xlim()
    
    # Get the actual y-tick positions where species names are displayed
    ytick_positions = ax.get_yticks()
    ytick_labels = [label.get_text() for label in ax.get_yticklabels()]
    
    # Create mapping from species name to y-position
    species_y_positions = {}
    for pos, label in zip(ytick_positions, ytick_labels):
        if label in species_names:
            species_y_positions[label] = pos
    
    # Hide the original y-tick labels and add them on the right side
    ax.set_yticklabels([])
    
    # NOW add species names on the right side (after axis inversion)
    for species_name, y_pos in species_y_positions.items():
        plt.text(-0.1, y_pos, species_name,  # Changed from -0.1 to 0.1
                ha='left', va='center', fontsize=10)  # Changed from ha='right' to ha='left'
    
    # Map your distance values to actual x-positions in the dendrogram
    max_distance = 5
    distance_to_x = {}
    for dist in [1, 2, 3, 4]:
        distance_to_x[dist] = x_min + (dist / max_distance) * (x_max - x_min)
    
    # Now add taxonomic labels at the correct positions
    for species_name, y_pos in species_y_positions.items():
        species_row = df[df['species'] == species_name].iloc[0]
        
        # Add genus label at actual distance 1 position
        if pd.notna(species_row['genus']):
            x_pos = distance_to_x[1] + 0.1
            plt.text(x_pos, y_pos, species_row['genus'], 
                    ha='right', va='center', fontsize=12, 
                    bbox=dict(boxstyle="round,pad=0.1", facecolor='lightblue', alpha=0.7))
        
        # Add family label at actual distance 2 position
        if pd.notna(species_row['family']):
            x_pos = distance_to_x[2] + 0.1
            plt.text(x_pos, y_pos, species_row['family'], 
                    ha='right', va='center', fontsize=12,
                    bbox=dict(boxstyle="round,pad=0.1", facecolor='lightgreen', alpha=0.7))
        
        # Add order label at actual distance 3 position
        if pd.notna(species_row['order']):
            x_pos = distance_to_x[3] + 0.1
            plt.text(x_pos, y_pos, species_row['order'], 
                    ha='right', va='center', fontsize=12,
                    bbox=dict(boxstyle="round,pad=0.1", facecolor='lightyellow', alpha=0.7))
        
        # Add class label at actual distance 4 position
        if pd.notna(species_row['class']):
            x_pos = distance_to_x[4] + 0.1
            plt.text(x_pos, y_pos, species_row['class'], 
                    ha='right', va='center', fontsize=12,
                    bbox=dict(boxstyle="round,pad=0.1", facecolor='lightcoral', alpha=0.7))
    
    # Invert the x-axis so 0 is on the right and distances increase to the left
    ax.invert_xaxis()
    
    # Add vertical reference lines at the actual taxonomic distance values (after inversion)
    for distance in [1, 2, 3, 4]:
        plt.axvline(x=distance, color='gray', linestyle='--', alpha=0.3)
    
    plt.title('Taxonomic Tree with Hierarchical Labels')
    plt.xlabel('Taxonomic Distance')
    plt.tight_layout()
    plt.show()
    
    return linkage_matrix

linkage_matrix = create_tree_from_distance_matrix(location, distance_matrix, species_names)