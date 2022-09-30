dependant_variables = {
    "main_floor": "float",
    "parking_floor_1": "float",
    "parking_floor_2": "float",
    "parking_floor_3": "float",
    "floor_1": "float",
    "floor_2": "float",
    "floor_3": "float",
    "floor_4": "float",
    "floor_5": "float",
    "floor_6": "float",
    "floor_7": "float",
    "floor_8": "float",
    "floor_9": "float",
    "floor_10": "float",
    "floor_11": "float",
    "floor_12": "float",
    "floor_13": "float",
    "floor_14": "float",
    "floor_15": "float",
    "floor_16": "float",
    "floor_17": "float",
    "floor_18": "float",
    "floor_19": "float",
    "floor_20": "float",
    "floor_21": "float",
    "floor_22": "float",
    "floor_23": "float",
    "floor_24": "float",
    "floor_25": "float",
    "floor_26": "float",
    "floor_27": "float",
    "floor_28": "float",
    "floor_29": "float",
    "floor_30": "float",
}

independent_variables = {
    "minutes": "int",
    "upwards_trips": "int",
    "downwards_trips": "int",
    "parkings_occupancy": "float",
    "residents_occupancy": "float",
    "rain_chances": "float",
    "temperature": "float",
    "passengers": "int",
    "water_flux": "float",
    "weight": "float",
}

insert_data = {
    "minutes": 100,
    "upwards_trips": 100,
    "downwards_trips": 100,
    "parkings_occupancy": 0.9,
    "residents_occupancy": 0.9,
    "rain_chances": 0.6,
    "temperature": 15.0,
    "passengers": 100,
    "water_flux": 100.0,
    "weight": 100.0,
}

update_data = {
    "minutes": 20,
    "upwards_trips": 20,
    "downwards_trips": 20,
    "parkings_occupancy": 20,
    "residents_occupancy": 20,
    "rain_chances": 20,
    "temperature": 20,
    "passengers": 20,
    "water_flux": 20,
    "weight": 20,
}

variables = ["upwards_trips",
              "downwards_trips",
              "parkings_occupancy",
              "residents_occupancy",
              "rain_chances",
              "temperature",
              "passengers",
              "water_flux"]

filters = {
    "minutes": (1200, "=")
} 

conditions = {
    "minutes": ("1380", ">"),
    "minutes": ("240", "<")
}