# %%
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
# %%
data = pd.read_csv("../data/transformed_data.csv")
data2 = pd.read_csv("../data/raw_data.csv")
gdp_per_capita_data = pd.read_csv("../data/gdp-per-capita-worldbank.csv")
print(data)
# %%
print(data.head())
# %%
print(data2.head())
# %%
data["COUNTRY"].value_counts()
# %%
data["COUNTRY"].value_counts().mode()
# %%
code = data["CODE"].unique().tolist()
country = sorted(list(set(data["COUNTRY"].unique()) & 
                      set(
                          gdp_per_capita_data.loc[gdp_per_capita_data["Year"] == 2022]["Entity"].unique()
                          )))
hdi = []
tc = []
td = []
sti = []
population = data["POP"].unique().tolist()
gdp = []
gdp_per_capita_before_covid = []
gdp_per_capita_during_covid = []
gdp_per_capita_after_covid = []
# %%
for i in country:
    hdi.append((data.loc[data["COUNTRY"] == i, "HDI"]).sum()/294) #dividing by mode
    tc.append((data2.loc[data2["location"] == i, "total_cases"]).sum())
    td.append((data2.loc[data2["location"] == i, "total_deaths"]).sum())
    sti.append((data.loc[data["COUNTRY"] == i, "STI"]).sum()/294)
    population.append((data2.loc[data2["location"] == i, "population"]).sum()/294)
    gdp_per_capita_before_covid.append(
        gdp_per_capita_data.loc[(gdp_per_capita_data["Entity"] == i) 
                                & (gdp_per_capita_data["Year"] == 2019), 
                                "GDP per capita, PPP (constant 2017 international $)"].item()
        )
    gdp_per_capita_during_covid.append(
        gdp_per_capita_data.loc[(gdp_per_capita_data["Entity"] == i) 
                                & (gdp_per_capita_data["Year"] == 2021), 
                                "GDP per capita, PPP (constant 2017 international $)"].item()
        )
    gdp_per_capita_after_covid.append(
        gdp_per_capita_data.loc[(gdp_per_capita_data["Entity"] == i) 
                                & (gdp_per_capita_data["Year"] == 2022), 
                                "GDP per capita, PPP (constant 2017 international $)"].item()
        )

aggregated_data = pd.DataFrame(list(zip(code, country, hdi, tc, td, sti, population, 
                                        gdp_per_capita_before_covid, 
                                        gdp_per_capita_during_covid, 
                                        gdp_per_capita_after_covid)), 
                               columns = ["Country Code", "Country", "HDI", 
                                          "Total Cases", "Total Deaths", 
                                          "Stringency Index", "Population", 
                                          "GDP Per Capita Before Covid", 
                                          "GDP Per Capita During Covid",
                                          "GDP Per Capita After Covid"])

print(aggregated_data.head())
# %%
data = aggregated_data.sort_values(by=["Total Cases"], ascending=False)
data.head()
# %%
figure = px.bar(data[data["Total Cases"] > 1e7], 
                y = 'Total Cases', 
                x = 'Country',
                title = "Countries with more than 10 million Covid cases")
figure.show()
# %%
figure = px.bar(data[data["Total Deaths"] > 1e5], 
                y = 'Total Deaths', 
                x = 'Country',
                title = "Countries with more than 100 thousand deaths")
figure.show()
# %%
fig = go.Figure()
fig.add_trace(go.Bar(
    x = data["Country"],
    y = data["Total Cases"],
    name='Total Cases',
    marker_color='indianred'
))
fig.add_trace(go.Bar(
    x = data["Country"],
    y = data["Total Deaths"],
    name='Total Deaths',
    marker_color='lightsalmon'
))
fig.update_layout(barmode='group', xaxis_tickangle = -45)
fig.show()
# %%
cases = data["Total Cases"].sum()
deceased = data["Total Deaths"].sum()

labels = ["Total Cases", "Total Deaths"]
values = [cases, deceased]

fig = px.pie(data, values=values, names = labels,
             title = "Percentage of Total Cases and Deaths", hole = 0.5)
fig.show()
# %%
death_rate = (data["Total Deaths"].sum() / data["Total Cases"].sum()) * 100
print("Death Rate = ", death_rate)
# %%
# stringency index. It is a composite measure of response indicators, including school closures, workplace closures, and travel bans. It shows how strictly countries are following these measures to control the spread of covid-19
fig = px.bar(data, x ='Country', y = 'Total Cases', 
             hover_data=['Population', 'Total Deaths'],
             color = 'Stringency Index', height = 400,
             title = "Stringency Index by Country during Covid-19")
fig.show()
# %%
# Analyzing Covid-19 Impacts on Economy
fig = px.bar(data, x = 'Country', y = 'Total Cases', 
             hover_data=['Population', 'Total Deaths'],
             color = "GDP Per Capita Before Covid", height= 400,
             title = "GDP Per Capita before Covid-19")
fig.show()
# %%
fig = px.bar(data, x = 'Country', y = 'Total Cases', 
             hover_data=['Population', 'Total Deaths'],
             color = "GDP Per Capita During Covid", height= 400,
             title = "GDP Per Capita during Covid-19")
fig.show()
# %%
fig = px.bar(data, x = 'Country', y = 'Total Cases', 
             hover_data=['Population', 'Total Deaths'],
             color = "GDP Per Capita After Covid", height= 400,
             title = "GDP Per Capita after Covid-19")
fig.show()
# %%
fig = go.Figure()
fig.add_trace(go.Bar(
    x = data["Country"],
    y = data["GDP Per Capita Before Covid"],
    name='GDP Per Capita before Covid-19',
    marker_color='indianred'
))
fig.add_trace(go.Bar(
    x = data["Country"],
    y = data["GDP Per Capita During Covid"],
    name='GDP Per Capita during Covid-19',
    marker_color='lightsalmon'
))
fig.add_trace(go.Bar(
    x = data["Country"],
    y = data["GDP Per Capita After Covid"],
    name='GDP Per Capita after Covid-19',
    marker_color='pink'
))
fig.update_layout(barmode='group', xaxis_tickangle = -45)
fig.show()
# %%
# Human Development Index. It is a statistic composite index of life expectancy, education, and per capita indicators
fig = px.bar(data, x = 'Country', y = 'Total Cases', 
             hover_data=['Population', 'Total Deaths'],
             color = "HDI", height= 400,
             title = "Human Development Index during Covid-19")
fig.show()
# %%
