from dataclasses import dataclass
from typing import List, Union

@dataclass
class Star:
    name: str
    type: str

@dataclass
class Binary:
    starA: Star
    starB: Star

@dataclass
class Territory:
    baseTerrain: str
    territoryTrait: str

@dataclass
class Planet:
    name: str
    type: str
    body: str
    gravity: str
    orbitalFeatures: [str]
    atmosphericPresence:str
    atmosphericComposition:str
    climate:str
    habitability:str
    territories: [Territory]

@dataclass
class StarSystem:
    name:str
    keyFeature: str
    star: Star | Binary
    solarZoneInnerElements: list
    solarZoneMiddleElements: list
    solarZoneOuterElements: list



