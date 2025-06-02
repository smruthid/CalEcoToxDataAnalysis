import math

import pandas as pd
import streamlit as st
import plotly.graph_objects as go

st.title("Toxicity Sankey")
st.write(
    "For each species, show the studies per chemical and exposure type."
)

############################################
############################################
# Data Cleaning
############################################
############################################
data = pd.read_csv('Data/calecotox_toxicity_data.csv')

############################################
### Clean animal names
############################################
# drop rows where Animal Name is nan
data = data.dropna(subset='Animal Name', axis=0)

name_list = data['Animal Name'].astype(str).sort_values().unique()
name_map = []

# because the list is sorted, can just match entries missing the common name
# with subsequent entries that have it
for i in range(len(name_list)-1):
    if name_list[i] in name_list[i+1] and 'ssp.' not in name_list[i+1]:
        name_map.append({name_list[i] : name_list[i+1]})
        i += 1

for name in name_map:
    data['Animal Name'] = data['Animal Name'].apply(lambda x: name[x] if x in name else x)

# Handle animal names where the common name is not present
name_dict = {}
name_dict['Anas platyrhynchos'] = 'Mallard Duck'
name_dict['Zenaida macroura'] = 'Mourning Dove'
name_dict['Vulpes macrotis ssp. arsipus'] = 'Desert Kit Fox'
name_dict['Dipodomys merriami'] = 'Merriam\'s Kangaroo Rat'
name_dict['Taricha torosa'] = 'California Newt'
name_dict['Pelecanus occidentalis ssp. californicus'] = 'California Brown Pelican'
name_dict['Rallus longirostris ssp. obsoletus'] = 'California Clapper Rail'
name_dict['Pituophis catenifer'] = 'Gopher Snake'
name_dict['Melospiza melodia ssp. pusillula'] = 'Song Sparrow'
name_dict['Dicamptodon tenebrosus'] = 'Coastal Giant Salamander'
name_dict['Enhydra lutris ssp. nereis'] = 'California Sea Otter'
name_dict['Chelonia mydas'] = 'Green Sea Turtle'
name_dict['Egretta thula'] = 'Snowy Egret'

data['Animal Name'] = data['Animal Name'].apply(lambda x: x + f' ({name_dict[x]})' if x in name_dict else x)

############################################
### Clean exposure techniques
############################################

# drop rows where Tox Exposure Technique is nan
data = data.dropna(subset='Tox Exposure Technique', axis=0)

# show pre-cleaning categories
exposure_count = data.groupby('Tox Exposure Technique').count()['Animal Name'].sort_values()
#print(len(exposure_count))

exp_cat_list = []

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
    'contaminated substrate',
    'site contamination (primary uptake via ingestion)',
    'contaminated sediment ingestion',
]
exp_cat_list.append(env_contam)


diet = {}
diet['label'] = 'Diet' 
diet['map'] = [
    'diet (parent)',
    'diet (parental)',
    'diet (via site contamination)',
    'dietary',
    'environmental contamination; diet',
    'diet',
    'dietary via parent regurgitation & self-feeding',
    'ingestion',
    'diet (secondary exposure)',
    'parent diet',
    'parent',
    'ingested fishing weight',
    'ingested fishing weights',
    'consumed mammal bait',
    'parental diet',
]
exp_cat_list.append(diet)

gavage = {}
gavage['label'] = 'Gavage'
gavage['map'] = [
    'oral intubation',
    'intubation',
    'gavage',
    'oral gavage',
    'oral intubation (2 #four shot)\ningestion (field exposure)',
    'oral intubation (lab exposure)\ningestion (field exposure)'
]
exp_cat_list.append(gavage)

waterborne = {}
waterborne['label'] = 'Waterborne'
waterborne['map'] = [
    'waterborne',
    'drinking water',
    'parental drinking water',
    'in bathing water',
    'water-borne; flow-through'
]
exp_cat_list.append(waterborne)

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
]
exp_cat_list.append(ovo)

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
    '2 doses: 0.5 mg/kg each via jugular and medial metatarsal veins',
    'intravenous',
]
exp_cat_list.append(injection)

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
    'egg surface',
    'in ovo, immersion',
    'incubation day 19: egg injection; days 1-29 posthatch: oral gavage',
    'in ovo; oral gavage',
    'in ovo, external application',
    'eggshell surface application',
]
exp_cat_list.append(ovo_exp)

oral = {}
oral['label'] = 'Oral'
oral['map'] = [
    'oral',
    'oral (parent)'
]
exp_cat_list.append(oral)

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
exp_cat_list.append(oral_exp)

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
exp_cat_list.append(field_app)

top_app = {}
top_app['label'] = 'Topical application'
top_app['map'] = {
    'topical to eye',
    'topical application',
    'dorsal application',
    'experimental application'
}
exp_cat_list.append(top_app)

other = {}
other['label'] = 'Other'
other['map'] = {
    'route',
    'computer model',
    'embedded projectile',
    'modeled data',
    'embedded in muscle'
}
exp_cat_list.append(other)

nr = {}
nr['label'] = 'Not recorded'
nr['map'] = {
    'nr',
}
exp_cat_list.append(nr)

mult = {}
mult['label'] = 'Multiple'
mult['map'] = {
    'multiple',
}
exp_cat_list.append(mult)

exp_clean_list = []

env_contam = {}
env_contam['label'] = 'Environmental contamination'
env_contam['map'] = [
    'environmental', 
    'environmental contamination',
    'environmental contaimination', 
    'envrionmental contamination',
]
exp_clean_list.append(env_contam)

diet = {}
diet['label'] = 'Diet (parental)' 
diet['map'] = [
    'diet (parent)',
    'diet (parental)',
    'environmental contamination; diet',
    'dietary via parent regurgitation & self-feeding',
    'parent diet',
    'parent',
    'parental diet',
]
exp_clean_list.append(diet)

im_injection = {}
im_injection['label'] = 'Intramuscular Injection'
im_injection['map'] = [
    'im injection',
    'intramuscular injection',
    'intramuscular',
]
exp_clean_list.append(im_injection)

ovo_sur = {}
ovo_sur['label'] = 'Application to egg surface'
ovo_sur['map'] = [
    'application to egg surface',
    'application to shell surface',
    'application to eggshell surface',
    'topical on eggshell',
    'egg surface',
    'in ovo, external application',
    'eggshell surface application',
]
exp_clean_list.append(ovo_sur)

nr = {}
nr['label'] = 'Not recorded'
nr['map'] = {
    'nr',
}
exp_clean_list.append(nr)

data['Tox Exposure Category'] = data['Tox Exposure Technique']
for exposure in exp_cat_list:
    data['Tox Exposure Category'] = \
        data['Tox Exposure Category'].astype(str).apply(lambda x: exposure['label'] if x.strip().lower() in exposure['map'] else x)

for exposure in exp_clean_list:
    data['Tox Exposure Technique'] = \
        data['Tox Exposure Technique'].astype(str).apply(lambda x: exposure['label'] if x.strip().lower() in exposure['map'] else x[:1].upper() + x[1:])

############################################
############################################
# End of data cleaning
############################################
############################################


sel_value = st.session_state.get("sel_mode", False)
sel_label = (
    "Multiple Selection"
    if sel_value
    else "Single Selection"
)
st.toggle(sel_label, value=sel_value, key='sel_mode')

sel_mode = (
    'multi-row'
    if sel_value
    else 'single-row'
)

name_sel = data.groupby(['Animal Name']).count().reset_index()
event = st.dataframe(
    name_sel[['Animal Name', 'Tox Exposure']],
    hide_index=True,
    column_config={
        'Animal Name': 'Scientific Name (Common Name)',
        'Tox Exposure': 'Num Entries'
    },
    on_select="rerun",
    selection_mode=sel_mode
)

# allow user to drill down like
# select animal -> view sankey diagram of toxins -> exposure method
chemicals = None

if len(event.selection.rows) > 0:
    sel_animals = []
    for row in event.selection.rows:
        sel_animals.append(name_sel.iloc[row]['Animal Name'])
    st.session_state['sel_animal'] = sel_animals
else:
    st.session_state['sel_animal'] = None
    
sel_animals = st.session_state['sel_animal']
if sel_animals is not None:
    if len(sel_animals) == 1:
        animal_name = sel_animals[0]
        st.header(f'{animal_name}')

        animal_entries = data[data['Animal Name'] == animal_name]
        chemicals = animal_entries.groupby(['Chemical', 'Tox Exposure Category', 'Tox Exposure Technique']).count().reset_index()
        #chemicals = animal_entries.sort_values(by=['Chemical', 'Tox Exposure Category', 'Tox Exposure Technique'])

        max_chem = len(animal_entries['Chemical'].unique())

        if max_chem > 1:
            num_chem = st.slider('\# of Chemicals', value=min((10, max_chem)), min_value=1, max_value=max_chem)
            topX = animal_entries.groupby(['Chemical']).count() \
                        .sort_values('Animal Name', ascending=False)[:num_chem]
            topX = list(topX.index)
            chemicals = chemicals[chemicals['Chemical'].isin(topX)].sort_values(by=['Chemical', 'Tox Exposure Category', 'Tox Exposure Technique'])

        toxins = list(chemicals['Chemical'].unique())
        categories = list(chemicals['Tox Exposure Category'].unique())
        exposures = list(chemicals['Tox Exposure Technique'].unique())

        #chem_dim = go.parcats.Dimension(
        #    values = chemicals['Chemical'],
        #    label = 'Chemical'
        #)

        #cat_dim = go.parcats.Dimension(
        #    values = chemicals['Tox Exposure Category'],
        #    label = 'Exposure Category'
        #)

        #tox_dim = go.parcats.Dimension(
        #    values = chemicals['Tox Exposure Technique'],
        #    label = 'Exposure Technique'
        #)

        # each entry is a dict w/three entries: souce, target, value
        # source: toxin index, exposure: exposures index, value: # of counts
        cat_links = chemicals[['Chemical', 'Tox Exposure Category', 'Animal Name']].to_dict('records')
        exp_links = chemicals[['Tox Exposure Category', 'Tox Exposure Technique', 'Animal Name']].to_dict('records')

        colors = ['salmon']*len(toxins) + ['green']*len(categories) + ['seagreen']*len(exposures)

        #fig = go.Figure(data = [go.Parcats(
        #    dimensions = [chem_dim, cat_dim, tox_dim],
        #    hoverinfo = 'count',
        #    line = {'shape': 'hspline'},
        #    )])

        labels = list(toxins) + list(categories) +  list(exposures)
        source = [toxins.index(link['Chemical']) for link in cat_links]
        source = source + [len(toxins) + categories.index(link['Tox Exposure Category']) for link in exp_links]
        target = [len(toxins) + categories.index(link['Tox Exposure Category']) for link in cat_links]
        target = target + [len(toxins) + len(categories) + exposures.index(link['Tox Exposure Technique']) for link in exp_links]

        value = [link['Animal Name'] for link in cat_links]
        value = value + [link['Animal Name'] for link in exp_links]

        fig = go.Figure(data=[go.Sankey(
            node = dict(
                pad = 5,
                thickness = 20,
                #line = dict(color = 'black', width=0.5),
                label = labels,
                color = colors
            ),
            link = dict(
                source = source,
                target = target,
                value = value,
                hovercolor = 'rgba(255, 215, 0, 0.5)',
            ))])

        st.plotly_chart(fig)
    else:
        for animal in sel_animals:
            st.header(f'{animal}')

        chemicals = data.groupby(['Animal Name', 'Chemical', 'Tox Exposure Category']).count().reset_index()
        topX = sel_animals

        chemicals = chemicals[chemicals['Animal Name'].isin(topX)].sort_values(by=['Animal Name', 'Chemical', 'Tox Exposure Category'])

        max_chem = len(chemicals['Chemical'].unique())
        if max_chem > 1:
            num_chem = st.slider('\# of Chemicals', value=min((10, max_chem)), min_value=1, max_value=max_chem)
            topX = chemicals.groupby(['Chemical']).count() \
                        .sort_values('Animal Name', ascending=False)[:num_chem]
            topX = list(topX.index)
            chemicals = chemicals[chemicals['Chemical'].isin(topX)].sort_values(by=['Chemical', 'Tox Exposure Category', 'Tox Exposure Technique'])

        #st.write(chemicals)

        animals = list(chemicals['Animal Name'].unique())
        toxins = list(chemicals['Chemical'].unique())
        categories = list(chemicals['Tox Exposure Category'].unique())

        # each entry is a dict w/three entries: souce, target, value
        # source: toxin index, exposure: exposures index, value: # of counts
        tox_links = chemicals[['Animal Name', 'Chemical', 'Tox Exposure Technique']].to_dict('records')
        cat_links = chemicals[['Chemical', 'Tox Exposure Category', 'Tox Exposure Technique' ]].to_dict('records')

        colors = ['cyan']*len(animals) + ['salmon']*len(toxins) + ['green']*len(categories)

        labels = list(animals) + list(toxins) +  list(categories)
        source = [animals.index(link['Animal Name']) for link in tox_links]
        source = source + [len(animals) + toxins.index(link['Chemical']) for link in cat_links]
        target = [len(animals) + toxins.index(link['Chemical']) for link in tox_links]
        target = target + [len(animals) + len(toxins) + categories.index(link['Tox Exposure Category']) for link in cat_links]

        value = [link['Tox Exposure Technique'] for link in tox_links]
        value = value + [link['Tox Exposure Technique'] for link in cat_links]

        #animal_dim = go.parcats.Dimension(
        #    values = chemicals['Animal Name'],
        #    label = 'Animal Name'
        #)

        #chem_dim = go.parcats.Dimension(
        #    values = chemicals['Chemical'],
        #    label = 'Chemical'
        #)

        #cat_dim = go.parcats.Dimension(
        #    values = chemicals['Tox Exposure Category'],
        #    label = 'Exposure Category'
        #)

        #tox_dim = go.parcats.Dimension(
        #    values = list(chemicals['Tox Exposure Technique'].unique()),
        #    label = 'Exposure Technique'
        #)

        #fig = go.Figure(data = [go.Parcats(
        #    dimensions = [animal_dim, chem_dim, cat_dim],
        #    hoverinfo = 'count',
        #    line = {'shape': 'hspline'},
        #    )])

        fig = go.Figure(data=[go.Sankey(
            arrangement = 'perpendicular',
            node = dict(
                pad = 5,
                thickness = 20,
                line = dict(color = 'black', width=0.5),
                label = labels,
                color = colors
            ),
            link = dict(
                source = source,
                target = target,
                value = value,
                hovercolor = 'rgba(255, 215, 0, 0.5)',
            ))],
            layout=go.Layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            ))

        st.plotly_chart(fig)
        

else:
    st.header(f'Top Animals, Chemicals, and Exposure')

    col1, col2 = st.columns(2)

    with col1:
        num_anim = st.slider('\# of Animals', value=5, min_value=1, max_value=25)

    chemicals = data.groupby(['Animal Name', 'Chemical', 'Tox Exposure Category']).count().reset_index()
    #chemicals = data.sort_values(by=['Chemical', 'Tox Exposure Category', 'Tox Exposure Technique'])
    topX = data.groupby(['Animal Name']).count() \
                .sort_values('Tox Exposure Technique', ascending=False)[:num_anim]
    topX = list(topX.index)

    chemicals = chemicals[chemicals['Animal Name'].isin(topX)].sort_values(by=['Animal Name', 'Chemical', 'Tox Exposure Category'])

    with col2:
        num_chem = st.slider('\# of Chemicals', value=5, min_value=1, max_value=15)

    topX = chemicals.groupby(['Chemical']).count() \
                .sort_values('Tox Exposure Technique', ascending=False)[:num_chem]
    topX = list(topX.index)
    chemicals = chemicals[chemicals['Chemical'].isin(topX)].sort_values(by=['Animal Name', 'Chemical', 'Tox Exposure Category'])
    #st.write(chemicals)

    animals = list(chemicals['Animal Name'].unique())
    toxins = list(chemicals['Chemical'].unique())
    categories = list(chemicals['Tox Exposure Category'].unique())

    # each entry is a dict w/three entries: souce, target, value
    # source: toxin index, exposure: exposures index, value: # of counts
    tox_links = chemicals[['Animal Name', 'Chemical', 'Tox Exposure Technique']].to_dict('records')
    cat_links = chemicals[['Chemical', 'Tox Exposure Category', 'Tox Exposure Technique' ]].to_dict('records')

    colors = ['cyan']*len(animals) + ['salmon']*len(toxins) + ['green']*len(categories)

    labels = list(animals) + list(toxins) +  list(categories)
    source = [animals.index(link['Animal Name']) for link in tox_links]
    source = source + [len(animals) + toxins.index(link['Chemical']) for link in cat_links]
    target = [len(animals) + toxins.index(link['Chemical']) for link in tox_links]
    target = target + [len(animals) + len(toxins) + categories.index(link['Tox Exposure Category']) for link in cat_links]

    value = [link['Tox Exposure Technique'] for link in tox_links]
    value = value + [link['Tox Exposure Technique'] for link in cat_links]

    #animal_dim = go.parcats.Dimension(
    #    values = chemicals['Animal Name'],
    #    label = 'Animal Name'
    #)

    #chem_dim = go.parcats.Dimension(
    #    values = chemicals['Chemical'],
    #    label = 'Chemical'
    #)

    #cat_dim = go.parcats.Dimension(
    #    values = chemicals['Tox Exposure Category'],
    #    label = 'Exposure Category'
    #)

    #tox_dim = go.parcats.Dimension(
    #    values = list(chemicals['Tox Exposure Technique'].unique()),
    #    label = 'Exposure Technique'
    #)

    #fig = go.Figure(data = [go.Parcats(
    #    dimensions = [animal_dim, chem_dim, cat_dim],
    #    hoverinfo = 'count',
    #    line = {'shape': 'hspline'},
    #    )])

    fig = go.Figure(data=[go.Sankey(
        arrangement = 'perpendicular',
        node = dict(
            pad = 5,
            thickness = 20,
            line = dict(color = 'black', width=0.5),
            label = labels,
            color = colors
        ),
        link = dict(
            source = source,
            target = target,
            value = value,
            hovercolor = 'rgba(255, 215, 0, 0.5)',
        ))])

    st.plotly_chart(fig)

#css = (
#r'.node-label {'
#r'    font-family: "Source Sans Pro"'
#r'    fill: rgb(68, 68, 68) !important;'
#r'    text-shadow: none !important;'
#r'}'
#)
css = (
r'.node-label {'
r'    cursor: default; '
r'    font-family: "Source Sans Pro", sans-serif !important; '
r'    font-size: 12px; '
r'    fill: rgb(230, 234, 241) !important; '
r'    fill-opacity: 1 !important; '
r'    font-weight: normal !important; '
r'    font-style: normal !important; '
r'    font-variant: normal !important; '
r'    text-shadow: rgb(68, 68, 68) 1px 1px 1px, rgb(68, 68, 68) -1px -1px 1px, rgb(68, 68, 68) 1px -1px 1px, rgb(68, 68, 68) -1px 1px 1px !important; '
r'    white-space: pre;'
r'}'
)
print(css)
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
