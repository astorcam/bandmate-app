import googlemaps
import requests
API_KEY='AIzaSyAO-2U9g7LQ0fHvkI4IfDBL_adMQflkcV4'
direccion='Calle Bilbao, 5, Getxo'
params = {
    'key': API_KEY,
    'address': direccion}

url = 'https://maps.googleapis.com/maps/api/geocode/json?'

response = requests.get(url, params=params).json()
response.keys()
print('ha llegado aqui 1')
if response['status'] == 'OK':
    print('ha llegado aqui 2')
    location = response['results'][0]['geometry']['location']
    print(location['lat']) 
    print(location['lng'])

else:
    print('No ha encontrado nada')
