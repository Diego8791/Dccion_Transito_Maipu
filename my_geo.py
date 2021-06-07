import urllib.request, urllib.parse, urllib.error
import json
import ssl


def adress_locations(adress):
    
    clave_api = False

    # Si tiene una clave API de Google Places, ingresala aquí
    # clave_api = 'AIzaSy___IDByT70'
    # https://developers.google.com/maps/documentation/geocoding/intro

    if clave_api is False:
        clave_api = 42
        url_de_servicio = 'http://py4e-data.dr-chuck.net/json?'
    else :
        url_de_servicio = 'https://maps.googleapis.com/maps/api/geocode/json?'

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    direccion = adress
    
    parms = dict()
    parms['address'] = direccion
    if clave_api is not False: parms['key'] = clave_api
    url = url_de_servicio + urllib.parse.urlencode(parms)

    print('Recuperando...')
    uh = urllib.request.urlopen(url, context=ctx)
    datos = uh.read().decode()
    print('Recuperado!..')

    try:
        js = json.loads(datos)
    except:
        js = None

    if not js or 'status' not in js or js['status'] != 'OK':
        print('==== Error al Recuperar ====')

    try:
        lat = js['results'][0]['geometry']['location']['lat']
        lng = js['results'][0]['geometry']['location']['lng']
        print(lat, lng)
    except:
        print('Direccion no procesada!')
        lat = 0
        lng = 0
        
    return lat, lng
