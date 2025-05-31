import pandas as pd
import streamlit as st
import plotly.graph_objects as go

st.title("Toxicity Sankey")
st.write(
    "For each species, show common exposure methods associated with chemicals"
)

data = pd.read_csv('Data/calecotox_toxicity_data.csv')
name_unique = data['Animal Name'].unique()
event = st.dataframe(
    name_unique,
    on_select="rerun",
    selection_mode="single-row"
)

# allow user to drill down like
# select animal -> view sankey diagram of toxins -> exposure method

if len(event.selection.rows) > 0:
    animal_name = name_unique[event.selection.rows].item()
    st.header(f'{animal_name}')

    animal_entries = data[data['Animal Name'] == animal_name]
    chemicals = animal_entries.groupby(['Chemical', 'Tox Exposure Technique']).count().reset_index()

    top10 = animal_entries.groupby(['Chemical']).count() \
                .sort_values('Animal Name', ascending=False)[:10]

    top10 = list(top10.index)
    chemicals = chemicals[chemicals['Chemical'].isin(top10)]

    toxins = list(chemicals['Chemical'].unique())
    exposures = list(chemicals['Tox Exposure Technique'].unique())

    #toxins
    #exposures

    # each entry is a dict w/three entries: source, exposure, value
    # source: toxin index, exposure: exposures index, value: # of counts
    links = chemicals[['Chemical', 'Tox Exposure Technique', 'Animal Name']].to_dict('records')

    colors = ['cyan']*len(toxins) + ['green']*len(exposures)

    labels = list(toxins) + list(exposures)
    source = [toxins.index(link['Chemical']) for link in links]
    target = [len(toxins) + exposures.index(link['Tox Exposure Technique']) for link in links]
    value = [link['Animal Name'] for link in links]

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
            value = value
        ))])

    fig.update_layout(title_text='Toxin Sankey', font_size=10)
    st.plotly_chart(fig)




