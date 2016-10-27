from chalice import Chalice
from packages import geoip
import os
app = Chalice(app_name='geoip')
app.debug = True

@app.route('/')
def index():
    return {'hello': 'world'}

@app.route('/where_am_i')
def where_am_i():
   with  geoip.open_database("./packages/GeoLite2-City.mmdb") as db:
      obj = db.lookup(app.current_request.to_dict()['context']['source-ip'])
      print obj
      return serialize_geoip(obj)


def serialize_geoip(geoip_object):
  dict_ = geoip_object.to_dict()
  sub = set(dict_.pop('subdivisions'))
  if sub:
     dict_['subdivisions'] = sub.pop()
  return dict_

@app.route("/headers",method=["GET", "POST"], content_types=['application/x-www-form-urlencoded'])
def headers():
   return app.current_request.headers


@app.route("/r")
def headers():
   return 


@app.route('/map.html')
def map():
   details = where_am_i()
   label = details["ip"]
   x, y = location = details["location"]
   formated = "center: new google.maps.LatLng({x}, {y}),".format(x=x,y=y) 
   return '''<!DOCTYPE html><html><body><h1>My First Google Map</h1><div id='map' style='width:100%;height:500px'></div><script>function myMap() {  var mapCanvas = document.getElementById('map');  var mapOptions = {''' + formated + '''zoom: 10};  var map = new google.maps.Map(mapCanvas, mapOptions);}</script><script src='https://maps.googleapis.com/maps/api/js?key=AIzaSyAEV9MSuB4M-IxGEle3epiOKs3gmSITtuQ&callback=myMap'></script></body></html>'''


'''
<!DOCTYPE html>
<html>
  <head>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
    <meta charset="utf-8">
    <title>Simple markers</title>
    <style>
      /* Always set the map height explicitly to define the size of the div
       * element that contains the map. */
      #map {
        height: 100%;
      }
      /* Optional: Makes the sample page fill the window. */
      html, body {
        height: 100%;
        margin: 0;
        padding: 0;
      }
    </style>
  </head>
  <body>
    <div id="map"></div>
    <script>

      function initMap() {
        var myLatLng = {lat: {{latitude}}, lng: {{logitude}}};
        var map = new google.maps.Map(document.getElementById('map'), {
          zoom: 10,
          center: myLatLng
        });

        var marker = new google.maps.Marker({
          position: myLatLng,
          map: map,
          title: '{{label}}'
        });
      }
    </script>
<script src="https://maps.googleapis.com/maps/api/js?callback=initMap"></script>

</body>
</html>
'''
@app.route('/on_map')
def render_map():
   loc_str = return_requst() 
   location = loc_str.split("location")     

@app.route('/fs')
def show_fs():
   return [f for f in os.walk('.')]

