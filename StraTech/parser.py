import re
from models import Planet
from rocket import Rocket

EARTH_MASS_KG = 6 * 10**24


def parse_mass(mass_text):
    mass_text = mass_text.strip()

    if "Earths" in mass_text:
        value = mass_text.replace("Earths", "").strip()
        return float(value) * EARTH_MASS_KG

    if "kg" in mass_text:
        value = mass_text.replace("kg", "").strip()

        match = re.match(r"([0-9.]+)\s*\*\s*10\^([0-9]+)", value)
        if match:
            base = float(match.group(1))
            exponent = int(match.group(2))
            return base * (10 ** exponent)

        return float(value)

    raise ValueError(f"Unknown mass format: {mass_text}")


def parse_planet_line(line):
    line = line.strip()

    name_part, data_part = line.split(":", 1)
    name = name_part.strip()

    parts = data_part.split(",")

    if len(parts) != 2:
        raise ValueError(f"Invalid line format: {line}")

    diameter_text = parts[0].replace("diameter =", "").replace("km", "").strip()
    mass_text = parts[1].replace("mass =", "").strip()

    diameter_km = float(diameter_text)
    mass_kg = parse_mass(mass_text)

    return Planet(name, diameter_km, mass_kg)


def load_planets(file_path):
    planets = []

    with open(file_path, "r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            line = line.strip()

            if not line:
                continue

            try:
                planet = parse_planet_line(line)
                planets.append(planet)
            except Exception as error:
                print(f"Skipping invalid line {line_number}: {error}")

    return planets


def load_rocket(file_path):
    rocket_data = {}

    with open(file_path, "r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            line = line.strip()

            if not line:
                continue

            if "=" not in line:
                print(f"Skipping invalid rocket line {line_number}: {line}")
                continue

            key, value = line.split("=", 1)

            normalized_key = key.strip().lower().replace(" ", "_")
            rocket_data[normalized_key] = value.strip()

    if "engine_count" not in rocket_data:
        raise ValueError(
            "Missing 'engine_count' in Rocket_Data.txt. "
            "Expected format: engine_count = 4"
        )

    if "acceleration_per_engine_m_s2" not in rocket_data:
        raise ValueError(
            "Missing 'acceleration_per_engine_m_s2' in Rocket_Data.txt. "
            "Expected format: acceleration_per_engine_m_s2 = 10"
        )

    engine_count = int(rocket_data["engine_count"])
    acceleration_per_engine_m_s2 = float(rocket_data["acceleration_per_engine_m_s2"])

    return Rocket(engine_count, acceleration_per_engine_m_s2)



def load_orbital_data(file_path):
    orbital_data = {}

    with open(file_path, "r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            line = line.strip()

            if not line:
                continue

            try:
                name_part, data_part = line.split(":", 1)
                planet_name = name_part.strip()

                parts = data_part.split(",")
                if len(parts) != 2:
                    raise ValueError(f"Invalid line format: {line}")

                period_text = parts[0].replace("period =", "").replace("days", "").strip()
                orbital_radius_text = parts[1].replace("orbital radius =", "").replace("AU", "").strip()

                period_days = float(period_text)
                orbital_radius_au = float(orbital_radius_text)

                orbital_data[planet_name] = {
                    "period_days": period_days,
                    "orbital_radius_au": orbital_radius_au
                }

            except Exception as error:
                print(f"Skipping invalid orbital line {line_number}: {error}")

    return orbital_data