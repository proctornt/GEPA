import ee
# ee.Authenticate()
ee.Initialize()

import geopandas
import geopy
from geopy.geocoders import Nominatim

adress=str(input("What is the address? "))

locator = Nominatim(user_agent='myGeocoder')
location = locator.geocode(adress)

u_lat=(location.latitude)
u_long=(location.longitude)
U_point=ee.Geometry.Point(u_long, u_lat)
#ucal berkley
dataset = ee.Image('WORLDCLIM/V1/BIO')
annualrain = dataset.select('bio12')    
#European Space Agency Data, some college in Belgium
landcoverdata=ee.Image("ESA/GLOBCOVER_L4_200901_200912_V2_3")
landtype=landcoverdata.select('landcover')
#Eu, Copernicus Climate Project 
collection = ee.ImageCollection("ECMWF/ERA5/MONTHLY").filterBounds(U_point).filterDate('1980-01-01', '2022-10-01')
reduced_to_image = collection.reduce(ee.Reducer.mean())



scale= 100

rainmm= annualrain.sample(U_point, scale).first().get('bio12').getInfo()


temp = reduced_to_image.sample(U_point,100).first().get('mean_2m_air_temperature_mean').getInfo()



landcover=landtype.sample(U_point,100).first().get('landcover').getInfo()

rain=rainmm/25.4



#Dictionary 
thisdict = {
  11: "Post-flooding or irrigated croplands",
  14: "Rainfed croplands",
  20: "Mosaic cropland (50-70%)/vegetation (grassland, shrubland, forest)(20-50%)",
  30: "Mosaic vegetation (grassland, shrubland,forest)(50-70%)/cropland(20-50%)",
  40: "Closed to open (>15%) broadleaved evergreen and/or semi-decidous forest (>5m)",
  50: "Closed (>40%) broadleaved decidous forest (>5m)",
  60: "Open (15-40%) broadleaved deciduos forest (>5m)",
  70: "Closed (>40%) needleleaved evergreen forest (>5m)",
  90:"Open (15-40%) needleleaved deciduous or evergreen forest (>5m)",
  100:"Closed to open (>15%) mixed broadleaved and needleleaved forest (>5m)",
  110: "Mosaic forest-shrubland (50-70%) / grassland (20-50%)",
  120: "Mosaic grassland (50-70%) / forest-shrubland (20-50%)",
  130: "Closed to open (>15%) shrubland (<5m)",
  140: "Closed to open (>15%) grassland",
  150: "Sparse (>15%) vegetation (woody vegetation, shrubs, grassland)",
  160:"Closed (>40%) broadleaved forest regularly flooded - Fresh water",
  170:"Closed (>40%) broadleaved semi-deciduous and/or evergreen forest regularly flooded - saline water",
  180: "Closed to open (>15%) vegetation (grassland, shrubland, woody vegetation) on regularly flooded or waterlogged soil - fresh, brackish or saline water",
  190: "Artificial surfaces and associated areas (urban areas >50%) GLOBCOVER 2009",
  200:"Bare areas",
  210:"Water bodies",
  220:"Permanent snow and ice",
  230:"Unclassified"


}


x = thisdict.get(landcover)


tempf=1.8*(temp-273) + 32.
#tempf=(tempc/.875)+32
print(rain,"Inches")
print(tempf,"Fahrenheit")
print(x)
print(u_long,u_lat)