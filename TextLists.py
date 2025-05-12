import random

STAR_TYPES = {
    "Mighty": "The fierce light of this star dominates its system utterly. Its coloration is likely to be blue or blue-white. The Inner Cauldron is dominant, and the Primary Biosphere is weak.",
    "Vigorous": "A steady illumination burns forth from the heart of this star. Its coloration is likely to be a pure white.",
    "Luminous": "Though it is has been long aeons since this star has shone at its brightest, a constant glow nonetheless provides for the system. It is likely to be yellow or yellow-orange in colour. The Inner Cauldron is weak.",
    "Dull": "The end of the star’s life advances inexorably, although it can still burn for millennia yet. Many stars of this type are of a vast size, seemingly incongruous with their wan light. Its coloration is likely a sullen red. The Outer Reaches are Dominant.",
    "Anomalous": "The star is an unnatural outlier, shedding a strange light that behaves in ways it should not. Its light can be of any colour, even one that is not typical for a star, from bilious green to barely-visible purple. The Game Master can choose to make one Solar Zone dominant or weak at his discretion.",
}
STAR_TYPES_SOLAR_ZONES = {
    "Mighty": (2,-2,0),
    "Vigorous": (0,0,0),
    "Luminous": (-2,0,0),
    "Dull": (0,0,2),
    "Anomalous": tuple(random.choice([-2,0,2]) for _ in range(3))
}

PLANET_TYPES = ["Planet","Gas Giant"]
PLANET_ROCKY_BODY_TYPES = {
    "Low Mass": "The world is even lower in mass than its small size would suggest. It is likely comprised of light materials, or it has large pockets of trapped gas making up much of its volume.",
    "Small": "This world lacks the mass and size to support significant gravity or resources.",
    "Small and Dense": "The shrunken silhouette of this Planet belies the strength of its gravity well and the richness of its crust.",
    "Large": "Worlds of this size can range across a vast spectrum of possible types.",
    "Large and Dense": "Though impressive in volume, the mass of this world is, in fact, compressed significantly.",
    "Vast": "Huge and voluminous, worlds of this type strain the upper edges of the possible size for a single world. Such Planets tend to be of middling density, as they are already more massive than is common."
}
PLANET_GAS_BODY_TYPES = {
    "Gas Dwarf": "Although much smaller than the typical world of this sort, a Gas Dwarf is still considerably more massive than most rocky Planets",
    "Gas Giant": "Typical gas giants are vastly more massive than almost any other world, and tend to have correspondingly powerful gravitational effects.",
    "Massive Gas Giant": "The largest gas giants can rival weaker stars in size and mass, with some of them having some degree of kinship with such bodies."
}
PLANET_ROCKY_GRAVITY = {
    "Low Gravity": "Low Gravity Worlds rule is in effect",
    "Normal Gravity": "Terran-standard gravity. No modifiers.",
    "High Gravity": "Strong gravitational pull."
}
PLANET_GAS_GRAVITY = {
    "Weak": "Though puny by the standards of gas giants, this gravity well is stronger than that of almost any solid Planet",
    "Strong": "This gas giant has the impressive gravity well common to such worlds.",
    "Powerful": "The influence of this gravity well extends well beyond the immediate presence of its source, drawing in whatever passes by",
    "Titanic": "The effects of such a vast gravity well on the ordering of the System are second only to it's Star"
    }
PLANET_ROCKY_ORBITALS = {
    "No Features": "No notable features are added to the Planet’s orbit.",
    "Large Asteroid": "An asteroid of unusual size has been captured by the Planet’s gravity well, and now occupies a stable orbit around it.",
    "Lesser Moon": "An orbital body somewhere between an extremely large asteroid and a very small moon orbits the Planet. It has its own extremely limited gravity well, allowing low-gravity travel across the surface.",
    "Moon": "A true moon. Quarter the size of the actual planet it orbits, it's surface contains mineral remnants of the planets formation."
}
PLANET_GAS_ORBITALS = {
    "No Features": "No notable features are added to the Gas Giant’s orbit.",
    "Planetary Rings (Debris)": "A narrow band of asteroids or chunks of ice extends out around the Gas Giant.",
    "Planetary Rings (Dust)": "A wide ring of fine particles encircles the gas giant.",
    "Lesser Moon": "An orbital body somewhere between an extremely large asteroid and a very small moon orbits the Gas Giant.",
    "Moon": "A true moon. Less than a quarter the size of the actual planet it orbits, it's surface contains mineral remnants of the planets formation."
}
PLANET_ATMOSPHERIC_PRESENCE = {
    "None": "The Planet has no atmosphere, or it has one so thin as to be effectively nonexistent. Activity on the Planet is treated as being in vacuum"
}
PLANET_ATMOSPHERIC_COMPOSITION = {
    "Deadly": "An atmosphere of this sort is little more than a vast acid bath."
}
PLANET_GAS_CLASS = {
    "Class I": "Cold gas giants with thick ammonia clouds dominating their upper atmospheres.",
    "Class II": "Slightly warmer gas giants where water vapor condenses into high-altitude clouds.",
    "Class III": "Hotter gas giants lacking significant cloud cover, with deep, clear atmospheres.",
    "Class IV": "Very hot gas giants where alkali metals like sodium and potassium create colorful hazes.",
    "Class V": "Extremely hot \"roasters\" with high-altitude silicate and iron clouds."
}
PLANET_CLIMATES = {
    "Burning World": "A fierce heat blankets the Planet in its entirety. The heat usually recedes at night, but it is likely still too warm for comfort. The entire Planet is affected by extreme heat. Tests made to resist the heat are Very Hard (–30)."}
PLANET_HABITABILITY = {
    "Inhospitable": "There is no life or water to be found on this Planet."
}

SYSTEM_FEATURES = {
    "Bountiful": "The system is rich in rare minerals and valuable resources. Asteroid belts and planets have increased chances of hosting exotic materials. Colonization and mining efforts are highly profitable.",
    "Gravity Tides": "Wild gravitational currents churn the system unpredictably. Starships face hazardous piloting conditions and increased orbital dangers. Interplanetary travel can sometimes be faster using these hidden gravity streams.",
    "Haven": "The system provides safe worlds ideal for colonization. Many planets are more habitable than usual, fostering rapid settlement. It’s a prime location for establishing strongholds or colonies.",
    "Ill-Omened": "A dark reputation clings to the system, sowing fear among crews. Explorers suffer morale penalties and face increased difficulty with Fear tests. Legends of cursed worlds and ancient terrors abound.",
    "Pirate Den": "The system teems with pirate vessels and outlaw havens. Voidships risk ambush at every turn, and combat is almost inevitable. Raiders may sometimes be willing to trade under flag of truce.",
    "Ruined Empire": "Ruins of ancient civilizations litter the system. Explorers can uncover valuable archeotech, relics, or hidden dangers. Traces of lost knowledge offer rare rewards but serious risks.",
    "Starfarers": "An active voidfaring civilization lives among the stars here. Human or xenos colonies exist on many worlds or stations. Interaction may lead to alliances, trade, or devastating conflict.",
    "Stellar Anomaly": "A massive, mysterious celestial object warps the region’s space. Navigation is treacherous and bizarre phenomena are common. It can act as a landmark for astromantic charts and warp routes.",
    "Warp Stasis": "The system is partially frozen in the warp, time and space behaving oddly. Warp travel takes twice as long to reach or leave. Psychic powers are dampened, hindering astropaths and psykers.",
    "Warp Turbulence": "Warp storms buffet the system, making navigation hazardous. Warp travel and psychic abilities become much riskier. Phenomena like warp rifts or storms may appear suddenly."
}
SYSTEM_ELEMENTS = {
    "Asteroid Belt": "A wide ring of debris formed from shattered planets. Passing through requires careful navigation or lengthy detours. Often hides mineral riches and can complicate system travel.",
    "Asteroid Cluster": "Dense clumps of asteroids, remnants of shattered planets or moons. Pirates use them for ambushes and salvage opportunities abound. Navigation hazards are common.",
    "Derelict Station": "Ruins of ancient orbital stations or abandoned outposts. They may hold valuable technology, archeotech, or hostile threats. Sometimes treated like derelict vessels during boarding actions.",
    "Dust Cloud": "Massive clouds of cosmic dust and gas, sometimes remnants of solar events. They obscure auger readings and offer concealment for ships. Often treated mechanically like nebulae.",
    "Gas Giant": "Enormous planets primarily composed of gas, often surrounded by moons. These moons can offer significant exploration or resource opportunities. Gas Giants themselves are not directly habitable.",
    "Gravity Riptide": "Dangerous, invisible gravitational anomalies. They are extremely difficult to detect until ships are almost caught. Mapping them is essential for safe navigation within a system.",
    "Planet": "A world of rock, gas, or ice orbiting a star. Further details like biosphere, atmosphere, and resources are determined during Planet Creation. These are often prime targets for colonization or exploitation.",
    "Radiation Bursts": "Zones plagued by high radiation from stellar activity. Halves auger detection bonuses and damages unshielded ships. Rare but dangerous surges can occur with little warning.",
    "Solar Flares": "Frequent eruptions from a volatile star impacting nearby zones. Ships must test daily for severe damage unless sheltered. Multiple Solar Flares increase the likelihood of daily hazards.",
    "Starship Graveyard": "Wreckage fields from ancient battles or expeditions. Hidden treasures and salvage opportunities abound amidst the drifting hulks. Many derelicts are too damaged for easy recovery."
}
SYSTEM_ZONES_ALLOWED = {
    "Inner Cauldron": [
        "No Feature", "Asteroid Cluster", "Dust Cloud", "Gas Giant",
        "Gravity Riptide", "Planet", "Radiation Bursts", "Solar Flares"
    ],
    "Primary Biosphere": [
        "No Feature", "Asteroid Belt", "Asteroid Cluster", "Derelict Station", "Dust Cloud",
        "Gravity Riptide", "Planet", "Starship Graveyard"
    ],
    "Outer Reaches": [
        "No Feature","Asteroid Belt", "Asteroid Cluster", "Derelict Station",
        "Dust Cloud", "Gas Giant", "Gravity Riptide", "Planet", "Starship Graveyard"
    ]
}
SYSTEM_ZONES_WEIGHTS = {
    "Inner Cauldron": [20, 9, 12, 4, 11, 20, 12, 12],
    "Primary Biosphere": [20, 10, 11, 6, 11, 6, 29, 7],
    "Outer Reaches": [20, 9, 11, 6, 9, 18, 7, 13, 7],
}