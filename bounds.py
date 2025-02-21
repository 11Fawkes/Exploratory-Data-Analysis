

from line_profiler import profile


coordinates = [
    [[[8.131946, 55.128649], [11.954962, 54.303704], [13.427042, 54.901882],
      [14.283925, 54.226708], [14.569553, 53.094024], [14.327868, 52.656394],
      [14.987008, 51.041394], [14.327868, 50.903033], [12.262561, 50.331436],
      [13.844498, 48.705463], [13.030709, 47.390912], [12.217769, 47.694974],
      [11.009344, 47.435519], [10.427103, 47.561701], [10.306261, 47.23449],
      [9.756977, 47.61357], [9.515292, 47.435519], [8.570524, 47.754098],
      [8.438019, 47.52091], [7.658036, 47.543164], [7.531701, 47.779943],
      [7.61378, 48.416442], [8.218246, 48.951366], [7.087178, 49.088258],
      [6.549782, 49.79545], [6.154298, 50.190968], [6.308097, 50.499452],
      [5.846699, 51.027576], [6.208104, 51.467697], [5.966419, 51.869708],
      [6.812316, 51.910391], [6.713445, 52.106505], [6.361903, 53.690201],
      [8.131946, 55.128649]]]
]
@profile
def find_bounds(coordinates):
    # Initialize min and max values
    min_lat, max_lat = 90, -90
    min_lon, max_lon = 180, -180

    # Iterate through each polygon in the MultiPolygon
    for polygon in coordinates:
        for coord in polygon[0]:  # Assuming each polygon is a list of coordinates
            lon, lat = coord
            min_lat = min(lat, min_lat)
            max_lat = max(lat, max_lat)
            min_lon = min(lon, min_lon)
            max_lon = max(lon, max_lon)

    # Now you have your bounds
    bounds = [[max_lat, min_lon], [min_lat, max_lon]]  # [[top left], [bottom right]
    top_left_coords=bounds[0]
    bottom_right_coords=bounds[1]
    return bounds,top_left_coords,bottom_right_coords
bounds,top_left_coords,bottom_right_coords=find_bounds(coordinates)
