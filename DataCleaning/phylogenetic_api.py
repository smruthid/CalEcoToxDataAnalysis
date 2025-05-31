import pandas as pd
import numpy as np
import time
import requests
import xml.etree.ElementTree as ET
import os


df = pd.read_csv('../Data/calecotox_toxicity_data.csv')

split_data = df['Animal Name'].str.split('(', expand=True)

df['Scientific Name'] = split_data[0].str.strip()
df['Common Name'] = split_data[1].str.replace(')', '').str.strip()
df = df.drop(columns=['Animal Name'])

# Remove the columns and insert them at the beginning
common_col = df.pop('Common Name')
scientific_col = df.pop('Scientific Name')

df.insert(0, 'Common Name', common_col)
df.insert(1, 'Scientific Name', scientific_col)

df = df.dropna(subset=['Scientific Name'])
my_dict = dict(zip(df['Scientific Name'], df['Common Name']))

values_to_delete = []

for name in my_dict:
    if 'ssp.' in name:
        clean_name = name.split(' ssp. ')[0]
        if clean_name in my_dict:
            values_to_delete.append(name)

for key in values_to_delete:
    my_dict.pop(key, None)

scientific_list = list(my_dict.keys())

def clean_name(name):
    return name.replace(' ', '+')


    

headers = {
    "Accept": "application/xml"
}

search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"  

tree = ['class', 'order', 'family', 'genus', 'species']
tree_df = pd.DataFrame()
for name in scientific_list:
    get_id_params = {
        "db": "taxonomy",
        "term": clean_name(name)
    }
    id_response = requests.get(search_url, params=get_id_params, headers=headers)
    if id_response.status_code == 200:
        id_root = ET.fromstring(id_response.content)
        id_val = id_root.find('.//Id')
        if id_val != None:
            get_full_data_params = {
                "db": "taxonomy",
                "id": id_val.text
            }
            full_data_response = requests.get(fetch_url, params=get_full_data_params, headers=headers)
            if full_data_response.status_code == 200:
                root = ET.fromstring(full_data_response.content)
                lineage_taxons = root.findall('.//LineageEx/Taxon')
                data_dict = {
                    'species': name
                }
                for taxon in lineage_taxons:
                    rank_element = taxon.find('Rank')
                    scientific_name = taxon.find('ScientificName')
                    if rank_element is not None and rank_element.text in tree:
                        data_dict[rank_element.text] = scientific_name.text
                new_row = pd.DataFrame([data_dict])
                tree_df = pd.concat([tree_df, new_row], ignore_index=True)
        time.sleep(0.5)
        print(name)
    else:
        print("No data found")

tree_df = tree_df.reset_index(drop=True)

os.makedirs('../Data', exist_ok=True)
tree_df.to_csv('../Data/PhylogeneticTreeData.csv')

animal_names = [
    "Anas platyrhynchos", 
    "Falco sparverius", 
    "Chelonia mydas", 
    "Phalacrocorax auritus", 
    "Turdus migratorius",
    "Falco peregrinus",
    "Enhydra lutris",
    "Zalophus californianus",
    "Egretta thula",
    "Sceloporus occidentalis"
]

tree_df_filtered = tree_df[tree_df['species'].isin(animal_names)]
tree_df_filtered = tree_df_filtered.reset_index(drop=True)
tree_df_filtered.to_csv('../Data/FilteredPhylogeneticTreeData.csv')