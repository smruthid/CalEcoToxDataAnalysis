import pandas as pd

pd.set_option('display.max_rows', None)
data = pd.read_csv('toxicity_data.csv')

#### CLEAN ANIMAL NAMES
# drop rows where Animal Name is nan
data = data.dropna(subset='Animal Name', axis=0)

# show pre-cleaning animal species
#species_count = data.groupby('Animal Name').count()[0].sort_values()
#print

name_list = data['Animal Name'].astype(str).sort_values().unique()
name_map = []

## because it's nicely sorted, can just match entries with the next one
for i in range(len(name_list)-1):
    if name_list[i] in name_list[i+1] and 'ssp.' not in name_list[i+1]:
        name_map.append({name_list[i] : name_list[i+1]})
        i += 1

for name in name_map:
    data['Animal Name'] = data['Animal Name'].apply(lambda x: name[x] if x in name else x)

#### CLEAN EXPOSURE TECHNIQUES
# drop rows where Tox Exposure Technique is nan
data = data.dropna(subset='Tox Exposure Technique', axis=0)

# show pre-cleaning categories
exposure_count = data.groupby('Tox Exposure Technique').count()['Animal Name'].sort_values()
#print(len(exposure_count))

exp_clean_list = []

env_contam = {}
env_contam['label'] = 'Environmental contamination'
env_contam['map'] = [
    'environmental', 
    'environmental contamination',
    'environmental contaimination', 
    'environmental contamination leads to altered porphyrinogen levels',
    'environmental exposure', 
    'site contamination',
    'habitat contamination',
    'envrionmental contamination',
    'contaminated substrate'
]
exp_clean_list.append(env_contam)

diet = {}
diet['label'] = 'Diet' 
diet['map'] = [
    'diet (parent)',
    'diet (parental)',
    'diet (via site contamination)',
    'dietary',
    'diet',
    'dietary via parent regurgitation & self-feeding',
    'environmental contamination; diet',
    'ingestion'
]
exp_clean_list.append(diet)

gavage = {}
gavage['label'] = 'Gavage'
gavage['map'] = [
    'oral intubation',
    'intubation',
    'gavage',
    'oral gavage'
]
exp_clean_list.append(gavage)

waterborne = {}
waterborne['label'] = 'Waterborne'
waterborne['map'] = [
    'waterborne',
    'drinking water',
    'parental drinking water',
    'in bathing water',
    'water-borne; flow-through'
]
exp_clean_list.append(waterborne)

ovo = {}
ovo['label'] =  'In ovo'
ovo['map'] = [
    'in ovo',
    'in ovo via maternal transfer',
    'in ovo via maternal transfer from previous year exposure',
    'parental diet (in ovo)',
    'in ovo & via parental exposure',
    'maternal diet',
    'parental transfer',
    'parental diet'
]
exp_clean_list.append(ovo)

injection = {}
injection['label'] = 'Injection'
injection['map'] = [
    'im injection',
    'im injection followed by iv 1 m later',
    'im injection followed by iv 2 w later',
    'intramuscular injection',
    'intraperitoneal injection',
    'intraperitoneal',
    'subcutaneous injection',
    'injection',
    'subcutaneous injection following sedation, surgery, recovery',
    'intracoelmic injection',
    'intramuscular',
    '2 doses: 0.5 mg/kg each via jugular and medial metatarsal veins'
]
exp_clean_list.append(injection)

ovo_exp = {}
ovo_exp['label'] = 'In ovo; experimental'
ovo_exp['map'] = [
    'egg yolk injection',
    'in ovo injection',
    'egg immersion',
    'application to egg surface',
    'egg injection',
    'application to shell surface',
    'application to eggshell surface',
    'topical on eggshell',
    'egg immersion in solution',
    'in ovo, immersion',
    'in ovo, external application',
    'eggshell surface application',
]
exp_clean_list.append(ovo_exp)

oral = {}
oral['label'] = 'Oral'
oral['map'] = [
    'oral'
]
exp_clean_list.append(oral)

oral_exp = {}
oral_exp['label'] = 'Oral; experimental'
oral_exp['map'] = [
    'oral via coated artichoke bracts',
    'oral capsule',
    'oral capsules; divided doses',
    'oral (capsule)',
    'oral via food pellets',
    'oral via capsule',
]
exp_clean_list.append(oral_exp)

field_app = {}
field_app['label'] = 'Field application'
field_app['map'] = [
    'field application',
    'treatment of nest-containing trees',
    'spiked nest material',
    'spray',
    'field-applied',
    'pesticide application (late fall)',
    'application to habitat',
    'pesticide application',
    'pesticide application; subjects walked 50, 150, or 300 m through application areas',
    'ambient overspray',
    'spray application to habitat'
]
exp_clean_list.append(field_app)

top_app = {}
top_app['label'] = 'Topical application'
top_app['map'] = {
    'topical to eye',
    'topical application',
    'dorsal application'
}
exp_clean_list.append(top_app)

for exposure in exp_clean_list:
    data['Tox Exposure Technique'] = \
        data['Tox Exposure Technique'].astype(str).apply(lambda x: exposure['label'] if x.lower() in exposure['map'] else x)

# show post-cleaning categories
exposure_count = data.groupby('Tox Exposure Technique').count()['Animal Name'].sort_values()
#print(len(exposure_count))
