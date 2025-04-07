# %%
import pandas as pd
import mysql.connector

# %%
df = pd.read_csv("ICRISAT-District Level Data - ICRISAT-District Level Data.csv")

# %%
df.head()

# %%
df.describe()

# %%
df.isnull().sum()

# %%
df.info()

# %%
df.columns

# %%
df=pd.read_csv("ICRISAT-District Level Data - ICRISAT-District Level Data.csv")
df.head()

# %%
def clean_column(col):
    col = col.lower().strip()  # Lowercase & remove leading/trailing spaces
    
    # Remove units like (1000 ha), (1000 tons), (Kg per ha)
    col = col.replace('(1000 ha)', '').replace('(1000 tons)', '').replace('(kg per ha)', '')
    
    col = col.replace('(', '').replace(')', '').replace('/', '').strip()
    
    # Replace multiple spaces with single underscore
    col = '_'.join(col.split())
    
    # Add appropriate suffix based on keywords
    if 'area' in col:
        col = col.replace('area', 'area_ha')
    elif 'production' in col:
        col = col.replace('production', 'production_tons')
    elif 'yield' in col:
        col = col.replace('yield', 'yield_kg_per_ha')
    
    return col

# Apply to all columns
df.columns = [clean_column(c) for c in df.columns]

# Preview




# %%
df.head()

# %%
# Columns to multiply by 1000 (Area in 1000 ha → ha)
area_cols = [col for col in df.columns if 'area_ha' in col]
df[area_cols] = df[area_cols] * 1000

# Columns to multiply by 1000 (Production in 1000 tons → tons)
production_cols = [col for col in df.columns if 'production_tons' in col]
df[production_cols] = df[production_cols] * 1000



# %%
production_cols = [col for col in df.columns if 'production_tons' in col]
for col in production_cols:
    new_col = col.replace('production_tons','production_kg')
    df[new_col] = df[col]*1000

# %% [markdown]
# 

# %%
df.to_csv("agricultural.csv")

# %%
df.head()

# %%
from sqlalchemy import create_engine
engine = create_engine('mysql+mysqlconnector://root:''@localhost:3306/agridata')

# %%
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()
session.rollback()  # Rollback pending transaction
session.close()


# %%
tablename='agridata1'
df.to_sql(tablename,engine,if_exists='replace',index=False)
print("datauplodaded to '{tablename}' table successfully")

# %%
numeric = df.select_dtypes(include=['number'])
negative_values = numeric <0 


# %%
negative_values

# %%
negative_values.sum()

# %%
def negative_numbers(data):
    numeric_cols = data.select_dtypes(include=['number'])
    numeric_0 = (numeric_cols<0).sum()
    numeric_0_cols = numeric_0[numeric_0>0]
    if not numeric_0_cols.empty:
        print("Column has positive values")
        print(numeric_0_cols)
    else:
        print("All number have only positive values")

# %%
def zero_number(data):
    numeric_cols = data.select_dtypes(include=['number'])
    number_01 = (numeric_cols==0).sum()
    numeric_0_cols = number_01[number_01==0]

    if not numeric_0_cols.empty:
        print("Columns has zero numbers")
        print(numeric_0_cols)
    else:
        print("Number doesnt contains any zero values")

# %% [markdown]
# Rice Data for each states

# %%
rice_states = df[['dist_code','year','state_code','rice_area_ha','rice_production_tons','rice_yield_kg_per_ha','rice_production_kg','state_name','dist_name']]

# %%
rice_states.describe()

# %%
rice_states=rice_states[rice_states['rice_area_ha']>0]
rice_states=rice_states[rice_states['rice_production_tons']>0]
negative_numbers(rice_states)

# %%
#tablename = 'ricedata'
#rice_states.to_sql(tablename,engine,if_exists='replace',index=False)


# %% [markdown]
# Wheat Data for each states

# %%
wheat_states = df[['dist_code','year','state_code','wheat_area_ha','wheat_production_tons','wheat_production_kg','wheat_yield_kg_per_ha','state_name','dist_name']]
wheat_states = wheat_states[wheat_states['wheat_production_kg']>0]
wheat_states = wheat_states[wheat_states['wheat_area_ha']!=0]
negative_numbers(wheat_states)

# %%
#tablename = 'wheat_states'
#wheat_states.to_sql(tablename,engine,if_exists='replace',index=False)
#print("datauplodaded to {'tablename'} table successfully")

# %% [markdown]
# Kharif Sorghum for each states
# 

# %%
kharif_sorghum = df[['dist_code','year','state_code','kharif_sorghum_area_ha','kharif_sorghum_production_tons','kharif_sorghum_production_kg','kharif_sorghum_yield_kg_per_ha','state_name','dist_name']]

# %%
kharif_sorghum = kharif_sorghum[kharif_sorghum['kharif_sorghum_area_ha']>0]
kharif_sorghum = kharif_sorghum[kharif_sorghum['kharif_sorghum_production_kg']>0]
negative_numbers(kharif_sorghum)

# %%
kharif_sorghum.describe()

# %%
#tablename = 'kharif_sorghum'
#kharif_sorghum.to_sql(tablename,engine,if_exists='replace',index=False)
#print(f"Data uploaded to {tablename} table successfully")

# %% [markdown]
# Rabi Sorghum for each states
# 

# %%
rabi_sorghum = df[['dist_code','year','state_code','rabi_sorghum_area_ha','rabi_sorghum_production_tons','rabi_sorghum_production_kg','rabi_sorghum_yield_kg_per_ha','state_name','dist_name']]
rabi_sorghum = rabi_sorghum.loc[rabi_sorghum['rabi_sorghum_area_ha']>0]
rabi_sorghum = rabi_sorghum.loc[rabi_sorghum['rabi_sorghum_area_ha']!=0]
rabi_sorghum = rabi_sorghum.loc[rabi_sorghum['rabi_sorghum_production_kg']!=0]
negative_numbers(rabi_sorghum)

# %%
rabi_sorghum.describe()

# %%
tablename = 'rabi_sorghum'
rabi_sorghum.to_sql(tablename,engine,if_exists='replace',index=False)
print(f"Data uploaded to {tablename} table successfully")

# %% [markdown]
# Sorghum for each states

# %%
sorghum = df[['dist_code','year','state_code','sorghum_area_ha','sorghum_production_tons','sorghum_production_kg','sorghum_yield_kg_per_ha','state_name','dist_name']]
sorghum = sorghum.loc[sorghum['sorghum_area_ha']>0]
sorghum = sorghum.loc[sorghum['sorghum_area_ha']!=0]
sorghum = sorghum.loc[sorghum['sorghum_production_kg']!=0]
negative_numbers(sorghum)

# %%
sorghum.describe()

# %%
# tablename = 'sorghum'
# sorghum.to_sql(tablename,engine,if_exists='replace',index=False)
# print(f"Data uploaded to {tablename} table successfully")

# %% [markdown]
# Pearl Millet for each state

# %%
pearl_millet = df[['dist_code','year','state_code','pearl_millet_area_ha','pearl_millet_production_tons','pearl_millet_production_kg','pearl_millet_yield_kg_per_ha','state_name','dist_name']]
pearl_millet = pearl_millet.loc[pearl_millet['pearl_millet_area_ha']>0]
pearl_millet = pearl_millet.loc[pearl_millet['pearl_millet_area_ha']!=0]
pearl_millet = pearl_millet.loc[pearl_millet['pearl_millet_production_kg']!=0]
negative_numbers(pearl_millet)

# %%
pearl_millet.describe()

# %%
# tablename = 'pearl_millet'
# pearl_millet.to_sql(tablename,engine,if_exists='replace',index=False)
# print(f"Data uploaded to {tablename} table successfully")

# %% [markdown]
# Maize for each state

# %%
maize = df[['dist_code','year','state_code','maize_area_ha','maize_production_tons','maize_production_kg','maize_yield_kg_per_ha','state_name','dist_name']]
maize = maize.loc[maize['maize_area_ha']>0]
maize = maize.loc[maize['maize_production_kg']!=0]
maize = maize.loc[maize['maize_yield_kg_per_ha']!=0]
negative_numbers(maize)

# %%
maize.describe()

# %%
# tablename = 'maize'
# maize.to_sql(tablename,engine,if_exists='replace',index=False)
# print(f"Data uploaded to {tablename} table successfully")

# %% [markdown]
# Finger millet for each state

# %%
finger_millet = df[['dist_code','year','state_code','finger_millet_area_ha','finger_millet_production_tons','finger_millet_production_kg','finger_millet_yield_kg_per_ha','state_name','dist_name']]
finger_millet = finger_millet.loc[finger_millet['finger_millet_area_ha']>0]
finger_millet = finger_millet.loc[finger_millet['finger_millet_production_kg']!=0]
negative_numbers(finger_millet)

# %%
finger_millet.describe()

# %%
tablename = 'finger_millet'
finger_millet.to_sql(tablename,engine,if_exists='replace',index=False)
print(f"Data uploaded to {tablename} table successfully")

# %% [markdown]
# Barley for each state

# %%
barley = df[['dist_code','year','state_code','barley_area_ha','barley_production_tons','barley_production_kg','barley_yield_kg_per_ha','state_name','dist_name']]
barley = barley.loc[barley['barley_area_ha']>0]
barley = barley.loc[barley['barley_production_tons']!=0]
negative_numbers(barley)

# %%
barley.describe()

# %%
# tablename = 'barley'
# barley.to_sql(tablename,engine,if_exists='replace',index=False)
# print(f"Data uploaded to {tablename} table successfully")

# %% [markdown]
# Chickpea for each state

# %%
chickpea = df[['dist_code','year','state_code','chickpea_area_ha','chickpea_production_tons','chickpea_production_kg','chickpea_yield_kg_per_ha','state_name','dist_name']]
chickpea = chickpea.loc[chickpea['chickpea_area_ha']>0]
chickpea = chickpea.loc[chickpea['chickpea_production_tons']>0]
chickpea = chickpea.loc[chickpea['chickpea_production_kg']!=0]
negative_numbers(chickpea)

# %%
chickpea.describe()

# %%
# tablename = 'chickpea'
# chickpea.to_sql(tablename,engine,if_exists='replace',index=False)
# print(f"Data uploaded to {tablename} table successfully")

# %% [markdown]
# pigeonpea for each state

# %%
pigeonpea = df[['dist_code','year','state_code','pigeonpea_area_ha','pigeonpea_production_tons','pigeonpea_production_kg','pigeonpea_yield_kg_per_ha','state_name','dist_name']]
pigeonpea = pigeonpea.loc[pigeonpea['pigeonpea_area_ha']>0]
pigeonpea = pigeonpea.loc[(pigeonpea['pigeonpea_production_kg']>0) & (pigeonpea['pigeonpea_production_kg']!=0)]
negative_numbers(pigeonpea)

# %%
pigeonpea.describe()

# %%
# tablename = 'pigeonpea'
# pigeonpea.to_sql(tablename,engine,if_exists='replace',index=False)
# print(f"Data uploaded to {tablename} table successfully")

# %% [markdown]
# Groudnut for each state

# %%
groundnut = df[['dist_code','year','state_code','groundnut_area_ha','groundnut_production_tons','groundnut_production_kg','groundnut_yield_kg_per_ha','state_name','dist_name']]
groundnut = groundnut.loc[(groundnut['groundnut_area_ha']>0) & (groundnut['groundnut_area_ha']!=0)]
groundnut = groundnut.loc[(groundnut['groundnut_production_tons']>0 & (groundnut['groundnut_production_tons']!=0))]
negative_numbers(groundnut)

# %%
groundnut.describe()

# %%
# tablename = 'groundnut'
# groundnut.to_sql(tablename,engine,if_exists='replace',index=False)
# print(f"Data uploaded to {tablename} table successfully")

# %% [markdown]
# Sesamum for each state

# %%
sesamum = df[['dist_code','year','state_code','sesamum_area_ha','sesamum_production_tons','sesamum_production_kg','sesamum_yield_kg_per_ha','state_name','dist_name']]
negative_numbers(sesamum)
sesamum = sesamum.loc[(sesamum['sesamum_area_ha']>0) & (sesamum['sesamum_area_ha']!=0)]
sesamum = sesamum.loc[(sesamum['sesamum_production_kg']>0) & (sesamum['sesamum_production_kg']!=0)]
negative_numbers(sesamum)

# %%
sesamum.describe()

# %%
# tablename = 'sesamum'
# sesamum.to_sql(tablename,engine,if_exists='replace',index=False)
# print(f"Data uploaded to {tablename} table successfully")

# %% [markdown]
# Rapeseed and mustrad for each state

# %%
rapeseed = df[['dist_code','year','state_code','rapeseed_and_mustard_area_ha','rapeseed_and_mustard_production_tons','rapeseed_and_mustard_production_kg','rapeseed_and_mustard_yield_kg_per_ha','state_name','dist_name']]
rapeseed = rapeseed.loc[(rapeseed['rapeseed_and_mustard_area_ha']>0)&(rapeseed['rapeseed_and_mustard_area_ha']!=0)]
rapeseed = rapeseed.loc[(rapeseed['rapeseed_and_mustard_production_kg']>0)&(rapeseed['rapeseed_and_mustard_production_kg']!=0)]
negative_numbers(rapeseed)

# %%
rapeseed.describe()

# %%
# tablename = 'rapeseed'
# rapeseed.to_sql(tablename,engine,if_exists='replace',index=False)
# print(f"Data uploaded to {tablename} table successfully")

# %% [markdown]
# Minor pulses for each state

# %%
minor_pulses = df[['dist_code','year','state_code','minor_pulses_area_ha','minor_pulses_production_tons','minor_pulses_production_kg','minor_pulses_yield_kg_per_ha','state_name','dist_name']]
minor_pulses = minor_pulses.loc[(minor_pulses['minor_pulses_area_ha']>0)&(minor_pulses['minor_pulses_area_ha']!=0)]
minor_pulses = minor_pulses.loc[(minor_pulses['minor_pulses_production_tons']>0)&(minor_pulses['minor_pulses_production_tons']!=0)]
minor_pulses['minor_pulses_yield_kg_per_ha'] = minor_pulses['minor_pulses_production_kg']/minor_pulses['minor_pulses_area_ha']
negative_numbers(minor_pulses)

# %%
minor_pulses.describe()

# %%
# tablename = 'minor_pulses'
# minor_pulses.to_sql(tablename,engine,if_exists='replace',index=False)
# print(f"Data uploaded to {tablename} table successfully")

# %% [markdown]
# Safflower for each state

# %%
safflower = df[['dist_code','year','state_code','safflower_area_ha','safflower_production_tons','safflower_production_kg','safflower_yield_kg_per_ha','state_name','dist_name']]
safflower = safflower.loc[(safflower['safflower_area_ha']>0)&(safflower['safflower_area_ha']!=0)]
safflower = safflower.loc[(safflower['safflower_production_kg']>0)&(safflower['safflower_production_kg']!=0)]
negative_numbers(safflower) 

# %%
safflower.describe()

# %%
# tablename = 'safflower'
# safflower.to_sql(tablename,engine,if_exists='replace',index=False)
# print(f"Data uploaded to {tablename} table successfully")

# %% [markdown]
# Castor for each state

# %%
castor = df[['dist_code','year','state_code','castor_area_ha','castor_production_tons','castor_production_kg','castor_yield_kg_per_ha','state_name','dist_name']]
castor = castor.loc[(castor['castor_area_ha']>0)&(castor['castor_area_ha']!=0)]
castor = castor.loc[(castor['castor_production_kg']>0)&(castor['castor_production_kg']!=0)]
negative_numbers(castor)

# %%
castor.describe()

# %%
# tablename = 'castor'
# castor.to_sql(tablename,engine,if_exists='replace',index=False)
# print(f"Data uploaded to {tablename} table successfully")

# %% [markdown]
# Linseed for each state

# %%
linseed = df[['dist_code','year','state_code','linseed_area_ha','linseed_production_tons','linseed_production_kg','linseed_yield_kg_per_ha','state_name','dist_name']]
linseed = linseed.loc[(linseed['linseed_area_ha']>0)&(linseed['linseed_area_ha']!=0)]
linseed = linseed.loc[(linseed['linseed_production_kg']>0)&(linseed['linseed_production_kg']!=0)]
negative_numbers(linseed)

# %%
linseed.describe()

# %%
# tablename = 'linseed'
# linseed.to_sql(tablename,engine,if_exists='replace',index=False)
# print(f"Data uploaded to {tablename} table successfully")

# %% [markdown]
# Sunflower for each state

# %%
sunflower = df[['dist_code','year','state_code','sunflower_area_ha','sunflower_production_tons','sunflower_production_kg','sunflower_yield_kg_per_ha','state_name','dist_name']]
sunflower = sunflower.loc[(sunflower['sunflower_area_ha']>0)&(sunflower['sunflower_area_ha'])!=0]
sunflower = sunflower.loc[(sunflower['sunflower_production_tons']>0)&(sunflower['sunflower_production_tons']!=0)]
negative_numbers(sunflower)

# %%
sunflower.describe()

# %%
# tablename = 'sunflower'
# sunflower.to_sql(tablename,engine,if_exists='replace',index=False)
# print(f"Data uploaded to {tablename} table successfully")

# %% [markdown]
# soyabean for each state

# %%
soyabean = df[['dist_code','year','state_code','soyabean_area_ha','soyabean_production_tons','soyabean_production_kg','soyabean_yield_kg_per_ha','state_name','dist_name']]
soyabean = soyabean.loc[(soyabean['soyabean_area_ha']>0)&(soyabean['soyabean_area_ha']!=0)]
soyabean = soyabean.loc[(soyabean['soyabean_production_tons']>0)&(soyabean['soyabean_production_tons']!=0)]
negative_numbers(soyabean)

# %%
soyabean.describe()

# %%
# tablename = 'soyabean'
# soyabean.to_sql(tablename,engine,if_exists='replace',index=False)
# print(f"Data uploaded to {tablename} table successfully")

# %% [markdown]
# Oil seed state wise

# %%
oilseed = df[['dist_code','year','state_code','oilseeds_area_ha','oilseeds_production_tons','oilseeds_production_kg','oilseeds_yield_kg_per_ha','state_name','dist_name']]
oilseed = oilseed.loc[(oilseed['oilseeds_area_ha']>0)&(oilseed['oilseeds_area_ha']!=0)]
oilseed = oilseed.loc[(oilseed['oilseeds_production_kg']>0)&(oilseed['oilseeds_production_kg']!=0)]
oilseed['oilseeds_yield_kg_per_ha'] = oilseed['oilseeds_production_kg']/oilseed['oilseeds_area_ha']
negative_numbers(oilseed)

# %%
# tablename = 'oilseed'
# oilseed.to_sql(tablename,engine,if_exists='replace',index=False)
# print(f"Data uploaded to {tablename} table successfully")

# %%
state_count = df[df['oilseeds_production_kg'] > 0]['state_name'].nunique()
print(f"Total States with Oilseed Production: {state_count}")

# %%
oilseed1=oilseed.groupby("state_name").agg({"state_name":"count","oilseeds_production_kg":"sum"})
oilseed1


# %% [markdown]
# sugarcane statewise data

# %%
sugarcane = df[['dist_code','year','state_code','sugarcane_area_ha','sugarcane_production_tons','sugarcane_production_kg','sugarcane_yield_kg_per_ha','state_name','dist_name']]
sugarcane = sugarcane.loc[(sugarcane['sugarcane_area_ha']>0)&(sugarcane['sugarcane_area_ha']!=0)]
sugarcane = sugarcane.loc[(sugarcane['sugarcane_production_kg']>0)&(sugarcane['sugarcane_production_kg']!=0)]
negative_numbers(sugarcane)

# %%
sugarcane.describe()

# %%
# tablename = 'sugarcane'
# sugarcane.to_sql(tablename,engine,if_exists='replace',index=False)
# print(f"Data uploaded to {tablename} table successfully")

# %% [markdown]
# COTTON STATWISE DATA

# %%
cotton = df[['dist_code','year','state_code','cotton_area_ha','cotton_production_tons','cotton_production_kg','cotton_yield_kg_per_ha','state_name','dist_name']]
cotton = cotton.loc[(cotton['cotton_area_ha']>0)&(cotton['cotton_area_ha']!=0)]
cotton = cotton.loc[(cotton['cotton_production_kg']>0)&(cotton['cotton_production_kg']!=0)]
negative_numbers(cotton)

# %%
# tablename = 'cotton'
# cotton.to_sql(tablename,engine,if_exists='replace',index=False)
# print(f"Data uploaded to {tablename} table successfully")

# %% [markdown]
# fruits cultivation state wise data

# %%
fruits = df[['dist_code','year','state_code','fruits_area_ha','state_name','dist_name']]
fruits = fruits.loc[fruits['fruits_area_ha']>0]
negative_numbers(fruits)

# %%
fruits.describe()

# %%
# tablename = 'fruits'
# fruits.to_sql(tablename,engine,if_exists='replace',index=False)
# print(f"Data uploaded to {tablename} table successfully")

# %% [markdown]
# Vegetable cultivation state wise data

# %%
vegetable = df[['dist_code','year','state_code','vegetables_area_ha','state_name','dist_name']]
vegetable = vegetable.loc[vegetable['vegetables_area_ha']>0]
negative_numbers(vegetable)

# %%
# tablename = 'vegetable'
# vegetable.to_sql(tablename,engine,if_exists='replace',index=False)
# print(f"Data uploaded to {tablename} table successfully")

# %% [markdown]
# Fruits and vegetable area combined
# 

# %%
fru_veg = df[['dist_code','year','fruits_and_vegetables_area_ha','state_name','dist_name']]
fru_veg = fru_veg.loc[fru_veg['fruits_and_vegetables_area_ha']>0]
negative_numbers(fru_veg)

# %%
# tablename = 'fru_veg'
# fru_veg.to_sql(tablename,engine,if_exists='replace',index=False)
# print(f"Data uploaded to {tablename} table successfully")

# %% [markdown]
# Potatoes area combined

# %%
potatoes = df[['dist_code','year','potatoes_area_ha','state_name','dist_name']]
potatoes = potatoes.loc[potatoes['potatoes_area_ha']>0]
negative_numbers(potatoes)

# %%
# tablename = 'potatoes'
# potatoes.to_sql(tablename,engine,if_exists='replace',index=False)
# print(f"Data uploaded to {tablename} table successfully")

# %% [markdown]
# Onion area combined

# %%
onion = df[['dist_code','year','onion_area_ha','state_name','dist_name']]
onion = onion.loc[onion['onion_area_ha']>0]
negative_numbers(onion)

# %%
# tablename = 'onion'
# onion.to_sql(tablename,engine,if_exists='replace',index=False)
# print(f"Data uploaded to {tablename} table successfully")

# %% [markdown]
# Fodder area combined

# %%
fodder = df[['dist_code','year','fodder_area_ha','state_name','dist_name']]
fodder = fodder.loc[fodder['fodder_area_ha']>0]
negative_numbers(fodder)

# %%
# tablename = 'fodder'
# fodder.to_sql(tablename,engine,if_exists='replace',index=False)
# print(f"Data uploaded to {tablename} table successfully")

# %%
import mysql.connector

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = ""
)

mycursor = mydb.cursor()

# %%
mycursor.execute("""SELECT STATE_CODE,
                 SUM(RICE_PRODUCTION_KG) AS TOTAL_RICEPRODUCTION_KG
                 FROM AGRIDATA.RICEDATA 
                 GROUP BY STATE_CODE
                 ORDER BY TOTAL_RICEPRODUCTION_KG DESC
                 LIMIT 7;""")

# %%
mycursor.fetchall()

# %%
rice_states.groupby('year').agg(sum)

# %%
# Group rice and wheat data year-wise
rice_yearly = rice_states.groupby('year').agg('sum').reset_index()
wheat_yearly = wheat_states.groupby('year').agg('sum').reset_index()



# %%
# Merge rice & wheat yearly data on 'year'
combined = pd.merge(rice_yearly[['year', 'rice_production_kg']],
                    wheat_yearly[['year', 'wheat_production_kg']],
                    on='year')


# %%
combined

# %%
combined_yr=combined.groupby("year").agg("sum")
combined_yr.to_csv('combinedwheatrice.csv')


# %%
combined['wheat_production_kg'].min()

# %%
combined['rice_production_kg'].max()

# %%
import plotly.graph_objects as go

fig = go.Figure()

# Add Rice Production Line
fig.add_trace(go.Scatter(
    x=combined['year'],
    y=combined['rice_production_kg'],
    mode='lines+markers',
    name='Rice Production'
))

# Add Wheat Production Line
fig.add_trace(go.Scatter(
    x=combined['year'],
    y=combined['wheat_production_kg'],
    mode='lines+markers',
    name='Wheat Production'
))

# Layout
fig.update_layout(
    title='Rice Production vs Wheat Production (Last 50 Years)',
    xaxis_title='Year',
    yaxis_title='Production (kg)',
    template='plotly_white'
)

fig.show(renderer="browser")


# %%
tablename = 'combined'
combined.to_sql(tablename,engine,if_exists='replace',index=False)
print(f"Data uploaded to {tablename} table successfully")

# %%
pearl_millet1 = pearl_millet.groupby('year').agg('sum').reset_index()
finger_millet1 = finger_millet.groupby('year').agg('sum').reset_index()

# %%
combinedmillet = pd.merge(pearl_millet1[['year', 'pearl_millet_production_kg','state_name']],
                    finger_millet1[['year', 'finger_millet_production_kg','state_name']],
                    on='year')

# %%
tablename = 'combined_millet'
combinedmillet.to_sql(tablename,engine,if_exists="replace",index=False)
print(f"Data uploaded to {tablename} table successfully")

# %%
sorghumcombined = pd.merge(kharif_sorghum[['year','kharif_sorghum_production_kg','state_code','state_name']],
                           rabi_sorghum[['year','rabi_sorghum_production_kg','state_code','state_name']],
                           on='year')


# %%
oilseed1=oilseed.groupby('state_code').agg("sum")


# %%
import mysql.connector
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database='agridata')

mycursor = connection.cursor()


# %%
mycursor.execute("""SELECT STATE_NAME, SUM(RICE_PRODUCTION_KG) AS TOTAL_PRODUCTION
                 FROM AGRIDATA.RICEDATA
                 GROUP BY STATE_NAME
                 ORDER BY TOTAL_PRODUCTION DESC
                 LIMIT 3""")

out = mycursor.fetchall()
column = [i[0] for i in mycursor.description]

df1 = pd.DataFrame(out, columns=column)
df1


# %% [markdown]
# 1.Year-wise Trend of Rice Production Across States (Top 3)

# %%
mycursor.execute("""SELECT YEAR, SUM(RICE_PRODUCTION_KG)AS TOTAL_PRODUCTION, STATE_NAME
                 FROM AGRIDATA.RICEDATA
                 WHERE STATE_NAME IN ('West Bengal','Uttar Pradesh', 'Punjab')
                 GROUP BY YEAR,STATE_NAME
                 ORDER BY YEAR,STATE_NAME""")
out = mycursor.fetchall()
column = [i[0] for i in mycursor.description]
df1 = pd.DataFrame(out, columns = column)
tablename = "sqlquery1"
df1.to_sql(tablename,engine,if_exists='replace',index=False)

# %% [markdown]
# 2.Top 5 Districts by Wheat Yield Increase Over the Last 5 Years

# %%
mycursor.execute("""SELECT DIST_NAME, SUM(WHEAT_YIELD_KG_PER_HA)AS YIELD_PRODUCTION
                 FROM AGRIDATA.WHEAT_STATES
                 GROUP BY DIST_NAME
                 ORDER BY YIELD_PRODUCTION DESC
                 LIMIT 5;""")
out = mycursor.fetchall()
column = [i[0] for i in mycursor.description]
df1 = pd.DataFrame(out, columns = column)
mycursor.execute(f"""SELECT YEAR, DIST_NAME, SUM(WHEAT_YIELD_KG_PER_HA) AS YIELD_PRODUCTION
                     FROM AGRIDATA.WHEAT_STATES
                     WHERE YEAR >= (SELECT MAX(YEAR) FROM AGRIDATA.WHEAT_STATES) - 5
                     AND DIST_NAME IN ('Ludhiana','Sangrur','Patiala','Jalandhar','Ferozpur')
                     GROUP BY YEAR, DIST_NAME
                     ORDER BY YEAR, DIST_NAME;""")
out = mycursor.fetchall()
column = [i[0] for i in mycursor.description]
df1 = pd.DataFrame(out, columns = column)
tablename = "sqlquery2"

# %%
df1.to_sql(tablename,engine,if_exists='replace',index=False)

# %% [markdown]
# 3.States with the Highest Growth in Oilseed Production (5-Year Growth Rate)

# %%
mycursor.execute(""" WITH production_summary AS (
    SELECT 
        state_name,
        year,
        SUM(oilseeds_production_kg) AS total_production
    FROM 
        agridata.oilseed
    WHERE 
        year >= (SELECT MAX(year) FROM agridata.oilseed) - 5
    GROUP BY 
        state_name, year
),

growth_calculation AS (
    SELECT 
        state_name,
        MAX(CASE WHEN year = (SELECT MAX(year) FROM agridata.oilseed) - 5 THEN total_production END) AS production_5_years_ago,
        MAX(CASE WHEN year = (SELECT MAX(year) FROM agridata.oilseed) THEN total_production END) AS production_current_year
    FROM 
        production_summary
    GROUP BY 
        state_name
)

SELECT 
    state_name,
    production_5_years_ago,
    production_current_year,
    ROUND(((production_current_year - production_5_years_ago) / production_5_years_ago) * 100, 2) AS growth_rate_percentage
FROM 
    growth_calculation
WHERE 
    production_5_years_ago IS NOT NULL AND production_current_year IS NOT NULL
ORDER BY 
    growth_rate_percentage DESC
LIMIT 5;
""")
out = mycursor.fetchall()
column = [i[0] for i in mycursor.description]
df1 = pd.DataFrame(out, columns = column)
tablename = 'sqlquery3'

# %%
df1.to_sql(tablename,engine,if_exists="replace",index=False)

# %% [markdown]
# 4.District-wise Correlation Between Area and Production for Major Crops (Rice, Wheat, and Maize)

# %%
# Rice Data
mycursor.execute("SELECT DIST_CODE, DIST_NAME, SUM(RICE_AREA_HA) AS TOTAL_RICE_AREA, SUM(RICE_PRODUCTION_KG) AS TOTAL_RICE_PRODUCTION FROM AGRIDATA.RICEDATA GROUP BY DIST_CODE, DIST_NAME")
rice_rows = mycursor.fetchall()
rice_columns = [i[0] for i in mycursor.description]
rice_df = pd.DataFrame(rice_rows, columns=rice_columns)

# Wheat Data
mycursor.execute("SELECT DIST_CODE, SUM(WHEAT_AREA_HA) AS TOTAL_WHEAT_AREA, SUM(WHEAT_PRODUCTION_KG) AS TOTAL_WHEAT_PRODUCTION FROM AGRIDATA.WHEAT_STATES GROUP BY DIST_CODE")
wheat_rows = mycursor.fetchall()
wheat_columns = [i[0] for i in mycursor.description]
wheat_df = pd.DataFrame(wheat_rows, columns=wheat_columns)

# Maize Data
mycursor.execute("SELECT DIST_CODE, SUM(MAIZE_AREA_HA) AS TOTAL_MAIZE_AREA, SUM(MAIZE_PRODUCTION_KG) AS TOTAL_MAIZE_PRODUCTION FROM AGRIDATA.MAIZE GROUP BY DIST_CODE")
maize_rows = mycursor.fetchall()
maize_columns = [i[0] for i in mycursor.description]
maize_df = pd.DataFrame(maize_rows, columns=maize_columns)



# %%
# First merge Rice & Wheat
rice_wheat = pd.merge(rice_df, wheat_df, on='DIST_CODE', how='inner')

# Then merge with Maize
combined_df = pd.merge(rice_wheat, maize_df, on='DIST_CODE', how='inner')

tablename = 'sqlquery4'
combined_df.to_sql(tablename,engine,if_exists="replace",index=False)


# %% [markdown]
# Yearly Production Growth of Cotton in Top 5 Cotton Producing States

# %%
mycursor.execute("""WITH TOP_STATE AS (SELECT STATE_NAME, SUM(COTTON_PRODUCTION_KG) AS TOTAL_PRODUCTION
                 FROM AGRIDATA.COTTON
                 GROUP BY STATE_NAME
                 ORDER BY TOTAL_PRODUCTION DESC
                 LIMIT 5)

                 SELECT YEAR, STATE_NAME, SUM(COTTON_PRODUCTION_KG) AS YIELD_PRODUCTION
                 FROM AGRIDATA.COTTON
                 WHERE STATE_NAME IN (SELECT STATE_NAME FROM TOP_STATE)
                 GROUP BY YEAR,STATE_NAME
                 ORDER BY YEAR,STATE_NAME;""")

out = mycursor.fetchall()
column = [i[0] for i in mycursor.description]
df1 = pd.DataFrame(out, columns = column)
tablename = "sqlquery5"

# %%
df1.to_sql(tablename,engine,if_exists='replace',index=False)

# %% [markdown]
# 6.Districts with the Highest Groundnut Production in 2020

# %%
mycursor.execute("""SELECT DIST_NAME,SUM(GROUNDNUT_PRODUCTION_KG) AS PRODUCTION_KG,YEAR
                 FROM AGRIDATA.GROUNDNUT
                 WHERE YEAR <= 2020
                 GROUP BY YEAR,DIST_NAME
                 ORDER BY PRODUCTION_KG DESC;""")

out = mycursor.fetchall()
column = [i[0] for i in mycursor.description]
df1 = pd.DataFrame(out, columns = column)
tablename = "sqlquery6"

# %%
df1.to_sql(tablename,engine,if_exists='replace',index=False)

# %% [markdown]
# 7.Annual Average Maize Yield Across All States

# %%
mycursor.execute("""SELECT AVG(MAIZE_YIELD_KG_PER_HA) AS MAIZEYIELD, YEAR
                 FROM MAIZE
                 GROUP BY YEAR
                 ORDER BY YEAR
                 ;""")

out = mycursor.fetchall()
column = [i[0] for i in mycursor.description]
df1 = pd.DataFrame(out, columns = column)
tablename = "sqlquery7"

# %%
df1.to_sql(tablename,engine,if_exists='replace',index=False)

# %% [markdown]
# 8.Total Area Cultivated for Oilseeds in Each State

# %%
mycursor.execute(""" SELECT STATE_NAME, SUM(OILSEEDS_AREA_HA) AS TOTALAREA 
                 FROM AGRIDATA.OILSEED
                 GROUP BY STATE_NAME
                 ORDER BY TOTALAREA DESC
                 ;""")

out = mycursor.fetchall()
column = [i[0] for i in mycursor.description]
df1 = pd.DataFrame(out, columns = column)
tablename = "sqlquery8"

# %%
df1.to_sql(tablename,engine,if_exists='replace',index=False)

# %% [markdown]
# 9.Districts with the Highest Rice Yield

# %%
mycursor.execute(""" SELECT DIST_NAME, MAX(RICE_YIELD_KG_PER_HA) AS HIGHYIELD
                 FROM AGRIDATA.RICEDATA
                 GROUP BY DIST_NAME
                 ORDER BY HIGHYIELD  DESC

                 ;""")

out = mycursor.fetchall()
column = [i[0] for i in mycursor.description]
df1 = pd.DataFrame(out, columns = column)
tablename = "sqlquery9"

# %%
df1.to_sql(tablename,engine,if_exists='replace',index=False)

# %% [markdown]
# 10.Compare the Production of Wheat and Rice for the Top 5 States Over 10 Years

# %%
mycursor.execute("""
    SELECT STATE_NAME, YEAR, SUM(RICE_PRODUCTION_KG) AS RICE_PRODUCTION
    FROM AGRIDATA.RICEDATA
    GROUP BY STATE_NAME, YEAR
""")
rice_out = mycursor.fetchall()
rice_col = [i[0] for i in mycursor.description]
rice_df = pd.DataFrame(rice_out, columns=rice_col)

mycursor.execute("""
    SELECT STATE_NAME, YEAR, SUM(WHEAT_PRODUCTION_KG) AS WHEAT_PRODUCTION
    FROM AGRIDATA.WHEAT_STATES
    GROUP BY STATE_NAME, YEAR
""")
wheat_out = mycursor.fetchall()
wheat_col = [i[0] for i in mycursor.description]
wheat_df = pd.DataFrame(wheat_out, columns=wheat_col)

top5_states = rice_df.groupby('STATE_NAME')['RICE_PRODUCTION'].sum().sort_values(ascending=False).head(5).index.tolist()

rice_top = rice_df[rice_df['STATE_NAME'].isin(top5_states)]
wheat_top = wheat_df[wheat_df['STATE_NAME'].isin(top5_states)]

merged_df = pd.merge(rice_top, wheat_top, on=['STATE_NAME', 'YEAR'], how='inner')

recent_years = merged_df['YEAR'].sort_values().unique()[-10:]
final_df = merged_df[merged_df['YEAR'].isin(recent_years)]

tablename="sqlquery10"


# %%
final_df.to_sql(tablename,engine,if_exists='replace',index=False)

# %% [markdown]
# Data visualisation for all the crops
# 

# %% [markdown]
# Top 7 RICE PRODUCTION State Data(Bar_plot)

# %%
import plotly.express as px
import pandas as pd

# Assuming df_rice contains total rice production by state
top7_rice_states = rice_states.groupby('state_name')['rice_production_kg'].sum().nlargest(7).reset_index()

fig = px.bar(top7_rice_states,
             x='state_name',
             y='rice_production_kg',
             title='Top 7 Rice Producing States in India',
             labels={'state_name': 'State', 'rice_production_kg': 'Rice Production (kg)'},
             text='rice_production_kg')

fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig.update_layout(xaxis_tickangle=-45, template='plotly_white')
fig.show(renderer="browser")


# %% [markdown]
# Top 5 Wheat Producing States Data(Bar_chart)and its percentage(%)(Pie_chart)

# %%
import plotly.express as px
import pandas as pd

# Assuming df_rice contains total rice production by state
top5_wheat_states = wheat_states.groupby('state_name')['wheat_production_kg'].sum().nlargest(5).reset_index()

fig = px.bar(top5_wheat_states,
             x='state_name',
             y='wheat_production_kg',
             title='Top 5 Wheat Producing States in India',
             labels={'state_name': 'State', 'wheat_production_kg': 'Wheat Production (kg)'},
             text='wheat_production_kg')

fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig.update_layout(xaxis_tickangle=-45, template='plotly_white')
fig.show(renderer="browser")

# %%
import plotly.express as px

# Use the same top5_wheat_states DataFrame
fig_pie = px.pie(top5_wheat_states,
                 names='state_name',
                 values='wheat_production_kg',
                 title='Percentage Contribution of Top 5 Wheat Producing States')  # You can remove this line if you don't want a donut chart

# Optional: Customizing
fig_pie.update_traces(textinfo='percent+label')

fig_pie.update_layout(template='plotly_white')
fig_pie.show(renderer="browser")


# %% [markdown]
# Oil seed production by top 5 states

# %%
import plotly.express as px
import pandas as pd

# Assuming df_rice contains total rice production by state
top_5_oil_states = oilseed.groupby('state_name')['oilseeds_production_kg'].sum().nlargest(5).reset_index()

fig = px.bar(top_5_oil_states,
             x='state_name',
             y='oilseeds_production_kg',
             title='Top 5 Wheat Producing States in India',
             labels={'state_name': 'State', 'oilseed_production_kg': 'Oilseed Production (kg)'},
             text='oilseeds_production_kg')

fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig.update_layout(xaxis_tickangle=-45, template='plotly_white')
fig.show(renderer="browser")

# %% [markdown]
# Top 7 SUNFLOWER PRODUCTION  State

# %%
sunflower.head()

# %%
import plotly.express as px
import pandas as pd

# Assuming df_rice contains total rice production by state
top_7_sunflower_states = sunflower.groupby('state_name')['sunflower_production_kg'].sum().nlargest(7).reset_index()

fig = px.bar(top_7_sunflower_states,
             x='state_name',
             y='sunflower_production_kg',
             title='Top 5 Sunflower Producing States in India',
             labels={'state_name': 'State', 'sunflower_production_kg': 'Sunflower Production (kg)'},
             text='sunflower_production_kg')

fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig.update_layout(xaxis_tickangle=-45, template='plotly_white')
fig.show(renderer="browser")

# %% [markdown]
# India's SUGARCANE PRODUCTION From Last 50 Years(Line_plot)

# %%
sugarcane

# %%
import plotly.express as px
import pandas as pd

# Assuming 'sugarcane' is your DataFrame with 'year' and 'sugarcane_production_kg' columns
top_line_states = sugarcane.groupby('year')['sugarcane_production_kg'].sum().reset_index()

fig = px.line(
    top_line_states,
    x='year',
    y='sugarcane_production_kg',
    title="India's Sugarcane Production (Last 50 Years)",
    labels={'year': 'Year', 'sugarcane_production_kg': 'Sugarcane Production (kg)'}
)

# Optional: styling
fig.update_layout(
    template='plotly_white',
    xaxis_tickangle=-45
)

fig.show(renderer="browser")


# %% [markdown]
# Rice Production By West Bengal Districts

# %%
rice_states_west = rice_states.loc[rice_states['state_name']=="West Bengal"]

# %%
rice_states_west_plot = rice_states_west.groupby('dist_name')['rice_production_kg'].sum().reset_index()

fig = px.bar(rice_states_west_plot,
             x='dist_name',
             y='rice_production_kg',
             title='Top Rice Producing Districts in WestBengal',
             labels={'dist_name': 'District', 'rice_production_kg': 'Rice Production (kg)'},
             text='rice_production_kg')

fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig.update_layout(xaxis_tickangle=-45, template='plotly_white')
fig.show(renderer="browser")

# %% [markdown]
# Top 10 Wheat Production Years From UP

# %%
wheat_states_up = wheat_states.loc[wheat_states['state_name']=='Uttar Pradesh']
top5_wheat_year = wheat_states_up.groupby('year')['wheat_production_kg'].sum().nlargest(10).reset_index()

fig = px.bar(top5_wheat_year,
             x='year',
             y='wheat_production_kg',
             title='Top 10 Wheat Producing Year in UP',
             labels={'year': 'Year', 'wheat_production_kg': 'Wheat Production (kg)'},
             text='wheat_production_kg')

fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig.update_layout(xaxis_tickangle=-45, template='plotly_white')
fig.show(renderer="browser")

# %% [markdown]
# Millet Production (Last 50y)

# %%
combinedmillet.head()

# %%
import plotly.express as px
import pandas as pd


import plotly.graph_objects as go

fig = go.Figure()

# Add Rice Production Line
fig.add_trace(go.Scatter(
    x=combinedmillet['year'],
    y=combinedmillet['pearl_millet_production_kg'],
    mode='lines+markers',
    name='pearl_millet_production_kg'
))

# Add Wheat Production Line
fig.add_trace(go.Scatter(
    x=combinedmillet['year'],
    y=combinedmillet['finger_millet_production_kg'],
    mode='lines+markers',
    name='Wheat Production'
))

# Layout
fig.update_layout(
    title='Millet Production vs finger Millet Production (Last 50 Years)',
    xaxis_title='Year',
    yaxis_title='Production (kg)',
    template='plotly_white'
)

fig.show(renderer="browser")

# %% [markdown]
# Sorghum Production (Kharif and Rabi) by Region

# %%
import pandas as pd
import plotly.express as px

# Merge on year + state_code + state_name to align data correctly
sorghumcombined = pd.merge(
    kharif_sorghum[['year', 'kharif_sorghum_production_kg', 'state_code', 'state_name']],
    rabi_sorghum[['year', 'rabi_sorghum_production_kg', 'state_code', 'state_name']],
    on=['year', 'state_code', 'state_name'],
    how='outer'
)

# Group by state to get total Kharif and Rabi sorghum production
sorghum_by_state = sorghumcombined.groupby('state_name')[['kharif_sorghum_production_kg', 'rabi_sorghum_production_kg']].sum().reset_index()

# Bar chart with grouped bars
fig = px.bar(
    sorghum_by_state,
    x='state_name',
    y=['kharif_sorghum_production_kg', 'rabi_sorghum_production_kg'],
    title='Sorghum Production (Kharif and Rabi) by Region',
    labels={'value': 'Production (kg)', 'state_name': 'State', 'variable': 'Season'},
    barmode='group'  # Grouped bars
)

fig.update_layout(template='plotly_white', xaxis_tickangle=-45)
fig.show(renderer="browser")


# %% [markdown]
# Top 7 Groundnut producing states

# %%
groundnut

# %%

top7_groundnut_states = groundnut.groupby('state_name')['groundnut_production_kg'].sum().nlargest(7).reset_index()

fig = px.bar(top7_groundnut_states,
             x='state_name',
             y='groundnut_production_kg',
             title='Top 7 Groundnut Producing state',
             labels={'state_name': 'States', 'groundnut_production_kg': 'Groundnut Production (kg)'},
             text='groundnut_production_kg')

fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig.update_layout(xaxis_tickangle=-45, template='plotly_white')
fig.show(renderer="browser")

# %% [markdown]
# Soyabeans top 7 yield efficiency
# 

# %%
soyabean

# %%
import plotly.graph_objects as go
import pandas as pd

# Step 1: Group and find top 5 states by production
top5_soybean = soyabean.groupby('state_name').agg({
    'soyabean_production_kg': 'sum',
    'soyabean_yield_kg_per_ha': 'sum'  # average yield for context
}).sort_values(by='soyabean_production_kg', ascending=False).head(5).reset_index()

# Step 2: Plotly figure
fig = go.Figure()

# Bar chart for Production
fig.add_trace(go.Bar(
    x=top5_soybean['state_name'],
    y=top5_soybean['soyabean_production_kg'],
    name='Production (kg)',
    marker=dict(color='steelblue'),
    yaxis='y1'
))

# Line chart for Yield Efficiency
fig.add_trace(go.Scatter(
    x=top5_soybean['state_name'],
    y=top5_soybean['soyabean_yield_kg_per_ha'],
    name='Yield Efficiency (kg/ha)',
    mode='lines+markers',
    marker=dict(color='firebrick'),
    yaxis='y2'
))

# Layout: dual y-axis
fig.update_layout(
    title='Soybean Production and Yield Efficiency - Top 5 States',
    xaxis=dict(title='State'),
    yaxis=dict(title='Production (kg)', side='left'),
    yaxis2=dict(title='Yield Efficiency (kg/ha)', overlaying='y', side='right'),
    legend=dict(x=0.01, y=0.99),
    template='plotly_white'
)

fig.show(renderer="browser")


# %% [markdown]
# Oil production states

# %%
oilseed.head()

# %%
top_oil_states = oilseed.groupby('state_name')['oilseeds_production_kg'].sum().reset_index().sort_values(by='oilseeds_production_kg',ascending=False)

fig = px.bar(top_oil_states,
             x='state_name',
             y='oilseeds_production_kg',
             title='Top oilseed Producing state',
             labels={'state_name': 'States', 'oilseeds_production_kg': 'Oilseed Production (kg)'},
             text='oilseeds_production_kg')

fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
fig.update_layout(xaxis_tickangle=-45, template='plotly_white')
fig.show(renderer="browser")

# %% [markdown]
# Rice Vs Wheat for all states

# %%
combined

# %%
# Merge rice & wheat yearly data on 'year'
combined = pd.merge(rice_states[['year', 'rice_production_kg','state_name','rice_yield_kg_per_ha']],
                    wheat_states[['year', 'wheat_production_kg','state_name','wheat_yield_kg_per_ha']],
                    on=['year','state_name']
                    )
combined

# %% [markdown]
# Impact of Area Cultivated on Production (Rice, Wheat, Maize)

# %%
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Create subplots: 1 row, 3 columns
fig = make_subplots(rows=1, cols=3, subplot_titles=("Rice", "Wheat", "Maize"))

# RICE: Area vs Production
fig.add_trace(go.Scatter(
    x=rice_states['rice_area_ha'],
    y=rice_states['rice_production_kg'],
    mode='markers',
    marker=dict(size=5, color='green'),
    name="Rice"
), row=1, col=1)

# WHEAT: Area vs Production
fig.add_trace(go.Scatter(
    x=wheat_states['wheat_area_ha'],
    y=wheat_states['wheat_production_kg'],
    mode='markers',
    marker=dict(size=5, color='blue'),
    name="Wheat"
), row=1, col=2)

# MAIZE: Area vs Production
fig.add_trace(go.Scatter(
    x=maize['maize_area_ha'],
    y=maize['maize_production_kg'],
    mode='markers',
    marker=dict(size=5, color='orange'),
    name="Maize"
), row=1, col=3)

# Update layout
fig.update_layout(
    title_text="Impact of Area Cultivated on Production (Rice, Wheat, Maize)",
    showlegend=False,
    template="plotly_white",
    height=500,
    width=1200
)

# Axis titles
fig.update_xaxes(title_text="Area (ha)", row=1, col=1)
fig.update_yaxes(title_text="Production (kg)", row=1, col=1)

fig.update_xaxes(title_text="Area (ha)", row=1, col=2)
fig.update_yaxes(title_text="Production (kg)", row=1, col=2)

fig.update_xaxes(title_text="Area (ha)", row=1, col=3)
fig.update_yaxes(title_text="Production (kg)", row=1, col=3)

fig.show(renderer="browser")


# %%



