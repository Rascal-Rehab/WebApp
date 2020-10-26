import pandas as pd 
import geopandas as gp
import geopy as gpy
import matplotlib.pyplot as plt
from shapely import wkt
from scipy.stats import chisquare

#GDP DATA: https://www.bea.gov/data/gdp/gdp-county-metro-and-other-areas
#LatLong Data: https://simplemaps.com/data/us-cities
#state & county .shp files: https://www.census.gov/geographies/mapping-files/time-series/geo/carto-boundary-file.html
#fips: https://www.nrcs.usda.gov/wps/portal/nrcs/detail/sc/home/?cid=nrcs143_013697
#pops: https://www.census.gov/data/datasets/time-series/demo/popest/2010s-counties-total.html#par_textimage_70769902
#geocodes: https://data.healthcare.gov/dataset/Geocodes-USA-with-Counties/52wv-g36k

death_arrests = pd.read_csv('archive/deaths_arrests.csv')
# fatal = pd.read_csv('archive/fatal_encounters_dot_org.csv')
# pdeath = pd.read_csv('archive/police_deaths_538.csv')
pkillings = pd.read_csv('archive/police_killings_MPV.csv', usecols=[0,1,2,3,4,5,6,7,8,9,10,11,13,14,15,17,19])
# shootings = pd.read_csv('archive/shootings_wash_post.csv')
countyGDP = pd.read_excel('archive/countyGDP.xlsx')
fips = pd.read_excel('archive/fips.xlsx')
LatLong = pd.read_csv('archive/simplemaps/uscities.csv', usecols=[0,3,4,6,7,15])
usas = gp.read_file('archive/cb_2018_us_state_20m/cb_2018_us_state_20m.shp')
usac = gp.read_file('archive/cb_2018_us_county_20m/cb_2018_us_county_20m.shp')
pops=pd.read_csv('archive/pops.csv')
geocode=pd.read_csv('archive/GEOCODES.csv', usecols=[2,3,4,5])
#lists and dicts:
usac = usac.drop(['ALAND','AWATER','LSAD','COUNTYNS','AFFGEOID',"GEOID"], axis=1)
countyGDP = countyGDP.drop(['2015 GDP','2016 GDP','2017 GDP',20.17,20.16,20.18],axis=1)
death_arrests = death_arrests.drop(['Total', 'Black','White', 'Amer. Indian', 'Asian', 'Hawaiian', 'Asian/Pacific Islander','Other', 'Two or\r\nmore races', 'Hispanic','Black-White Dissimilarity Index (2010)','Murder and\r\nnonnegligent manslaughter', 'Murder Rate','Avg Annual Police Homicide Rate','Avg Annual Police Homicide Rate for Black People','Avg Annual Police Homicide Rate for White People','Avg Annual Police Homicide Rate for Hispanic People','Black-White Disparity', 'Hispanic-White Disparity','Violent crimes 2013 (if reported by agency)','Violent crimes 2014 (if reported by agency)','Violent crimes 2015 (if reported by agency)','Violent crimes 2016 (if reported by agency)','Violent crimes 2017 (if reported by agency)','Violent crimes 2018 (if reported by agency)','Average Violent Crimes Reported (2013-17)', 'Violent Crime Rate','2013 Total Arrests (UCR Data)', '2014 Total Arrests','2015 Total Arrests', '2016 Total Arrests', '2017 Total Arrests'],axis=1)
usaclst=[]
states=[]
cities=[]
location=[]
locale=[]
ciety=[]
staet=[]
county=[] #list of counties,
statebyc=[] #list of states, indexed by appeareance in county list
csloc=[] #string from df, as (county, state)
statefull=[] #full names of states, used as an intermediary for one of the dataframes for merging them
stategdp=[]
usaclocat=[]
usacGDPPC=[]
statefipsfull=[]
usacCS=[]
southeast=['Arkansas','Alabama', 'Florida', 'Georgia', 'Kentucky', 'Louisiana', 'Mississippi', 'North Carolina', 'South Carolina', 'Tennessee', 'Puerto Rico', 'Virginia']
northeast=['Connecticut', 'Delaware', 'Maryland', 'Massachusetts', 'Maine', 'New Hampshire', 'New Jersey', 'New York', 'Pennsylvania', 'Rhode Island', 'Vermont', 'West Virginia']
pacific_west=['California','Hawaii','Alaska','Idaho','Nevada','Oregon','Washington','Arizona','Utah']
midwest=['Illinois', 'Indiana', 'Iowa', 'Michigan', 'Minnesota', 'Missouri','Ohio', 'Wisconsin']
plains=['Kansas','Texas','New Mexico','Colorado','Oklahoma','Nebraska','South Dakota','North Dakota','Montana','Wyoming']
statesforend=['Kansas','Texas','New Mexico','Colorado','Oklahoma','Nebraska','South Dakota','North Dakota','Montana','Wyoming','Illinois', 'Indiana', 'Iowa', 'Michigan', 'Minnesota', 'Missouri','Ohio', 'Wisconsin', 'Connecticut', 'Delaware', 'Maryland', 'Massachusetts', 'Maine', 'New Hampshire', 'New Jersey', 'New York', 'Pennsylvania', 'Rhode Island', 'Vermont', 'West Virginia', 'Arkansas','Alabama', 'Florida', 'Georgia', 'Kentucky', 'Louisiana', 'Mississippi', 'North Carolina', 'South Carolina', 'Tennessee', 'Puerto Rico', 'Virginia','California','Hawaii','Alaska','Idaho','Nevada','Oregon','Washington','Arizona','Utah']
SEz={'ymin':24,'ymax':40,'xmin':-102,'xmax':-73}
NEz={'ymax':48,'ymin':36.5,'xmax':-67,'xmin':-83}
PWz={'ymax':50,'ymin':30.5,'xmin':-125,'xmax':-108}
MWz={'ymin':36,'ymax':50,'xmin':-97.5,'xmax':-77.5}
Pz={'ymin':25,'ymax':50,'xmin':-117,'xmax':-92}
statesdict = {'FM':'other','MH':'other','AE':'Armed Forces, Europe','AP':'Armed Forces, Pacific','PW':'Palau','AA':'Armed Forces, Americas','VI':'Virgin Islands','GU':'Guam','MP':'Northern Marianas','AS':"American Samoa","DC":"District of Columbia","PR":"Puerto Rico","AL":"Alabama","AK":"Alaska","AZ":"Arizona","AR":"Arkansas","CA":"California","CO":"Colorado","CT":"Connecticut","DE":"Delaware","FL":"Florida","GA":"Georgia","HI":"Hawaii","ID":"Idaho","IL":"Illinois","IN":"Indiana","IA":"Iowa","KS":"Kansas","KY":"Kentucky","LA":"Louisiana","ME":"Maine","MD":"Maryland","MA":"Massachusetts","MI":"Michigan","MN":"Minnesota","MS":"Mississippi","MO":"Missouri","MT":"Montana","NE":"Nebraska","NV":"Nevada","NH":"New Hampshire","NJ":"New Jersey","NM":"New Mexico","NY":"New York","NC":"North Carolina","ND":"North Dakota","OH":"Ohio","OK":"Oklahoma","OR":"Oregon","PA":"Pennsylvania","RI":"Rhode Island","SC":"South Carolina","SD":"South Dakota","TN":"Tennessee","TX":"Texas","UT":"Utah","VT":"Vermont","VA":"Virginia","WA":"Washington","WV":"West Virginia","WI":"Wisconsin","WY":"Wyoming"}
def strcat(a,b):
    return str(f"{a}, {b}")
pkillings["County"]=pkillings['County'].str.lower()
pkillings["State"]=pkillings['State'].str.upper()
pkillstate=[]
pkillcounty=[]
statefullname=[]
pkillfull=[]
geocodes=[]
geocodec=[]
geocodesf=[]
geocodesfn=[]
for iter in range(len(pkillings)):
    pkillstate.append(pkillings.iloc[iter,8])
    pkillcounty.append(pkillings.iloc[iter,10])
for iter in pkillstate:
    statefullname.append(statesdict[iter].lower())
for iter in range(len(pkillings)):
    pkillfull.append(strcat(pkillcounty[iter],statefullname[iter]))
for iter in range(len(geocode)):
    geocodec.append(str(geocode.iloc[iter,3]).lower())
    geocodes.append(geocode.iloc[iter,0])
for iter in geocodes:
    geocodesfn.append(statesdict[iter].lower())
for iter in range(len(geocodes)):
    geocodesf.append(strcat(geocodec[iter],geocodesfn[iter]))
geocode['locat']=geocodesf
pkillings['locat']=pkillfull
geocode = geocode.drop(['state','county'], axis=1)
geocode = geocode.drop_duplicates(subset='locat',keep='first',ignore_index=True)
pkillings= pkillings.merge(geocode, on='locat', how='left')
pkillings.fillna(0,inplace=True)
latlist=pkillings['latitude'].tolist()
longlist=pkillings['longitude'].tolist()
def cordsappend(x,y):
    return str(f"POINT({x} {y})")
cordina=[]
for iter in range(len(latlist)):
    latlist[iter] = float(latlist[iter])
    longlist[iter]= float(longlist[iter])
    cordina.append(cordsappend(longlist[iter],latlist[iter]))
pkillings['Coordinates']= cordina
pkillings['Coordinates'] = pkillings['Coordinates'].apply(wkt.loads)
gdf = gp.GeoDataFrame(pkillings, geometry='Coordinates')

for iter in range(29488):
    staet.append(str(LatLong.iloc[iter,1]).lower())
    ciety.append(str(LatLong.iloc[iter,0]).lower())
    locale.append([ciety[iter], staet[iter]])
for iter in range(106):
    states.append(str(death_arrests.iloc[iter,0]).lower())
    cities.append(str(death_arrests.iloc[iter,1]).lower())
    location.append([cities[iter], states[iter]])
for iter in countyGDP.iloc[:,-1]:
    csloc.append(iter)
for iter in csloc:
    try:
        county.append(iter.split(',',1)[0].lower())
    except:
        county.append(0)
    try:
        statebyc.append(iter.split(',',1)[1].lower())
    except:
        statebyc.append(0)
countyGDP['counties'] = county
countyGDP['State'] = statebyc
for iter in statebyc:
    if iter == 0:
        x=statebyc.index(iter)
        statebyc.remove(iter)
        county.remove(county[x])
def stateplot(states, us_map=True, incidents=True):
    fig, ax1 = plt.subplots(figsize=(8,8))
    if incidents == True:
        gdf.plot(ax=ax1, color='red', markersize=2) #FIX THIS LINE REFERENCE
    if us_map:
        ax1.set_xlim(left=-180,right=-60)
        ax1.set_ylim(ymin=15, ymax =100)
        if 'Hawaii' in states:
            usas[:7].plot(ax=ax1, alpha =.3)
            usas[8:25].plot(ax=ax1, alpha =.3)
            usas[26:].plot(ax=ax1, alpha =.3)
        elif "Puerto Rico" in states:
            usas[:25].plot(ax=ax1, alpha =.3)
            usas[26:48].plot(ax=ax1, alpha =.3)
            usas[49:].plot(ax=ax1, alpha =.3)
        elif "Alaska" in states:
            usas[:7].plot(ax=ax1, alpha=.3)
            usas[8:48].plot(ax=ax1, alpha =.3)
            usas[49:].plot(ax=ax1, alpha =.3)
        elif "Alaska" and "Puerto Rico" in states:
            usas[:48].plot(ax=ax1, alpha =.3)
            usas[49:].plot(ax=ax1, alpha =.3)
        elif "Puerto Rico" and "Hawaii" in states:
            usas[:25].plot(ax=ax1, alpha =.3)
            usas[26:].plot(ax=ax1, alpha =.3)
        elif 'Hawaii' and 'Alaska' in states:
            usas[:7].plot(ax=ax1, alpha =.3)
            usas[8:].plot(ax=ax1, alpha =.3)
        elif "Hawaii" and "Alaska" and "Puerto Rico" in states:
            usas[:].plot(ax=ax1, alpha =.3)
        else:
            usas[:7].plot(ax=ax1, alpha =.3)
            usas[8:25].plot(ax=ax1, alpha =.3)
            usas[26:48].plot(ax=ax1, alpha =.3)
            usas[49:].plot(ax=ax1, alpha =.3)
            ax1.set_xlim(left=-130,right=-60)
            ax1.set_ylim(ymin=23, ymax=53)
        for n in states:
            usas[usas.NAME == f'{n}'].plot(ax=ax1, edgecolor='k', alpha=.3,linewidth=1)
    elif us_map == False: #Need selective zooming on state 'n' somehow, or maybe just for regional selections.... REVIEW: See regional lists and subset usage below
        for n in states:
            usas[usas.NAME == f'{n}'].plot(ax=ax1, edgecolor='k',alpha=.3, linewidth=1)
    if all(x in southeast for x in states):
        ax1.set_xlim(left=SEz['xmin'], right=SEz['xmax'])
        ax1.set_ylim(ymin=SEz['ymin'], ymax=SEz['ymax'])
    elif all(x in northeast for x in states):
        ax1.set_xlim(left=NEz['xmin'], right=NEz['xmax'])
        ax1.set_ylim(ymin=NEz['ymin'], ymax=NEz['ymax'])
    elif all(x in pacific_west for x in states):
        ax1.set_xlim(left=PWz['xmin'], right=PWz['xmax'])
        ax1.set_ylim(ymin=PWz['ymin'], ymax=PWz['ymax'])
    elif all(x in midwest for x in states):
        ax1.set_xlim(left=MWz['xmin'], right=MWz['xmax'])
        ax1.set_ylim(ymin=MWz['ymin'], ymax=MWz['ymax'])
    elif all(x in plains for x in states):
        ax1.set_xlim(left=Pz['xmin'], right=Pz['xmax'])
        ax1.set_ylim(ymin=Pz['ymin'], ymax=Pz['ymax'])
    plt.ylabel('Latitude')
    plt.xlabel("Longitude")
    plt.axis('off')
def concat(a, b):
    return int(f"{a}{b}")
for iter in range(len(usac)):
    usaclst.append(concat(usac.iloc[iter,0],usac.iloc[iter,1]))
    if usac.iloc[iter, -1]==None:
        usac.drop(index=iter)
    elif usac.iloc[iter,-1]==0:
        usac.drop(index=iter)
usac['FIPS']=usaclst
usac = usac.merge(fips, how='inner',on='FIPS')
for iter in fips['State']:
    statefipsfull.append(statesdict[iter].lower())
fips['FullState']=statefipsfull
for iter in usac['State']:
    statefull.append(statesdict[iter].lower())
usac['StateFull']=statefull
for iter in range(len(usac)):
    usaclocat.append(strcat(usac.iloc[iter,-3],usac.iloc[iter,-1]))
usac['locat']=usaclocat
usac['locat']=usac['locat'].str.lower()
usac['Name']=usac['Name'].str.lower()
countyGDP[', ']=countyGDP[', '].str.lower()
usac = usac.drop(['STATEFP','COUNTYFP','NAME'], axis=1)
usac = usac.merge(countyGDP, left_on='locat', right_on=', ',how='inner')
pops['Area']=pops['Area'].str.lower()
usac = usac.merge(pops, left_on=', ', right_on='Area',how='inner')
usac = usac.drop(['Area','State_x','list','locat','Name','State_y'],axis=1)
def capita(gdp,pop):
    return float((gdp/pop)*1000)
for iter in range(len(usac)):
    usacGDPPC.append(capita(int(usac.iloc[iter,3]),int(usac.iloc[iter,-1])))
    usacCS.append(strcat(usac.iloc[iter,-2],usac.iloc[iter,2]))
usac['GDPPC']=usacGDPPC
# usac['CS']=usacCS
# usac = usac.drop(['StateFull','counties'], axis=1)

#county plots
vmin= usac['GDPPC'].min()
vmax= 150000
ax2 = usac.plot(edgecolor='black', legend=True,cmap='YlOrBr_r',column='GDPPC',vmin=vmin, vmax=vmax, legend_kwds={'label':'GDP Per Capita', 'orientation':'horizontal'})
gdf.plot(ax=ax2, marker='X',color='lime',markersize=4)
ax2.set_xlim(left=-130,right=-60)
ax2.set_ylim(ymin=23, ymax=53)
plt.ylabel('Latitude')
plt.xlabel('Longitude')
plt.axis('off')
# plt.savefig("static/contcounty_plt.svg")

#Must be correctly capitalized for this function call to work // input a regional list name, as shown
stateplot(['South Carolina'],us_map=True)
plt.axis('off')
# plt.show()

pkillings=pkillings.merge(usac, left_on='locat', right_on=', ', how='left')
pkillings=pkillings.drop([', ','counties','Victim\'s gender','2018 Relative Ranking','2018 % Rank','FIPS','StateFull','URL of image of victim','Agency responsible for death','Cause of death'],axis=1)
pkillings = pkillings.drop_duplicates(subset='GDPPC',keep='first',ignore_index=True)

# fff=0
# biny=[]
# while fff < 1000000:
#     biny.append(fff)
#     fff = fff+10000

# plt.subplots(figsize=(8,8))
# plt.hist(usac['Pop. Est'],alpha=.5,label='All US Counties',bins=biny)
# plt.hist(pkillings['Pop. Est'],alpha=.5,label='All Counties with Reported Incidents',bins=biny)
# plt.legend(loc='upper right')
# plt.xlabel('Population')
# plt.ylabel("Frequency")
# plt.savefig('static/HISTPOP.svg', format='svg')

#Rkill chart
labels = 'White', 'Black', 'Hispanic', 'Asian', 'Pacific-Islander', 'other'
sizes = [death_arrests.iloc[101,8], death_arrests.iloc[101,3], death_arrests.iloc[101,4], death_arrests.iloc[101,6],death_arrests.iloc[101,7],death_arrests.iloc[101,9]]
fig3, ax3 = plt.subplots(figsize=(8,8))
ax3.pie(sizes, autopct='%1.1f%%',pctdistance=1.1, shadow=False, startangle=180)
ax3.legend(labels=labels, loc='lower left')
ax3.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
ax3.set_title('Police Killings, Categorized by Race')
plt.savefig("Rkill_plt.svg", format='svg')
#RComp chart
labelsA = 'White', 'Black', 'Hispanic', 'Asian', 'Pacific-Islander','other'
sizesA = [76.3, 13.4, 18.5, 5.9, 0.2, 2.8] #according to data drawn from the US census Bureau, current as of 10/13/2020
fig4, ax4 = plt.subplots(figsize=(8,8))
ax4.pie(sizesA, autopct='%1.1f%%',pctdistance=1.1, startangle=180)
ax4.legend(labels=labelsA)
ax4.axis('equal')
ax4.set_title("Racial Composition within America")
plt.savefig("Rcomp_plt.svg", format='svg')
# plt.show()