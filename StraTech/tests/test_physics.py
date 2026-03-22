import unittest

from models import Planet
from rocket import Rocket
from physics import (
    escape_velocity,
    time_to_reach_velocity,
    distance_travelled,
    get_angular_position,
    get_cruising_velocity,
    seconds_to_readable_time,
    calculate_journey
)


class TestPhysics(unittest.TestCase):
    def setUp(self):
        self.earth = Planet("Earth", 12800, 6 * 10**24)
        self.mars = Planet("Mars", 5800, 0.11 * (6 * 10**24))
        self.rocket = Rocket(4, 10)

        self.orbital_data = {
            "Earth": {
                "period_days": 365.0,
                "orbital_radius_au": 1.0
            },
            "Mars": {
                "period_days": 687.0,
                "orbital_radius_au": 1.52
            }
        }

    def test_escape_velocity_earth(self):
        result = escape_velocity(self.earth)
        self.assertAlmostEqual(result, 11184, delta=50)

    def test_time_to_reach_velocity(self):
        result = time_to_reach_velocity(11184, 40)
        self.assertAlmostEqual(result, 279.6, places=1)

    def test_distance_travelled(self):
        result = distance_travelled(0, 279.6, 40)
        self.assertAlmostEqual(result, 1563523.2, delta=2000)

    def test_get_angular_position_200_days_for_earth(self):
        result = get_angular_position(200, 365)
        self.assertAlmostEqual(result, 197.26, places=2)

    def test_get_angular_position_full_period(self):
        result = get_angular_position(365, 365)
        self.assertAlmostEqual(result, 0.0, places=2)

    def test_get_cruising_velocity(self):
        result = get_cruising_velocity(self.earth, self.mars)
        self.assertAlmostEqual(result, escape_velocity(self.earth), places=2)

    def test_seconds_to_readable_time(self):
        result = seconds_to_readable_time(90061)
        self.assertEqual(result, "1d 1h 1m 1s")

    def test_calculate_journey(self):
        result = calculate_journey(self.mars, self.earth, self.rocket, self.orbital_data)

        self.assertIn("cruising_velocity_m_s", result)
        self.assertIn("acceleration_time_s", result)
        self.assertIn("cruise_time_s", result)
        self.assertIn("total_time_s", result)

        self.assertGreater(result["cruising_velocity_m_s"], 0)
        self.assertGreater(result["acceleration_time_s"], 0)
        self.assertGreater(result["total_time_s"], 0)


if __name__ == "__main__":
    unittest.main()