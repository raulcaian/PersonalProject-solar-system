from parser import load_planets, load_rocket, load_orbital_data
from physics import (
    escape_velocity,
    time_to_reach_velocity,
    distance_travelled,
    calculate_journey,
    calculate_planet_positions,
    find_optimal_transfer_window,
    find_optimal_transfer_window_stage_6
)


def find_planet_by_name(planets, name):
    for planet in planets:
        if planet.name.lower() == name.lower():
            return planet
    return None


def run_stage_1(planets):
    print("\nStage 1 - Escape velocity")
    print(f"{'Planet':<10} {'Escape Velocity (m/s)':>25}")
    print("-" * 40)

    for planet in planets:
        velocity = escape_velocity(planet)
        print(f"{planet.name:<10} {velocity:>25.2f}")


def run_stage_2(planets, rocket):
    print("\nStage 2 - Time and distance to escape velocity")
    print(
        f"{'Planet':<10}"
        f"{'Escape Velocity (m/s)':>25}"
        f"{'Time to Escape (s)':>22}"
        f"{'Distance Travelled (km)':>28}"
    )
    print("-" * 85)

    total_acceleration = rocket.get_total_acceleration()

    for planet in planets:
        escape_v = escape_velocity(planet)
        time_s = time_to_reach_velocity(escape_v, total_acceleration)
        distance_m = distance_travelled(0, time_s, total_acceleration)

        print(
            f"{planet.name:<10}"
            f"{escape_v:>25.2f}"
            f"{time_s:>22.2f}"
            f"{distance_m / 1000:>28.2f}"
        )


def run_stage_3(planets, rocket, orbital_data):
    print("\nStage 3 - Travel between two planets")
    print("Available planets:")
    for planet in planets:
        print("-", planet.name)

    start_name = input("Enter start planet: ").strip()
    destination_name = input("Enter destination planet: ").strip()

    start_planet = find_planet_by_name(planets, start_name)
    destination_planet = find_planet_by_name(planets, destination_name)

    if start_planet is None:
        print(f"Start planet '{start_name}' not found.")
        return

    if destination_planet is None:
        print(f"Destination planet '{destination_name}' not found.")
        return

    if start_planet.name.lower() == destination_planet.name.lower():
        print("Start planet and destination planet must be different.")
        return

    if start_planet.name not in orbital_data:
        print(f"Missing orbital data for {start_planet.name}.")
        return

    if destination_planet.name not in orbital_data:
        print(f"Missing orbital data for {destination_planet.name}.")
        return

    journey = calculate_journey(start_planet, destination_planet, rocket, orbital_data)

    print("\nJourney details:")
    print(f"Route: {start_planet.name} -> {destination_planet.name}")
    print(f"Cruising velocity: {journey['cruising_velocity_m_s']:.2f} m/s")
    print(f"Acceleration time: {journey['acceleration_time_s']:.2f} s")
    print(
        f"Distance from {start_planet.name} surface at cruise start: "
        f"{journey['acceleration_distance_km']:.2f} km"
    )
    print(f"Cruise time: {journey['cruise_time_s']:.2f} s")
    print(
        f"Distance from {destination_planet.name} surface to start deceleration: "
        f"{journey['deceleration_distance_km']:.2f} km"
    )
    print(f"Deceleration time: {journey['deceleration_time_s']:.2f} s")
    print(f"Total travel time: {journey['total_time_s']:.2f} s")
    print(f"Readable total time: {journey['total_time_readable']}")


def run_stage_4(orbital_data):
    print("\nStage 4 - Planetary angular positions")
    user_input = input("Enter elapsed time in days: ").strip()

    try:
        elapsed_days = float(user_input)
    except ValueError:
        print("Invalid input. Please enter a numeric value.")
        return

    if elapsed_days < 0:
        print("Elapsed time cannot be negative.")
        return

    positions = calculate_planet_positions(elapsed_days, orbital_data)

    print(f"\nPlanetary angular positions after {elapsed_days:.2f} days:")
    print(f"{'Planet':<10}{'Angle (degrees)':>20}{'Orbital Radius (AU)':>22}")
    print("-" * 52)

    for planet_name, data in positions.items():
        print(
            f"{planet_name:<10}"
            f"{data['angle_degrees']:>20.2f}"
            f"{data['orbital_radius_au']:>22.2f}"
        )


def run_stage_5(planets, rocket, orbital_data):
    print("\nStage 5 - First optimal transfer window")
    print("Available planets:")
    for planet in planets:
        print("-", planet.name)

    start_name = input("Enter start planet: ").strip()
    destination_name = input("Enter destination planet: ").strip()

    start_planet = find_planet_by_name(planets, start_name)
    destination_planet = find_planet_by_name(planets, destination_name)

    if start_planet is None:
        print(f"Start planet '{start_name}' not found.")
        return

    if destination_planet is None:
        print(f"Destination planet '{destination_name}' not found.")
        return

    if start_planet.name.lower() == destination_planet.name.lower():
        print("Start planet and destination planet must be different.")
        return

    if start_planet.name not in orbital_data:
        print(f"Missing orbital data for {start_planet.name}.")
        return

    if destination_planet.name not in orbital_data:
        print(f"Missing orbital data for {destination_planet.name}.")
        return

    result = find_optimal_transfer_window(
        start_planet,
        destination_planet,
        planets,
        rocket,
        orbital_data
    )

    if result is None:
        print("No suitable transfer window found within 10 years.")
        return

    journey = result["journey"]
    positions_xy = result["positions_xy"]

    print("\nOptimal transfer window found:")
    print(f"Route: {start_planet.name} -> {destination_planet.name}")
    print(f"Start of transfer window: 100 years + {result['wait_days']} days")
    print(f"Simulation day: {result['start_day']}")
    print(f"Center-to-center distance: {journey['center_to_center_distance_km']:.2f} km")
    print(f"Cruising velocity: {journey['cruising_velocity_m_s']:.2f} m/s")
    print(f"Acceleration time: {journey['acceleration_time_s']:.2f} s")
    print(
        f"Distance from {start_planet.name} surface at cruise start: "
        f"{journey['acceleration_distance_km']:.2f} km"
    )
    print(f"Cruise time: {journey['cruise_time_s']:.2f} s")
    print(
        f"Distance from {destination_planet.name} surface to start deceleration: "
        f"{journey['deceleration_distance_km']:.2f} km"
    )
    print(f"Deceleration time: {journey['deceleration_time_s']:.2f} s")
    print(f"Total travel time: {journey['total_time_s']:.2f} s")
    print(f"Readable total time: {journey['total_time_readable']}")

    print("\nPlanetary positions at transfer window:")
    print(f"{'Planet':<10}{'Angle (deg)':>15}{'X (km)':>18}{'Y (km)':>18}")
    print("-" * 61)

    for planet_name, data in positions_xy.items():
        print(
            f"{planet_name:<10}"
            f"{data['angle_degrees']:>15.2f}"
            f"{data['x_km']:>18.2f}"
            f"{data['y_km']:>18.2f}"
        )


def run_stage_6(planets, rocket, orbital_data):
    print("\nStage 6 - Optimal transfer window with moving planets")
    print("Available planets:")
    for planet in planets:
        print("-", planet.name)

    start_name = input("Enter start planet: ").strip()
    destination_name = input("Enter destination planet: ").strip()

    start_planet = find_planet_by_name(planets, start_name)
    destination_planet = find_planet_by_name(planets, destination_name)

    if start_planet is None:
        print(f"Start planet '{start_name}' not found.")
        return

    if destination_planet is None:
        print(f"Destination planet '{destination_name}' not found.")
        return

    if start_planet.name.lower() == destination_planet.name.lower():
        print("Start planet and destination planet must be different.")
        return

    if start_planet.name not in orbital_data:
        print(f"Missing orbital data for {start_planet.name}.")
        return

    if destination_planet.name not in orbital_data:
        print(f"Missing orbital data for {destination_planet.name}.")
        return

    result = find_optimal_transfer_window_stage_6(
        start_planet,
        destination_planet,
        planets,
        rocket,
        orbital_data
    )

    if result is None:
        print("No suitable transfer window found within 10 years.")
        return

    journey = result["journey"]
    positions_xy = result["positions_xy"]

    print("\nOptimal transfer window found:")
    print(f"Route: {start_planet.name} -> {destination_planet.name}")
    print(f"Start of transfer window: 100 years + {result['wait_days']} days")
    print(f"Simulation day: {result['start_day']}")
    print(f"Center-to-center distance: {journey['center_to_center_distance_km']:.2f} km")
    print(f"Cruising velocity: {journey['cruising_velocity_m_s']:.2f} m/s")
    print(f"Acceleration time: {journey['acceleration_time_s']:.2f} s")
    print(
        f"Distance from {start_planet.name} surface at cruise start: "
        f"{journey['acceleration_distance_km']:.2f} km"
    )
    print(f"Cruise time: {journey['cruise_time_s']:.2f} s")
    print(
        f"Distance from {destination_planet.name} surface to start deceleration: "
        f"{journey['deceleration_distance_km']:.2f} km"
    )
    print(f"Deceleration time: {journey['deceleration_time_s']:.2f} s")
    print(f"Total travel time: {journey['total_time_s']:.2f} s")
    print(f"Readable total time: {journey['total_time_readable']}")

    print("\nPlanetary positions at launch window:")
    print(f"{'Planet':<10}{'Angle (deg)':>15}{'X (km)':>18}{'Y (km)':>18}")
    print("-" * 61)

    for planet_name, data in positions_xy.items():
        print(
            f"{planet_name:<10}"
            f"{data['angle_degrees']:>15.2f}"
            f"{data['x_km']:>18.2f}"
            f"{data['y_km']:>18.2f}"
        )


def main():
    planets = load_planets("data/Planetary_Data.txt")
    rocket = load_rocket("data/Rocket_Data.txt")
    orbital_data = load_orbital_data("data/Solar_System_Data.txt")

    print("Choose a stage:")
    print("1. Stage 1 - Escape velocity")
    print("2. Stage 2 - Time and distance to escape velocity")
    print("3. Stage 3 - Travel between two planets")
    print("4. Stage 4 - Planetary angular positions")
    print("5. Stage 5 - First optimal transfer window")
    print("6. Stage 6 - Optimal transfer window with moving planets")

    choice = input("Enter your choice (1/2/3/4/5/6): ").strip()

    if choice == "1":
        run_stage_1(planets)
    elif choice == "2":
        run_stage_2(planets, rocket)
    elif choice == "3":
        run_stage_3(planets, rocket, orbital_data)
    elif choice == "4":
        run_stage_4(orbital_data)
    elif choice == "5":
        run_stage_5(planets, rocket, orbital_data)
    elif choice == "6":
        run_stage_6(planets, rocket, orbital_data)
    else:
        print("Invalid choice. Please enter 1, 2, 3, 4, 5, or 6.")


if __name__ == "__main__":
    main()