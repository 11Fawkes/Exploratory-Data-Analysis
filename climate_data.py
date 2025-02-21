from image_arrays import image_array, image_to_data_uri
from retrive_data import image_aer_380, image_ch4, image_co, image_hcho, image_no2, image_o3, image_so2

image_dict={"CO":{"image":image_co,"minVal":0.0,"maxVal": 0.1},
            "NO2":{"image":image_no2, "minVal":0.0,"maxVal": 0.0003},
            "HCHO":{"image":image_hcho,"minVal":0.0,"maxVal": 0.001},
            "O3":{"image":image_o3, "minVal":0.0,"maxVal": 0.36},
            "SO2":{"image":image_so2, "minVal":0.0,"maxVal": 0.01},
            "AER":{"image":image_aer_380,"minVal":-1,"maxVal": 5},
            "CH4":{"image":image_ch4, "minVal":1600.0,"maxVal": 2000.0}}

image_uris = {key: image_to_data_uri(value.get('image')) for key, value in image_dict.items()}
image_arrays = {key: image_array(value.get('image')) for key, value in image_dict.items()}
image_shapes = {key: value.shape for key, value in image_arrays.items()}
