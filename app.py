from flask import Flask, request
from flask_restful import Api, Resource
import geopandas as gpd
from shapely.geometry import Point


app = Flask(__name__)
api = Api(app)




class GeoFence(Resource):
    def get(self):
        latitude = request.args.get('latitude')
        longitude = request.args.get('longitude')

        if latitude and longitude:
                # Path to the shapefile
            shapefile_path = 'shapefile_500/grid.shp'

            # Read the shapefile
            dataframe = gpd.read_file(shapefile_path)

            polygon_id = self.find_polygon_id(latitude, longitude, dataframe)

            return {    "success": True ,"message": "in grid {}".format(polygon_id)}, 200
        
        else:
            return {    "success": False, "message": "Bad request, latitude or longitude can't be empty"}, 400
        
    def find_polygon_id(self, latitude, longitude, shapefile):
        point = gpd.GeoSeries([Point(longitude, latitude)])
        point_in_polygons = shapefile.contains(point.geometry[0])

        if any(point_in_polygons):
            polygon_ids = shapefile.loc[point_in_polygons, 'id']
            if len(polygon_ids) > 1:
                return -2  # in multiple polygons, should never happen
            else:
                return polygon_ids.iloc[0]
        else:
            return -99  # not in any of the polygons
        
api.add_resource(GeoFence, '/geofence')

