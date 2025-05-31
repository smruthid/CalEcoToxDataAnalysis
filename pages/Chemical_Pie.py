import pandas as pd
import streamlit as st
import plotly.graph_objects as go

st.title("Sankey Example")

# Start of Pie chart
st.header("🧬 Interactive Drilldown Pie Chart")

# Load dataset
df = pd.read_csv("toxicity_data.csv")

# Clean missing values
df = df.dropna(subset=["Toxicity Endpoint Type", "Chemical", "Life Cycle Stage"])

# 1st level pie: Endpoint Type
level1_options = df["Toxicity Endpoint Type"].value_counts()
level1_selection = st.selectbox("Select Endpoint Type", level1_options.index)

# 2nd level pie: Chemicals under selected Endpoint Type
subset1 = df[df["Toxicity Endpoint Type"] == level1_selection]
level2_counts = subset1["Chemical"].value_counts().nlargest(10)  # top 10 for clarity
level2_selection = st.selectbox("Select Chemical", level2_counts.index)

# 3rd level pie: Life Cycle Stage under selected Chemical
subset2 = subset1[subset1["Chemical"] == level2_selection]
level3_counts = subset2["Life Cycle Stage"].value_counts()

# Plot level 1 pie
fig1 = go.Figure(data=[go.Pie(labels=level1_options.index, values=level1_options.values, hole=0.3)])
fig1.update_layout(title="Toxicity Endpoint Type Distribution")
st.plotly_chart(fig1)

# Plot level 2 pie
fig2 = go.Figure(data=[go.Pie(labels=level2_counts.index, values=level2_counts.values, hole=0.3)])
fig2.update_layout(title=f"Top Chemicals in '{level1_selection}'")
st.plotly_chart(fig2)

# Plot level 3 pie
fig3 = go.Figure(data=[go.Pie(labels=level3_counts.index, values=level3_counts.values, hole=0.3)])
fig3.update_layout(title=f"Life Cycle Stages for '{level2_selection}'")
st.plotly_chart(fig3)
#End of Pie chart

st.write(
    "testing~"
)

data = pd.read_csv('toxicity_data.csv')
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




