class Planet:
    def __init__(self, name, diameter_km, mass_kg, orbit_au=None):
        self.name = name
        self.diameter_km = diameter_km
        self.mass_kg = mass_kg
        self.orbit_au = orbit_au