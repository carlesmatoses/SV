import app as st
import pandas as pd
import numpy as np
import streamlit as st
import altair as alt
from vega_datasets import data as vega_data
st. set_page_config(layout="wide")

col1 = st.columns(1)


# import stored dataset
country_lists = pd.read_csv('country_lists_enriched.csv')

################################
################################
################################
################################
## Q1
# prepare dataframe
df = country_lists.copy()
highlight = alt.selection_point(fields=['country'], on='click', clear='true')

# Melt each metric separately
visa_free_count = df.melt(
    id_vars=['country', 'region'],
    value_vars=[col for col in df.columns if col.startswith('year_visa_free_count_')],
    var_name='year',
    value_name='visa_free_count'
)
visa_free_count['year'] = visa_free_count['year'].str.replace('year_visa_free_count_', '')

per_million = df.melt(
    id_vars=['country', 'region'],
    value_vars=[col for col in df.columns if col.startswith('year_visa_free_per_million_')],
    var_name='year',
    value_name='visa_free_per_million'
)
per_million['year'] = per_million['year'].str.replace('year_visa_free_per_million_', '')

normalized = df.melt(
    id_vars=['country', 'region'],
    value_vars=[col for col in df.columns if col.startswith('year_visa_free_per_population_')],
    var_name='year',
    value_name='visa_free_per_population'
)
normalized['year'] = normalized['year'].str.replace('year_visa_free_per_population_', '')

# Merge all three melted DataFrames on country, region, and year
long_df = visa_free_count.merge(per_million, on=['country', 'region', 'year'])
long_df = long_df.merge(normalized, on=['country', 'region', 'year'])

# change year from string to integer
long_df['year'] = long_df['year'].astype(int) 

# Streamlit UI for metric and year selection
metric_labels = {
    'visa_free_count': 'Visa-Free Count',
    'visa_free_per_population': 'Visa-Free per Population',
    'visa_free_per_million': 'Visa-Free per Million'
}

with col1[0]:
    st.subheader("Controls")
    metric = st.selectbox(
        "Visa Free Waighting Method :",
        options=list(metric_labels.keys()),
        format_func=lambda x: metric_labels[x]
)

with col1[0]:
    year = st.slider("Year:", min_value=2006, max_value=2025, value=2021, step=1)

# Prepare data for selected metric and year
long_df_filtered = long_df[long_df['year'] == year]

# Melt for selected metric only
strip_df = long_df_filtered[['country', 'region', 'year', metric]].copy()
strip_df = strip_df.rename(columns={metric: 'value'})
strip_df['metric'] = metric

# Add jitter for strip plot
strip_df['jitter'] = (
    strip_df['country'].str[0]
    .apply(lambda x: (ord(x) % 20) / 100 - 0.1)
)

# Strip chart
strip_chart = alt.Chart(strip_df).mark_circle(size=60, opacity=0.6).encode(
    x=alt.X('region:N', title='Continent'),
    y=alt.Y(
        'value:Q',
        title='Visa-Free Destinations',
        scale=alt.Scale(type='pow', exponent=0.5),
        axis=alt.Axis(labelLimit=200, labelFontSize=10, labelPadding=10, format="~s")
    ),
    color=alt.condition(highlight, 'region:N', alt.value('lightgray')),
    opacity=alt.condition(highlight, alt.value(1), alt.value(0.3)),
    tooltip=['country', 'region', 'year', 'value'],
    xOffset=alt.XOffset('jitter:Q', scale=alt.Scale(domain=[-0.2, 0.2]))
).add_params(
    highlight
).properties(
    title=f'Visa-Free Destinations by Continent ({year}, {metric_labels[metric]})',
    width=200,
    height=400
)

# Mean line
mean_value = strip_df.groupby('region')['value'].mean().reset_index()
mean_line = alt.Chart(mean_value).mark_rule(
    color='black',
    strokeDash=[4,2]
).encode(
    x=alt.X('region:N'),
    y='value:Q',
    tooltip=[alt.Tooltip('region:N'), alt.Tooltip('value:Q', title='Mean')],
)

# Combine and display
q1 = alt.layer(strip_chart, mean_line).resolve_scale(y='shared').properties(
    title=alt.TitleParams(
        text=f'Visa-Free Destinations by Continent ({year}, {metric_labels[metric]})',
        anchor="middle"
    )
)
# st.altair_chart(q1, use_container_width=False)

################################
################################
################################
################################
## Q2

# Define color scheme
continent_color = alt.Color('region:N', title='Continent')

# Prepare data
data = country_lists.copy()
data_selected = data[['country', 'year_visa_free_count_2006', 'year_visa_free_count_2021', 'region']].copy()
data_selected = data_selected.rename(columns={
    'year_visa_free_count_2006': 'count_2006',
    'year_visa_free_count_2021': 'count_2021'
})

# Compute changes and ranks
data_selected['change'] = data_selected['count_2021'] - data_selected['count_2006']
changes = data_selected.sort_values('change', ascending=False).reset_index(drop=True)
changes['rank'] = changes.index

# Melt long for slope chart
changes_long = changes.melt(
    id_vars=['country', 'region', 'change', 'rank'],
    value_vars=['count_2006', 'count_2021'],
    var_name='year',
    value_name='visa_free_count'
)
changes_long['year'] = changes_long['year'].map({'count_2006': '2006', 'count_2021': '2021'})

with col1[0]:
    start_rank, end_rank = st.slider(
        "Select rank range:",
        min_value=0,
        max_value=len(changes),
        value=(0, 10),
        step=1,
        help="Filter which ranked countries (by change in visa-free access) to show"
    )

# Filter data in Python (faster + avoids complicated Altair transforms)
filtered_data = changes_long[(changes_long['rank'] >= start_rank) & (changes_long['rank'] < end_rank)]

base = alt.Chart(filtered_data).encode(
    y=alt.Y(
        'country:N',
        title='Country',
        sort=alt.EncodingSortField(field='change', order='descending'),
        axis=alt.Axis(labelLimit=200)
    ),
    x=alt.X('change:Q', title='Visa-Free Destinations (Change 2006–2021)'),
    color=alt.condition(highlight, 'region:N', alt.value('lightgray')),
    opacity=alt.condition(highlight, alt.value(1), alt.value(0.3)),
    tooltip=['country', 'region', 'year', 'visa_free_count', 'change']
).transform_filter(
    alt.datum.year == '2021'
).add_params(
    highlight
)

bars = base.mark_bar()
text_labels = base.mark_text(align='left', dx=3).encode(
    text=alt.Text('change:Q', format='+d')
)

bar_chart = (bars + text_labels).properties(
    title='Visa-Free Change (2006–2021)',
    width=300,
    height=400
)

slope_chart = alt.Chart(filtered_data).encode(
    y=alt.Y(
        'country:N',
        sort=alt.EncodingSortField(field='change', order='descending'),
        axis=None
    ),
    x=alt.X('visa_free_count:Q', title='Visa-Free Destinations'),
    color=alt.condition(highlight, 'region:N', alt.value('lightgray')),
    opacity=alt.condition(highlight, alt.value(1), alt.value(0.3)),
    detail='country:N',
    tooltip=['country', 'region', 'year', 'visa_free_count', 'change']
).add_params(
    highlight
)

lines = slope_chart.mark_line(point=True, size=3)

slope_chart_final = lines.properties(
    title='Change Over Time (2006 → 2021)',
    width=250,
    height=400
)

q2 = alt.hconcat(bar_chart, slope_chart_final).resolve_scale(color='shared').properties(
    title=alt.TitleParams(
        text="Countries with Greatest Changes in Visa-Free Access (2006–2021)",
        anchor="middle"
    )
)


# st.altair_chart(q2, use_container_width=True)



################################
################################
################################
################################
## Q3

df = country_lists.copy()

# Melt visa_free_count columns for all years
visa_free_count = df.melt(
    id_vars=['country', 'region'],
    value_vars=[col for col in df.columns if col.startswith('year_visa_free_count_')],
    var_name='year',
    value_name='visa_free_count'
)
visa_free_count['year'] = visa_free_count['year'].str.replace('year_visa_free_count_', '').astype(int)

# remove unwanted years
visa_free_count = visa_free_count[~visa_free_count['year'].isin([2007, 2009])]

all_years = sorted(visa_free_count['year'].unique())

# Mean per region (continent lines)
mean_per_region = visa_free_count.groupby(['region', 'year'])['visa_free_count'].mean().reset_index()

parallel_chart = alt.Chart(visa_free_count).mark_line(opacity=0.15).encode(
    x=alt.X('year:Q', title='Year', axis=alt.Axis(values=all_years)),
    y=alt.Y('visa_free_count:Q', title='Visa-Free Count'),
    color=alt.condition(highlight, 'region:N', alt.value('lightgray')),
    opacity=alt.condition(highlight, alt.value(0.15), alt.value(0.05)),
    detail='country:N',
    tooltip=['country', 'region', 'year', 'visa_free_count']
).add_params(
    highlight
).properties(
    width=700,
    height=400
)

continent_chart = alt.Chart(mean_per_region).mark_line(point=True, size=3, opacity=1).encode(
    x=alt.X('year:Q', title='Year', axis=alt.Axis(values=all_years)),
    y=alt.Y('visa_free_count:Q', title='Mean Visa-Free Count'),
    color=continent_color,
    tooltip=['region', 'year', 'visa_free_count']
).properties(
    width=700,
    height=400
)

q3 = alt.layer(continent_chart, parallel_chart).resolve_scale(
    x='shared',
    y='shared'
).properties(
    title='Visa-Free Destinations Over Time: Countries (faint) and Continents (bold)',
    width=400,
    height=400
).interactive()

# st.altair_chart(q3, use_container_width=True)



################################
################################
################################
################################
## Q4


# Load world topojson from Vega datasets
world_map = alt.topo_feature(vega_data.world_110m.url, 'countries')

# Prepare country data for 2021
country_counts = country_lists.copy()

color = alt.Color(
    'us_access_type:N',
    title='US Access Type',
    scale=alt.Scale(
        domain=[
            'visa_required',
            'electronic_travel_authorisation',
            'visa_online',
            'visa_on_arrival',
            'visa_free_access',
            'unknown',
            'US',
            'Schengen Area'
        ],
        range=[
            "#c6dbef",
            "#6baed6",
            "#3182bd",
            "#08519c",
            "#08306b",
            "#fdae61",
            "#e87c7e",
            "#31a354",
        ]
    )
)

geo_chart = alt.Chart(world_map).mark_geoshape().transform_lookup(
    lookup='id',
    from_=alt.LookupData(
        data=country_counts,
        key='iso_numeric',
        fields=['iso_numeric', 'us_access_type_code', 'us_access_type', 'country']
    )
).encode(
    tooltip=['id:N', 'country:N', 'us_access_type:N'],
    color=color
).project(
    type='naturalEarth1'
).properties(
    title='US Access Type per Country (2021)',
    width=600,
    height=500
)

us_highlight = alt.Chart(world_map).mark_geoshape(
    fill=None,
    stroke='black',
    strokeWidth=0.5
).transform_filter(
    alt.datum.id == 840
).project(
    type='naturalEarth1'
)

schengen_iso_codes = [
    40, 56, 100, 191, 203, 208, 233, 246, 250, 276, 300, 348, 352, 372, 380, 428, 440, 442, 528, 578, 616, 620, 703, 705, 724, 752, 756, 807
]

schengen_highlight = alt.Chart(world_map).mark_geoshape(
    fill=None,
    stroke="#2d6205",
    strokeWidth=1,
    opacity=0.5
).transform_filter(
    alt.FieldOneOfPredicate(field='id', oneOf=schengen_iso_codes)
).project(
    type='naturalEarth1'
)

q4 = geo_chart + schengen_highlight + us_highlight

# st.altair_chart(q4, use_container_width=True)


##############################
################################
################################
## Final composition
# Hide legend for q3
q3_no_legend = q3.encode(color=alt.Color('region:N', legend=None))

# rows
row1 = alt.hconcat(q2, q1, q3_no_legend)
row2 = alt.hconcat(q4).resolve_scale(color="independent")
 
# final layout
# final_layout = alt.vconcat(row1, row2).resolve_scale(color='independent')
# st.altair_chart(row1, use_container_width=False)
# st.altair_chart(row2, use_container_width=True)

with col1[0]:
    st.altair_chart(row1, use_container_width=True)

col2 = st.columns(1)
with col2[0]:
    st.altair_chart(row2, use_container_width=True)

# combined_chart = alt.vconcat(
#     alt.hconcat(q2, q1),
#     alt.hconcat(q3_no_legend, q4).resolve_scale(color="independent"),
# ).resolve_scale(color='independent')
# st.altair_chart(combined_chart, use_container_width=True)