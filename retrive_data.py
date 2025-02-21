
import io
import streamlit as st
from PIL import Image
from matplotlib import pyplot as plt
import requests
from utilities import get_api_headers, past_time, current_time
from line_profiler import LineProfiler, profile


url = "https://creodias.sentinel-hub.com/api/v1/process"
# Retrive the Carbon Monoxide (CO)
@profile
@st.cache_data
def get_carbon_monoxide_data():

    evalscript = """
    //VERSION=3
    //S5P Carbon Monoxide total column mol/m2 (CO)
    var minVal = 0.0;
    var maxVal = 0.1;
    var diff = maxVal - minVal;
    const map = [
        [minVal, 0x00007f],
        [minVal + 0.125 * diff, 0x0000ff],
        [minVal + 0.375 * diff, 0x00ffff],
        [minVal + 0.625 * diff, 0xffff00],
        [minVal + 0.875 * diff, 0xff0000],
        [maxVal, 0x7f0000]
    ];

    const visualizer = new ColorRampVisualizer(map)
    function setup() {
        return {
            input: [
                {
                    bands: ["CO","dataMask"],
                    metadata: ["bounds"],
                }
            ],
            output: [
                {
                    id: "default",
                    bands: 4,
                },
            ],
        };
    }
    function evaluatePixel(samples) {
        const [r, g, b] = visualizer.process(samples.CO);
        const statsVal = isFinite(samples.CO) ? samples.CO : NaN;
        return {
            default: [r, g, b, samples.dataMask],
            eobrowserStats: [statsVal],
            dataMask: [samples.dataMask],
        };
    }
    """
    # Define the payload with coordinates and other parameters
    payload = {
        "input": {
            "bounds": {
                "properties": {
                    "crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
                },
                "geometry": {
                    "type": "MultiPolygon",
                    "coordinates": [
                        [
                            [
                                [8.131946, 55.128649],
                                [11.954962, 54.303704],
                                [13.427042, 54.901882],
                                [14.283925, 54.226708],
                                [14.569553, 53.094024],
                                [14.327868, 52.656394],
                                [14.987008, 51.041394],
                                [14.327868, 50.903033],
                                [12.262561, 50.331436],
                                [13.844498, 48.705463],
                                [13.030709, 47.390912],
                                [12.217769, 47.694974],
                                [11.009344, 47.435519],
                                [10.427103, 47.561701],
                                [10.306261, 47.23449],
                                [9.756977, 47.61357],
                                [9.515292, 47.435519],
                                [8.570524, 47.754098],
                                [8.438019, 47.52091],
                                [7.658036, 47.543164],
                                [7.531701, 47.779943],
                                [7.61378, 48.416442],
                                [8.218246, 48.951366],
                                [7.087178, 49.088258],
                                [6.549782, 49.79545],
                                [6.154298, 50.190968],
                                [6.308097, 50.499452],
                                [5.846699, 51.027576],
                                [6.208104, 51.467697],
                                [5.966419, 51.869708],
                                [6.812316, 51.910391],
                                [6.713445, 52.106505],
                                [6.361903, 53.690201],
                                [8.131946, 55.128649]
                            ]
                        ]
                    ]
                }
            },
            "data": [
                {
                    "dataFilter": {
                        "timeRange": {
                            "from": past_time,
                            "to": current_time
                        },
                        "mosaickingOrder": "mostRecent"
                    },
                    "processing": {
                        "minQa": "50"
                    },
                    "type": "sentinel-5p-l2"
                }
            ]
        },
        "output": {
            "width": 512,
            "height": 700,
            "responses": [
                {
                    "identifier": "default",
                    "format": {
                        "type": "image/png"
                    }
                }
            ]
        },
        "evalscript": evalscript
    }


    # Send the POST request to the API endpoint
    response = requests.post(url, headers=get_api_headers(), json=payload)

    # Handle the response
    if response.status_code == 200:
        image_data = response.content
        image_co = Image.open(io.BytesIO(image_data))
        return image_co
        # Process the response content if needed
    else:
        print(f"Request failed with status code: {response.status_code}")
        print("Response content:", response.text)
        return None
image_co=get_carbon_monoxide_data()

#Retrive the Formaldehyde (HCHO)
@profile
@st.cache_data
def get_formaldehyde_data():

    evalscript = """
    //VERSION=3
    //S5P Formaldehyde tropospheric vertical column mol/m2 (HCHO)
    var minVal = 0.0;
    var maxVal = 0.001;
    var diff = maxVal - minVal;
    const map = [
        [minVal, 0x00007f],
        [minVal + 0.125 * diff, 0x0000ff],
        [minVal + 0.375 * diff, 0x00ffff],
        [minVal + 0.625 * diff, 0xffff00],
        [minVal + 0.875 * diff, 0xff0000],
        [maxVal, 0x7f0000]
    ];

    const visualizer = new ColorRampVisualizer(map)
    function setup() {
        return {
            input: [
                {
                    bands: ["HCHO","dataMask"],
                    metadata: ["bounds"],
                }
            ],
            output: [
                {
                    id: "default",
                    bands: 4,
                },
            ],
        };
    }
    function evaluatePixel(samples) {
        const [r, g, b] = visualizer.process(samples.HCHO);
        const statsVal = isFinite(samples.HCHO) ? samples.HCHO : NaN;
        return {
            default: [r, g, b, samples.dataMask],
            eobrowserStats: [statsVal],
            dataMask: [samples.dataMask],
        };
    }
    """
    # Define the payload with coordinates and other parameters
    payload = {
        "input": {
            "bounds": {
                "properties": {
                    "crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
                },
                "geometry": {
                    "type": "MultiPolygon",
                    "coordinates": [
                        [
                            [
                                [8.131946, 55.128649],
                                [11.954962, 54.303704],
                                [13.427042, 54.901882],
                                [14.283925, 54.226708],
                                [14.569553, 53.094024],
                                [14.327868, 52.656394],
                                [14.987008, 51.041394],
                                [14.327868, 50.903033],
                                [12.262561, 50.331436],
                                [13.844498, 48.705463],
                                [13.030709, 47.390912],
                                [12.217769, 47.694974],
                                [11.009344, 47.435519],
                                [10.427103, 47.561701],
                                [10.306261, 47.23449],
                                [9.756977, 47.61357],
                                [9.515292, 47.435519],
                                [8.570524, 47.754098],
                                [8.438019, 47.52091],
                                [7.658036, 47.543164],
                                [7.531701, 47.779943],
                                [7.61378, 48.416442],
                                [8.218246, 48.951366],
                                [7.087178, 49.088258],
                                [6.549782, 49.79545],
                                [6.154298, 50.190968],
                                [6.308097, 50.499452],
                                [5.846699, 51.027576],
                                [6.208104, 51.467697],
                                [5.966419, 51.869708],
                                [6.812316, 51.910391],
                                [6.713445, 52.106505],
                                [6.361903, 53.690201],
                                [8.131946, 55.128649]
                            ]
                        ]
                    ]
                }
            },
            "data": [
                {
                    "dataFilter": {
                        "timeRange": {
                            "from": past_time,
                            "to": current_time
                        },
                        "mosaickingOrder": "mostRecent"
                    },
                    "processing": {
                        "minQa": "50"
                    },
                    "type": "sentinel-5p-l2"
                }
            ]
        },
        "output": {
            "width": 512,
            "height": 700,
            "responses": [
                {
                    "identifier": "default",
                    "format": {
                        "type": "image/png"
                    }
                }
            ]
        },
        "evalscript": evalscript
    }


    # Send the POST request to the API endpoint
    response = requests.post(url, headers=get_api_headers(), json=payload)

    # Handle the response
    if response.status_code == 200:
        image_data = response.content
        image_hcho = Image.open(io.BytesIO(image_data))
        return image_hcho
        # Process the response content if needed
    else:
        print(f"Request failed with status code: {response.status_code}")
        print("Response content:", response.text)
        return None
image_hcho=get_formaldehyde_data()

# Retrieve Nitrogen Oxide (NO2)
@profile
@st.cache_data
def get_nitrogen_dioxide_data():

    evalscript = """
    //VERSION=3
    //S5P Nitrogen Dioxide tropospheric column mol/m2 (NO2)
    var minVal = 0.0;
    var maxVal = 0.0003;
    var diff = maxVal - minVal;
    const map = [
        [minVal, 0x00007f],
        [minVal + 0.125 * diff, 0x0000ff],
        [minVal + 0.375 * diff, 0x00ffff],
        [minVal + 0.625 * diff, 0xffff00],
        [minVal + 0.875 * diff, 0xff0000],
        [maxVal, 0x7f0000]
    ];

    const visualizer = new ColorRampVisualizer(map)
    function setup() {
        return {
            input: [
                {
                    bands: ["NO2","dataMask"],
                    metadata: ["bounds"],
                }
            ],
            output: [
                {
                    id: "default",
                    bands: 4,
                },
            ],
        };
    }
    function evaluatePixel(samples) {
        const [r, g, b] = visualizer.process(samples.NO2);
        const statsVal = isFinite(samples.NO2) ? samples.NO2 : NaN;
        return {
            default: [r, g, b, samples.dataMask],
            eobrowserStats: [statsVal],
            dataMask: [samples.dataMask],
        };
    }
    """
    # Define the payload with coordinates and other parameters
    payload = {
        "input": {
            "bounds": {
                "properties": {
                    "crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
                },
                "geometry": {
                    "type": "MultiPolygon",
                    "coordinates": [
                        [
                            [
                                [8.131946, 55.128649],
                                [11.954962, 54.303704],
                                [13.427042, 54.901882],
                                [14.283925, 54.226708],
                                [14.569553, 53.094024],
                                [14.327868, 52.656394],
                                [14.987008, 51.041394],
                                [14.327868, 50.903033],
                                [12.262561, 50.331436],
                                [13.844498, 48.705463],
                                [13.030709, 47.390912],
                                [12.217769, 47.694974],
                                [11.009344, 47.435519],
                                [10.427103, 47.561701],
                                [10.306261, 47.23449],
                                [9.756977, 47.61357],
                                [9.515292, 47.435519],
                                [8.570524, 47.754098],
                                [8.438019, 47.52091],
                                [7.658036, 47.543164],
                                [7.531701, 47.779943],
                                [7.61378, 48.416442],
                                [8.218246, 48.951366],
                                [7.087178, 49.088258],
                                [6.549782, 49.79545],
                                [6.154298, 50.190968],
                                [6.308097, 50.499452],
                                [5.846699, 51.027576],
                                [6.208104, 51.467697],
                                [5.966419, 51.869708],
                                [6.812316, 51.910391],
                                [6.713445, 52.106505],
                                [6.361903, 53.690201],
                                [8.131946, 55.128649]
                            ]
                        ]
                    ]
                }
            },
            "data": [
                {
                    "dataFilter": {
                        "timeRange": {
                            "from": past_time,
                            "to": current_time
                        },
                        "mosaickingOrder": "mostRecent"
                    },
                    "processing": {
                        "minQa": "50"
                    },
                    "type": "sentinel-5p-l2"
                }
            ]
        },
        "output": {
            "width": 512,
            "height": 700,
            "responses": [
                {
                    "identifier": "default",
                    "format": {
                        "type": "image/png"
                    }
                }
            ]
        },
        "evalscript": evalscript
    }


    # Send the POST request to the API endpoint
    response = requests.post(url, headers=get_api_headers(), json=payload)

    # Handle the response
    if response.status_code == 200:
        image_data = response.content
        image_no2 = Image.open(io.BytesIO(image_data))
        return image_no2
        # Process the response content if needed
    else:
        print(f"Request failed with status code: {response.status_code}")
        print("Response content:", response.text)
        return None
image_no2=get_nitrogen_dioxide_data()

# Retrive Ozone (O3)
@profile
@st.cache_data
def get_ozone_data():

    evalscript = """
    //VERSION=3
    //S5P Ozone total column mol/m2 (O3)
    var minVal = 0.0
    var maxVal = 0.36;
    var diff = maxVal - minVal;
    const map = [
        [minVal, 0x00007f],
        [minVal + 0.125 * diff, 0x0000ff],
        [minVal + 0.375 * diff, 0x00ffff],
        [minVal + 0.625 * diff, 0xffff00],
        [minVal + 0.875 * diff, 0xff0000],
        [maxVal, 0x7f0000]
    ];

    const visualizer = new ColorRampVisualizer(map)
    function setup() {
        return {
            input: [
                {
                    bands: ["O3","dataMask"],
                    metadata: ["bounds"],
                }
            ],
            output: [
                {
                    id: "default",
                    bands: 4,
                },
            ],
        };
    }
    function evaluatePixel(samples) {
        const [r, g, b] = visualizer.process(samples.O3);
        const statsVal = isFinite(samples.O3) ? samples.O3 : NaN;
        return {
            default: [r, g, b, samples.dataMask],
            eobrowserStats: [statsVal],
            dataMask: [samples.dataMask],
        };
    }
    """
    # Define the payload with coordinates and other parameters
    payload = {
        "input": {
            "bounds": {
                "properties": {
                    "crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
                },
                "geometry": {
                    "type": "MultiPolygon",
                    "coordinates": [
                        [
                            [
                                [8.131946, 55.128649],
                                [11.954962, 54.303704],
                                [13.427042, 54.901882],
                                [14.283925, 54.226708],
                                [14.569553, 53.094024],
                                [14.327868, 52.656394],
                                [14.987008, 51.041394],
                                [14.327868, 50.903033],
                                [12.262561, 50.331436],
                                [13.844498, 48.705463],
                                [13.030709, 47.390912],
                                [12.217769, 47.694974],
                                [11.009344, 47.435519],
                                [10.427103, 47.561701],
                                [10.306261, 47.23449],
                                [9.756977, 47.61357],
                                [9.515292, 47.435519],
                                [8.570524, 47.754098],
                                [8.438019, 47.52091],
                                [7.658036, 47.543164],
                                [7.531701, 47.779943],
                                [7.61378, 48.416442],
                                [8.218246, 48.951366],
                                [7.087178, 49.088258],
                                [6.549782, 49.79545],
                                [6.154298, 50.190968],
                                [6.308097, 50.499452],
                                [5.846699, 51.027576],
                                [6.208104, 51.467697],
                                [5.966419, 51.869708],
                                [6.812316, 51.910391],
                                [6.713445, 52.106505],
                                [6.361903, 53.690201],
                                [8.131946, 55.128649]
                            ]
                        ]
                    ]
                }
            },
            "data": [
                {
                    "dataFilter": {
                        "timeRange": {
                            "from": past_time,
                            "to": current_time
                        },
                        "mosaickingOrder": "mostRecent"
                    },
                    "processing": {
                        "minQa": "50"
                    },
                    "type": "sentinel-5p-l2"
                }
            ]
        },
        "output": {
            "width": 512,
            "height": 700,
            "responses": [
                {
                    "identifier": "default",
                    "format": {
                        "type": "image/png"
                    }
                }
            ]
        },
        "evalscript": evalscript
    }


    # Send the POST request to the API endpoint
    response = requests.post(url, headers=get_api_headers(), json=payload)

    # Handle the response
    if response.status_code == 200:
        image_data = response.content
        image_o3 = Image.open(io.BytesIO(image_data))
        return image_o3
        # Process the response content if needed
    else:
        print(f"Request failed with status code: {response.status_code}")
        print("Response content:", response.text)
        return None
image_o3=get_ozone_data()

#Retrive the Sulphur dioxide (SO2)
@profile
@st.cache_data
def get_sulfur_data():

    evalscript = """
    //VERSION=3
    //S5P Sulfur dioxide total column mol/m2 (SO2)
    var minVal = 0.0;
    var maxVal = 0.01;
    var diff = maxVal - minVal;
    const map = [
        [minVal, 0x00007f],
        [minVal + 0.125 * diff, 0x0000ff],
        [minVal + 0.375 * diff, 0x00ffff],
        [minVal + 0.625 * diff, 0xffff00],
        [minVal + 0.875 * diff, 0xff0000],
        [maxVal, 0x7f0000]
    ];

    const visualizer = new ColorRampVisualizer(map)
    function setup() {
        return {
            input: [
                {
                    bands: ["SO2","dataMask"],
                    metadata: ["bounds"],
                }
            ],
            output: [
                {
                    id: "default",
                    bands: 4,
                },
            ],
        };
    }
    function evaluatePixel(samples) {
        const [r, g, b] = visualizer.process(samples.SO2);
        const statsVal = isFinite(samples.SO2) ? samples.SO2 : NaN;
        return {
            default: [r, g, b, samples.dataMask],
            eobrowserStats: [statsVal],
            dataMask: [samples.dataMask],
        };
    }
    """
    # Define the payload with coordinates and other parameters
    payload = {
        "input": {
            "bounds": {
                "properties": {
                    "crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
                },
                "geometry": {
                    "type": "MultiPolygon",
                    "coordinates": [
                        [
                            [
                                [8.131946, 55.128649],
                                [11.954962, 54.303704],
                                [13.427042, 54.901882],
                                [14.283925, 54.226708],
                                [14.569553, 53.094024],
                                [14.327868, 52.656394],
                                [14.987008, 51.041394],
                                [14.327868, 50.903033],
                                [12.262561, 50.331436],
                                [13.844498, 48.705463],
                                [13.030709, 47.390912],
                                [12.217769, 47.694974],
                                [11.009344, 47.435519],
                                [10.427103, 47.561701],
                                [10.306261, 47.23449],
                                [9.756977, 47.61357],
                                [9.515292, 47.435519],
                                [8.570524, 47.754098],
                                [8.438019, 47.52091],
                                [7.658036, 47.543164],
                                [7.531701, 47.779943],
                                [7.61378, 48.416442],
                                [8.218246, 48.951366],
                                [7.087178, 49.088258],
                                [6.549782, 49.79545],
                                [6.154298, 50.190968],
                                [6.308097, 50.499452],
                                [5.846699, 51.027576],
                                [6.208104, 51.467697],
                                [5.966419, 51.869708],
                                [6.812316, 51.910391],
                                [6.713445, 52.106505],
                                [6.361903, 53.690201],
                                [8.131946, 55.128649]
                            ]
                        ]
                    ]
                }
            },
            "data": [
                {
                    "dataFilter": {
                        "timeRange": {
                            "from": past_time,
                            "to": current_time
                        },
                        "mosaickingOrder": "mostRecent"
                    },
                    "processing": {
                        "minQa": "50"
                    },
                    "type": "sentinel-5p-l2"
                }
            ]
        },
        "output": {
            "width": 512,
            "height": 700,
            "responses": [
                {
                    "identifier": "default",
                    "format": {
                        "type": "image/png"
                    }
                }
            ]
        },
        "evalscript": evalscript
    }


    # Send the POST request to the API endpoint
    response = requests.post(url, headers=get_api_headers(), json=payload)

    # Handle the response
    if response.status_code == 200:
        image_data = response.content
        image_so2 = Image.open(io.BytesIO(image_data))
        return image_so2
        # Process the response content if needed
    else:
        print(f"Request failed with status code: {response.status_code}")
        print("Response content:", response.text)
        return None
image_so2=get_sulfur_data()

#Retrive the Methane (CH4)
@profile
@st.cache_data
def get_methane_data():

    evalscript = """
    //VERSION=3
    //S5P Column averaged dry air mixing ratio of methane (parts per billion PPB) (CH4)
    var minVal = 1600.0;
    var maxVal = 2000.0;
    var diff = maxVal - minVal;
    const map = [
        [minVal, 0x00007f],
        [minVal + 0.125 * diff, 0x0000ff],
        [minVal + 0.375 * diff, 0x00ffff],
        [minVal + 0.625 * diff, 0xffff00],
        [minVal + 0.875 * diff, 0xff0000],
        [maxVal, 0x7f0000]
    ];

    const visualizer = new ColorRampVisualizer(map)
    function setup() {
        return {
            input: [
                {
                    bands: ["CH4","dataMask"],
                    metadata: ["bounds"],
                }
            ],
            output: [
                {
                    id: "default",
                    bands: 4,
                },
            ],
        };
    }
    function evaluatePixel(samples) {
        const [r, g, b] = visualizer.process(samples.CH4);
        const statsVal = isFinite(samples.CH4) ? samples.CH4 : NaN;
        return {
            default: [r, g, b, samples.dataMask],
            eobrowserStats: [statsVal],
            dataMask: [samples.dataMask],
        };
    }
    """
    # Define the payload with coordinates and other parameters
    payload = {
        "input": {
            "bounds": {
                "properties": {
                    "crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
                },
                "geometry": {
                    "type": "MultiPolygon",
                    "coordinates": [
                        [
                            [
                                [8.131946, 55.128649],
                                [11.954962, 54.303704],
                                [13.427042, 54.901882],
                                [14.283925, 54.226708],
                                [14.569553, 53.094024],
                                [14.327868, 52.656394],
                                [14.987008, 51.041394],
                                [14.327868, 50.903033],
                                [12.262561, 50.331436],
                                [13.844498, 48.705463],
                                [13.030709, 47.390912],
                                [12.217769, 47.694974],
                                [11.009344, 47.435519],
                                [10.427103, 47.561701],
                                [10.306261, 47.23449],
                                [9.756977, 47.61357],
                                [9.515292, 47.435519],
                                [8.570524, 47.754098],
                                [8.438019, 47.52091],
                                [7.658036, 47.543164],
                                [7.531701, 47.779943],
                                [7.61378, 48.416442],
                                [8.218246, 48.951366],
                                [7.087178, 49.088258],
                                [6.549782, 49.79545],
                                [6.154298, 50.190968],
                                [6.308097, 50.499452],
                                [5.846699, 51.027576],
                                [6.208104, 51.467697],
                                [5.966419, 51.869708],
                                [6.812316, 51.910391],
                                [6.713445, 52.106505],
                                [6.361903, 53.690201],
                                [8.131946, 55.128649]
                            ]
                        ]
                    ]
                }
            },
            "data": [
                {
                    "dataFilter": {
                        "timeRange": {
                            "from": past_time,
                            "to": current_time
                        },
                        "mosaickingOrder": "mostRecent"
                    },
                    "processing": {
                        "minQa": "50"
                    },
                    "type": "sentinel-5p-l2"
                }
            ]
        },
        "output": {
            "width": 512,
            "height": 700,
            "responses": [
                {
                    "identifier": "default",
                    "format": {
                        "type": "image/png"
                    }
                }
            ]
        },
        "evalscript": evalscript
    }


    # Send the POST request to the API endpoint
    response = requests.post(url, headers=get_api_headers(), json=payload)

    # Handle the response
    if response.status_code == 200:
        image_data = response.content
        image_ch4 = Image.open(io.BytesIO(image_data))
        return image_ch4
        # Process the response content if needed
    else:
        print(f"Request failed with status code: {response.status_code}")
        print("Response content:", response.text)
        return None
image_ch4=get_methane_data()

#Retrive the Aerosol index
@profile
@st.cache_data
def get_AER_AI_340_380_data():

    evalscript = """
    //VERSION=3
    //S5P UV aerosol index from 380 and 340 nm (unitless)
    var minVal = -1;
    var maxVal = 5;
    var diff = maxVal - minVal;
    const map = [
        [minVal, 0x00007f],
        [minVal + 0.125 * diff, 0x0000ff],
        [minVal + 0.375 * diff, 0x00ffff],
        [minVal + 0.625 * diff, 0xffff00],
        [minVal + 0.875 * diff, 0xff0000],
        [maxVal, 0x7f0000]
    ];

    const visualizer = new ColorRampVisualizer(map)
    function setup() {
        return {
            input: [
                {
                    bands: ["AER_AI_340_380","dataMask"],
                    metadata: ["bounds"],
                }
            ],
            output: [
                {
                    id: "default",
                    bands: 4,
                },
            ],
        };
    }
    function evaluatePixel(samples) {
        const [r, g, b] = visualizer.process(samples.AER_AI_340_380);
        const statsVal = isFinite(samples.AER_AI_340_380) ? samples.AER_AI_340_380 : NaN;
        return {
            default: [r, g, b, samples.dataMask],
            eobrowserStats: [statsVal],
            dataMask: [samples.dataMask],
        };
    }
    """
    # Define the payload with coordinates and other parameters
    payload = {
        "input": {
            "bounds": {
                "properties": {
                    "crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
                },
                "geometry": {
                    "type": "MultiPolygon",
                    "coordinates": [
                        [
                            [
                                [8.131946, 55.128649],
                                [11.954962, 54.303704],
                                [13.427042, 54.901882],
                                [14.283925, 54.226708],
                                [14.569553, 53.094024],
                                [14.327868, 52.656394],
                                [14.987008, 51.041394],
                                [14.327868, 50.903033],
                                [12.262561, 50.331436],
                                [13.844498, 48.705463],
                                [13.030709, 47.390912],
                                [12.217769, 47.694974],
                                [11.009344, 47.435519],
                                [10.427103, 47.561701],
                                [10.306261, 47.23449],
                                [9.756977, 47.61357],
                                [9.515292, 47.435519],
                                [8.570524, 47.754098],
                                [8.438019, 47.52091],
                                [7.658036, 47.543164],
                                [7.531701, 47.779943],
                                [7.61378, 48.416442],
                                [8.218246, 48.951366],
                                [7.087178, 49.088258],
                                [6.549782, 49.79545],
                                [6.154298, 50.190968],
                                [6.308097, 50.499452],
                                [5.846699, 51.027576],
                                [6.208104, 51.467697],
                                [5.966419, 51.869708],
                                [6.812316, 51.910391],
                                [6.713445, 52.106505],
                                [6.361903, 53.690201],
                                [8.131946, 55.128649]
                            ]
                        ]
                    ]
                }
            },
            "data": [
                {
                    "dataFilter": {
                        "timeRange": {
                            "from": past_time,
                            "to": current_time
                        },
                        "mosaickingOrder": "mostRecent"
                    },
                    "processing": {
                        "minQa": "50"
                    },
                    "type": "sentinel-5p-l2"
                }
            ]
        },
        "output": {
            "width": 512,
            "height": 700,
            "responses": [
                {
                    "identifier": "default",
                    "format": {
                        "type": "image/png"
                    }
                }
            ]
        },
        "evalscript": evalscript
    }


    # Send the POST request to the API endpoint
    response = requests.post(url, headers=get_api_headers(), json=payload)

    # Handle the response
    if response.status_code == 200:
        image_data = response.content
        image_aer_380 = Image.open(io.BytesIO(image_data))
        return image_aer_380
        # Process the response content if needed
    else:
        print(f"Request failed with status code: {response.status_code}")
        print("Response content:", response.text)
        return None
image_aer_380=get_AER_AI_340_380_data()
