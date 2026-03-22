import os
import tempfile
import unittest

from parser import parse_mass, parse_planet_line, load_rocket, load_orbital_data


class TestParser(unittest.TestCase):
    def test_parse_mass_earths(self):
        result = parse_mass("0.11 Earths")
        expected = 0.11 * (6 * 10**24)
        self.assertEqual(result, expected)

    def test_parse_mass_kg_scientific_format(self):
        result = parse_mass("6 * 10^24 kg")
        expected = 6 * 10**24
        self.assertEqual(result, expected)

    def test_parse_planet_line(self):
        line = "Mars: diameter = 5800 km, mass = 0.11 Earths"
        planet = parse_planet_line(line)

        self.assertEqual(planet.name, "Mars")
        self.assertEqual(planet.diameter_km, 5800)
        self.assertEqual(planet.mass_kg, 0.11 * (6 * 10**24))

    def test_load_rocket(self):
        rocket_content = (
            "engine_count = 4\n"
            "acceleration_per_engine_m_s2 = 10\n"
        )

        with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as temp_file:
            temp_file.write(rocket_content)
            temp_path = temp_file.name

        try:
            rocket = load_rocket(temp_path)
            self.assertEqual(rocket.engine_count, 4)
            self.assertEqual(rocket.acceleration_per_engine_m_s2, 10.0)
            self.assertEqual(rocket.get_total_acceleration(), 40.0)
        finally:
            os.remove(temp_path)

    def test_load_orbital_data(self):
        orbital_content = (
            "Earth: period = 365 days, orbital radius = 1 AU\n"
            "Mars: period = 687 days, orbital radius = 1.52 AU\n"
        )

        with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as temp_file:
            temp_file.write(orbital_content)
            temp_path = temp_file.name

        try:
            orbital_data = load_orbital_data(temp_path)

            self.assertIn("Earth", orbital_data)
            self.assertIn("Mars", orbital_data)

            self.assertEqual(orbital_data["Earth"]["period_days"], 365.0)
            self.assertEqual(orbital_data["Earth"]["orbital_radius_au"], 1.0)

            self.assertEqual(orbital_data["Mars"]["period_days"], 687.0)
            self.assertEqual(orbital_data["Mars"]["orbital_radius_au"], 1.52)
        finally:
            os.remove(temp_path)


if __name__ == "__main__":
    unittest.main()