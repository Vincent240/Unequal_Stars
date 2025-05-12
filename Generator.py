import pprint
import random
import string

import TextLists as TL
from StorageDataclasses import Star, Binary, Planet, StarSystem

inner_zone = "Inner Cauldron"
middle_zone = "Primary Biosphere"
outer_zone = "Outer Reaches"

def generate_name(cosmic_body_type) -> str:
    letter = random.choice(string.ascii_uppercase)
    number = random.randint(1, 99)
    name = cosmic_body_type + " " + letter + str(number)
    return name


def generate_star() -> Star:
    star_type = random.choice(list(TL.STAR_TYPES.keys()))
    name = generate_name("Star")
    return Star(name=name, type=star_type)


def generate_binary() -> Binary:
    stargen = random.randint(1, 10)
    if stargen >= 8:
        star_a = generate_star()
        star_b = generate_star()
    else:
        star_type = random.choice(list(TL.STAR_TYPES.keys()))
        star_a = Star(generate_name("Star"), star_type)
        star_b = Star(generate_name("Star"), star_type)
    return Binary(starA=star_a, starB=star_b)


def generate_planet(planet_type=random.choice(TL.PLANET_TYPES)) -> Planet:
    name = generate_name(planet_type)
    if planet_type == "Gas Giant":
        body = random.choice(list(TL.PLANET_GAS_BODY_TYPES.keys()))
        gravity = random.choice(list(TL.PLANET_GAS_GRAVITY.keys()))
        orbital_features = random.choice(list(TL.PLANET_GAS_ORBITALS.keys()))
        atmospheric_presence = "Gas Giant"
        atmospheric_composition = random.choice(list(TL.PLANET_GAS_CLASS.keys()))
        climate = "None"
        habitability = "Not Habitable"
        territories = []
    else:
        body = random.choice(list(TL.PLANET_ROCKY_BODY_TYPES.keys()))
        gravity = random.choice(list(TL.PLANET_ROCKY_GRAVITY.keys()))
        orbital_features = random.choice(list(TL.PLANET_ROCKY_ORBITALS.keys()))
        atmospheric_presence = random.choice(list(TL.PLANET_ATMOSPHERIC_PRESENCE.keys()))
        atmospheric_composition = random.choice(list(TL.PLANET_ATMOSPHERIC_COMPOSITION.keys()))
        climate = random.choice(list(TL.PLANET_CLIMATES.keys()))
        habitability = random.choice(list(TL.PLANET_HABITABILITY.keys()))
        territories = []
    return Planet(name, planet_type, body, gravity, orbital_features, atmospheric_presence, atmospheric_composition,
                  climate, habitability, territories)


def populate_solar_zones(key_feature, inner_str, middle_str, outer_str) -> list:
    inner_zone_elements = random.choices(TL.SYSTEM_ZONES_ALLOWED.get(inner_zone,[]),weights=TL.SYSTEM_ZONES_WEIGHTS.get(inner_zone), k=inner_str)
    middle_zone_elements = random.choices(TL.SYSTEM_ZONES_ALLOWED.get(middle_zone,[]),weights=TL.SYSTEM_ZONES_WEIGHTS.get(middle_zone), k=middle_str)
    outer_zone_elements = random.choices(TL.SYSTEM_ZONES_ALLOWED.get(outer_zone,[]),weights=TL.SYSTEM_ZONES_WEIGHTS.get(outer_zone), k=outer_str)
    solar_zones = [inner_zone_elements, middle_zone_elements, outer_zone_elements]

    for zone in solar_zones:
        for i, element in enumerate(zone):
             if element in ("Planet", "Gas Giant"):
                 zone[i] = generate_planet(element)

    if key_feature == "Bountiful":
        feature_element = random.choice(["Asteroid Cluster","Asteroid Belt"])
        random.choice(solar_zones).append(feature_element)
    if key_feature == "Gravity Tides":
        for _ in range(random.randint(1, 5)):
            random.choice(solar_zones).append(key_feature)
    if key_feature == "Haven":
        for zone in solar_zones:
            zone.append(generate_planet())
    if key_feature == "Starfarers":
        existing_planets = sum(isinstance(obj, Planet) for zone in solar_zones for obj in zone)
        while existing_planets < 4:
            random.choice(solar_zones).append(generate_planet())
            existing_planets += 1

    return solar_zones


def get_binary_zone_str(binary: Binary) -> list:
    star_type_rank = list(TL.STAR_TYPES.keys())
    if star_type_rank.index(binary.starA.type) < star_type_rank.index(binary.starB.type):
        star_str = TL.STAR_TYPES_SOLAR_ZONES[binary.starA.type]
    else:
        star_str = TL.STAR_TYPES_SOLAR_ZONES[binary.starB.type]

    return star_str


def get_star_zone_str(star: Star) -> list:
    star_str = TL.STAR_TYPES_SOLAR_ZONES[star.type]

    return star_str


def create_star_system() -> StarSystem:
    name = generate_name("System")
    key_feature = random.choice(list(TL.SYSTEM_FEATURES.keys()))
    star = random.choices([generate_star(), generate_binary()], weights=[9, 1], k=1)[0]

    if isinstance(star, Binary):
        solar_zone_str = get_binary_zone_str(star)
    else:
        solar_zone_str = get_star_zone_str(star)

    solar_zone_str_inner = random.randint(1, 5) + solar_zone_str[0]
    solar_zone_str_middle = random.randint(1, 5) + solar_zone_str[1]
    solar_zone_str_outer = random.randint(1, 5) + solar_zone_str[2]

    solar_zones = populate_solar_zones(key_feature, solar_zone_str_inner, solar_zone_str_middle, solar_zone_str_outer)

    return StarSystem(name, key_feature, star, solar_zones[0], solar_zones[1], solar_zones[2])


if __name__ == "__main__":
    # single_star = create_star()
    # star_str = get_star_zone_str(single_star)
    # print(single_star)
    # print(star_str)

    # pprint.pprint(single_star, width=45)
    # pprint.pprint(TextList.STAR_TYPES[single_star.type])

    # binary_star = create_binary()
    # pprint.pprint(binary_star, width=45)
    #
    # planet = create_planet()
    # pprint.pprint(planet, width=45)

    star_system = create_star_system()
    pprint.pprint(star_system)
