config = {
    "version": "v1",
    "config": {
        "visState": {
            "filters": [],
            "layers": [
                {
                    "id": "4hzerr6",
                    "type": "point",
                    "config": {
                        "dataId": "poi_count_isochrone_walk_10m",
                        "label": "Point",
                        "color": [231, 159, 213],
                        "highlightColor": [252, 242, 26, 255],
                        "columns": {
                            "lat": "latitude",
                            "lng": "longitude",
                            "altitude": None,
                        },
                        "isVisible": True,
                        "visConfig": {
                            "radius": 10,
                            "fixedRadius": False,
                            "opacity": 0.8,
                            "outline": False,
                            "thickness": 2,
                            "strokeColor": None,
                            "colorRange": {
                                "name": "Global Warming",
                                "type": "sequential",
                                "category": "Uber",
                                "colors": [
                                    "#5A1846",
                                    "#900C3F",
                                    "#C70039",
                                    "#E3611C",
                                    "#F1920E",
                                    "#FFC300",
                                ],
                            },
                            "strokeColorRange": {
                                "name": "Global Warming",
                                "type": "sequential",
                                "category": "Uber",
                                "colors": [
                                    "#5A1846",
                                    "#900C3F",
                                    "#C70039",
                                    "#E3611C",
                                    "#F1920E",
                                    "#FFC300",
                                ],
                            },
                            "radiusRange": [0, 50],
                            "filled": True,
                        },
                        "hidden": False,
                        "textLabel": [
                            {
                                "field": None,
                                "color": [255, 255, 255],
                                "size": 18,
                                "offset": [0, 0],
                                "anchor": "start",
                                "alignment": "center",
                            }
                        ],
                    },
                    "visualChannels": {
                        "colorField": {
                            "name": "poi_count_qk_isochrone_walk_10m",
                            "type": "integer",
                        },
                        "colorScale": "quantile",
                        "strokeColorField": None,
                        "strokeColorScale": "quantile",
                        "sizeField": None,
                        "sizeScale": "linear",
                    },
                }
            ],
            "interactionConfig": {
                "tooltip": {
                    "fieldsToShow": {
                        "poi_count_isochrone_walk_10m": [
                            {"name": "poi_count_qk_isochrone_walk_10m", "format": None}
                        ]
                    },
                    "compareMode": False,
                    "compareType": "absolute",
                    "enabled": True,
                },
                "brush": {"size": 0.5, "enabled": False},
                "geocoder": {"enabled": False},
                "coordinate": {"enabled": False},
            },
            "layerBlending": "normal",
            "splitMaps": [],
            "animationConfig": {"currentTime": None, "speed": 1},
        },
        "mapState": {
            "bearing": 0,
            "dragRotate": False,
            "latitude": 30.275804189289513,
            "longitude": -97.75164653148035,
            "pitch": 0,
            "zoom": 12.65329400633707,
            "isSplit": False,
        },
        "mapStyle": {
            "styleType": "dark",
            "topLayerGroups": {},
            "visibleLayerGroups": {
                "label": True,
                "road": True,
                "border": False,
                "building": True,
                "water": True,
                "land": True,
                "3d building": False,
            },
            "threeDBuildingColor": [
                9.665468314072013,
                17.18305478057247,
                31.1442867897876,
            ],
            "mapStyles": {},
        },
    },
}
