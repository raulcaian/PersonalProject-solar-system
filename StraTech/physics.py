import math

G = 6.67430e-11
AU_IN_KM = 149_597_870.7
SECONDS_PER_DAY = 86400


def get_radius_m(planet):
    return (planet.diameter_km / 2) * 1000


def get_radius_km(planet):
    return planet.diameter_km / 2


def escape_velocity(planet):
    radius_m = get_radius_m(planet)
    return math.sqrt((2 * G * planet.mass_kg) / radius_m)


def time_to_reach_velocity(target_velocity_m_s, acceleration_m_s2):
    if acceleration_m_s2 <= 0:
        raise ValueError("Acceleration must be greater than zero.")
    return target_velocity_m_s / acceleration_m_s2


def distance_travelled(initial_velocity_m_s, time_s, acceleration_m_s2):
    return initial_velocity_m_s * time_s + (acceleration_m_s2 * time_s ** 2) / 2


def get_cruising_velocity(start_planet, destination_planet):
    start_escape_velocity = escape_velocity(start_planet)
    destination_escape_velocity = escape_velocity(destination_planet)
    return max(start_escape_velocity, destination_escape_velocity)


def get_distance_between_planets_km(start_orbit_au, destination_orbit_au):
    return abs(start_orbit_au - destination_orbit_au) * AU_IN_KM


def seconds_to_readable_time(total_seconds):
    total_seconds = int(total_seconds)

    days = total_seconds // 86400
    remainder = total_seconds % 86400

    hours = remainder // 3600
    remainder %= 3600

    minutes = remainder // 60
    seconds = remainder % 60

    return f"{days}d {hours}h {minutes}m {seconds}s"


def calculate_journey(start_planet, destination_planet, rocket, orbital_data):
    total_acceleration = rocket.get_total_acceleration()

    cruising_velocity_m_s = get_cruising_velocity(start_planet, destination_planet)

    acceleration_time_s = time_to_reach_velocity(cruising_velocity_m_s, total_acceleration)
    deceleration_time_s = acceleration_time_s

    acceleration_distance_m = distance_travelled(0, acceleration_time_s, total_acceleration)
    deceleration_distance_m = acceleration_distance_m

    acceleration_distance_km = acceleration_distance_m / 1000
    deceleration_distance_km = deceleration_distance_m / 1000

    start_orbit_au = orbital_data[start_planet.name]["orbital_radius_au"]
    destination_orbit_au = orbital_data[destination_planet.name]["orbital_radius_au"]

    center_to_center_distance_km = get_distance_between_planets_km(
        start_orbit_au,
        destination_orbit_au
    )

    start_radius_km = get_radius_km(start_planet)
    destination_radius_km = get_radius_km(destination_planet)

    cruise_distance_km = (
        center_to_center_distance_km
        - start_radius_km
        - destination_radius_km
        - acceleration_distance_km
        - deceleration_distance_km
    )

    if cruise_distance_km < 0:
        cruise_distance_km = 0

    cruising_velocity_km_s = cruising_velocity_m_s / 1000
    cruise_time_s = cruise_distance_km / cruising_velocity_km_s
    total_time_s = acceleration_time_s + cruise_time_s + deceleration_time_s

    return {
        "cruising_velocity_m_s": cruising_velocity_m_s,
        "acceleration_time_s": acceleration_time_s,
        "acceleration_distance_km": acceleration_distance_km,
        "cruise_time_s": cruise_time_s,
        "deceleration_distance_km": deceleration_distance_km,
        "deceleration_time_s": deceleration_time_s,
        "total_time_s": total_time_s,
        "total_time_readable": seconds_to_readable_time(total_time_s)
    }


def get_angular_position(elapsed_days, orbital_period_days):
    if orbital_period_days <= 0:
        raise ValueError("Orbital period must be greater than zero.")

    angle = (elapsed_days / orbital_period_days) * 360
    return angle % 360


def calculate_planet_positions(elapsed_days, orbital_data):
    positions = {}

    for planet_name, data in orbital_data.items():
        period_days = data["period_days"]
        angle_degrees = get_angular_position(elapsed_days, period_days)

        positions[planet_name] = {
            "angle_degrees": angle_degrees,
            "orbital_radius_au": data["orbital_radius_au"]
        }

    return positions


def degrees_to_radians(angle_degrees):
    return math.radians(angle_degrees)


def get_planet_position_xy(orbital_radius_au, angle_degrees):
    angle_radians = degrees_to_radians(angle_degrees)

    x = orbital_radius_au * AU_IN_KM * math.cos(angle_radians)
    y = orbital_radius_au * AU_IN_KM * math.sin(angle_radians)

    return x, y


def get_planet_positions_xy(elapsed_days, orbital_data):
    positions = {}

    for planet_name, data in orbital_data.items():
        angle_degrees = get_angular_position(elapsed_days, data["period_days"])
        x_km, y_km = get_planet_position_xy(data["orbital_radius_au"], angle_degrees)

        positions[planet_name] = {
            "angle_degrees": angle_degrees,
            "orbital_radius_au": data["orbital_radius_au"],
            "x_km": x_km,
            "y_km": y_km
        }

    return positions


def distance_between_points_km(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def point_to_segment_distance_km(px, py, x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    if dx == 0 and dy == 0:
        return distance_between_points_km(px, py, x1, y1)

    t = ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)
    t = max(0, min(1, t))

    closest_x = x1 + t * dx
    closest_y = y1 + t * dy

    return distance_between_points_km(px, py, closest_x, closest_y)


def line_hits_any_planet(start_planet, destination_planet, planets, positions_xy):
    start_x = positions_xy[start_planet.name]["x_km"]
    start_y = positions_xy[start_planet.name]["y_km"]
    destination_x = positions_xy[destination_planet.name]["x_km"]
    destination_y = positions_xy[destination_planet.name]["y_km"]

    for planet in planets:
        if planet.name == start_planet.name or planet.name == destination_planet.name:
            continue

        if planet.name not in positions_xy:
            continue

        px = positions_xy[planet.name]["x_km"]
        py = positions_xy[planet.name]["y_km"]
        planet_radius_km = get_radius_km(planet)

        distance_to_path = point_to_segment_distance_km(
            px, py,
            start_x, start_y,
            destination_x, destination_y
        )

        if distance_to_path <= planet_radius_km:
            return True, planet.name

    return False, None


def calculate_actual_center_distance_km(start_planet, destination_planet, positions_xy):
    start_x = positions_xy[start_planet.name]["x_km"]
    start_y = positions_xy[start_planet.name]["y_km"]
    destination_x = positions_xy[destination_planet.name]["x_km"]
    destination_y = positions_xy[destination_planet.name]["y_km"]

    return distance_between_points_km(start_x, start_y, destination_x, destination_y)


def calculate_journey_with_actual_positions(start_planet, destination_planet, rocket, positions_xy):
    total_acceleration = rocket.get_total_acceleration()

    cruising_velocity_m_s = get_cruising_velocity(start_planet, destination_planet)

    acceleration_time_s = time_to_reach_velocity(cruising_velocity_m_s, total_acceleration)
    deceleration_time_s = acceleration_time_s

    acceleration_distance_m = distance_travelled(0, acceleration_time_s, total_acceleration)
    deceleration_distance_m = acceleration_distance_m

    acceleration_distance_km = acceleration_distance_m / 1000
    deceleration_distance_km = acceleration_distance_m / 1000

    center_to_center_distance_km = calculate_actual_center_distance_km(
        start_planet,
        destination_planet,
        positions_xy
    )

    start_radius_km = get_radius_km(start_planet)
    destination_radius_km = get_radius_km(destination_planet)

    cruise_distance_km = (
        center_to_center_distance_km
        - start_radius_km
        - destination_radius_km
        - acceleration_distance_km
        - deceleration_distance_km
    )

    if cruise_distance_km < 0:
        cruise_distance_km = 0

    cruising_velocity_km_s = cruising_velocity_m_s / 1000
    cruise_time_s = cruise_distance_km / cruising_velocity_km_s
    total_time_s = acceleration_time_s + cruise_time_s + deceleration_time_s

    return {
        "center_to_center_distance_km": center_to_center_distance_km,
        "cruising_velocity_m_s": cruising_velocity_m_s,
        "acceleration_time_s": acceleration_time_s,
        "acceleration_distance_km": acceleration_distance_km,
        "cruise_time_s": cruise_time_s,
        "deceleration_distance_km": deceleration_distance_km,
        "deceleration_time_s": deceleration_time_s,
        "total_time_s": total_time_s,
        "total_time_readable": seconds_to_readable_time(total_time_s)
    }


def find_optimal_transfer_window(start_planet, destination_planet, planets, rocket, orbital_data):
    base_day = 365 * 100
    max_wait_days = 365 * 10

    best_result = None

    for wait_days in range(max_wait_days + 1):
        current_day = base_day + wait_days
        positions_xy = get_planet_positions_xy(current_day, orbital_data)

        hits_planet, _ = line_hits_any_planet(
            start_planet,
            destination_planet,
            planets,
            positions_xy
        )

        if hits_planet:
            continue

        center_to_center_distance_km = calculate_actual_center_distance_km(
            start_planet,
            destination_planet,
            positions_xy
        )

        if best_result is None or center_to_center_distance_km < best_result["center_to_center_distance_km"]:
            journey = calculate_journey_with_actual_positions(
                start_planet,
                destination_planet,
                rocket,
                positions_xy
            )

            best_result = {
                "start_day": current_day,
                "wait_days": wait_days,
                "positions_xy": positions_xy,
                "center_to_center_distance_km": center_to_center_distance_km,
                "journey": journey
            }

    return best_result



def interpolate_point(x1, y1, x2, y2, fraction):
    x = x1 + (x2 - x1) * fraction
    y = y1 + (y2 - y1) * fraction
    return x, y


def get_rocket_surface_to_surface_path(start_planet, destination_planet, launch_positions_xy):
    start_x = launch_positions_xy[start_planet.name]["x_km"]
    start_y = launch_positions_xy[start_planet.name]["y_km"]
    destination_x = launch_positions_xy[destination_planet.name]["x_km"]
    destination_y = launch_positions_xy[destination_planet.name]["y_km"]

    dx = destination_x - start_x
    dy = destination_y - start_y
    distance = math.sqrt(dx * dx + dy * dy)

    if distance == 0:
        return {
            "start_surface_x": start_x,
            "start_surface_y": start_y,
            "end_surface_x": destination_x,
            "end_surface_y": destination_y
        }

    ux = dx / distance
    uy = dy / distance

    start_radius_km = get_radius_km(start_planet)
    destination_radius_km = get_radius_km(destination_planet)

    start_surface_x = start_x + ux * start_radius_km
    start_surface_y = start_y + uy * start_radius_km

    end_surface_x = destination_x - ux * destination_radius_km
    end_surface_y = destination_y - uy * destination_radius_km

    return {
        "start_surface_x": start_surface_x,
        "start_surface_y": start_surface_y,
        "end_surface_x": end_surface_x,
        "end_surface_y": end_surface_y
    }


def will_collide_during_journey(
    start_planet,
    destination_planet,
    planets,
    orbital_data,
    launch_day,
    journey_total_time_s,
    launch_positions_xy,
    samples_per_day=4
):
    path = get_rocket_surface_to_surface_path(
        start_planet,
        destination_planet,
        launch_positions_xy
    )

    rocket_start_x = path["start_surface_x"]
    rocket_start_y = path["start_surface_y"]
    rocket_end_x = path["end_surface_x"]
    rocket_end_y = path["end_surface_y"]

    total_days = journey_total_time_s / SECONDS_PER_DAY
    total_samples = max(2, int(total_days * samples_per_day) + 1)

    for sample_index in range(total_samples + 1):
        fraction = sample_index / total_samples
        current_day = launch_day + total_days * fraction

        rocket_x, rocket_y = interpolate_point(
            rocket_start_x,
            rocket_start_y,
            rocket_end_x,
            rocket_end_y,
            fraction
        )

        moving_positions_xy = get_planet_positions_xy(current_day, orbital_data)

        for planet in planets:
            if planet.name == start_planet.name or planet.name == destination_planet.name:
                continue

            if planet.name not in moving_positions_xy:
                continue

            planet_x = moving_positions_xy[planet.name]["x_km"]
            planet_y = moving_positions_xy[planet.name]["y_km"]
            planet_radius_km = get_radius_km(planet)

            distance_to_planet = distance_between_points_km(
                rocket_x, rocket_y,
                planet_x, planet_y
            )

            if distance_to_planet <= planet_radius_km:
                return True, planet.name, current_day

    return False, None, None


def find_optimal_transfer_window_stage_6(start_planet, destination_planet, planets, rocket, orbital_data):
    base_day = 365 * 100
    max_wait_days = 365 * 10

    best_result = None

    for wait_days in range(max_wait_days + 1):
        launch_day = base_day + wait_days
        launch_positions_xy = get_planet_positions_xy(launch_day, orbital_data)

        # Optional quick filter: if launch geometry already crosses a planet, skip fast
        hits_planet, _ = line_hits_any_planet(
            start_planet,
            destination_planet,
            planets,
            launch_positions_xy
        )
        if hits_planet:
            continue

        journey = calculate_journey_with_actual_positions(
            start_planet,
            destination_planet,
            rocket,
            launch_positions_xy
        )

        collides, blocking_planet, collision_day = will_collide_during_journey(
            start_planet,
            destination_planet,
            planets,
            orbital_data,
            launch_day,
            journey["total_time_s"],
            launch_positions_xy
        )

        if collides:
            continue

        center_to_center_distance_km = journey["center_to_center_distance_km"]

        if best_result is None or center_to_center_distance_km < best_result["center_to_center_distance_km"]:
            best_result = {
                "start_day": launch_day,
                "wait_days": wait_days,
                "positions_xy": launch_positions_xy,
                "center_to_center_distance_km": center_to_center_distance_km,
                "journey": journey
            }

    return best_result