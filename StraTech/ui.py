import tkinter as tk
from tkinter import ttk, messagebox

from parser import load_planets, load_rocket, load_orbital_data
from physics import (
    escape_velocity,
    time_to_reach_velocity,
    distance_travelled,
    calculate_journey,
    calculate_planet_positions,
    get_planet_positions_xy,
    find_optimal_transfer_window,
    find_optimal_transfer_window_stage_6
)


class SpaceChallengeUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Space Challenge Simulator")
        self.root.geometry("1200x750")

        self.planets = load_planets("data/Planetary_Data.txt")
        self.rocket = load_rocket("data/Rocket_Data.txt")
        self.orbital_data = load_orbital_data("data/Solar_System_Data.txt")

        self.planet_names = [planet.name for planet in self.planets]

        self.build_ui()

    def build_ui(self):
        main_frame = ttk.Frame(self.root, padding=12)
        main_frame.pack(fill="both", expand=True)

        control_frame = ttk.LabelFrame(main_frame, text="Controls", padding=10)
        control_frame.pack(side="left", fill="y", padx=(0, 10))

        output_frame = ttk.LabelFrame(main_frame, text="Simulation Output", padding=10)
        output_frame.pack(side="top", fill="both", expand=True)

        canvas_frame = ttk.LabelFrame(main_frame, text="Orbit View", padding=10)
        canvas_frame.pack(side="bottom", fill="both", expand=True)

        # Stage selector
        ttk.Label(control_frame, text="Choose Stage:").pack(anchor="w", pady=(0, 4))
        self.stage_var = tk.StringVar(value="Stage 1")
        self.stage_combo = ttk.Combobox(
            control_frame,
            textvariable=self.stage_var,
            state="readonly",
            values=[
                "Stage 1",
                "Stage 2",
                "Stage 3",
                "Stage 4",
                "Stage 5",
                "Stage 6"
            ],
            width=20
        )
        self.stage_combo.pack(fill="x", pady=(0, 10))
        self.stage_combo.bind("<<ComboboxSelected>>", self.on_stage_change)

        # Start planet
        ttk.Label(control_frame, text="Start Planet:").pack(anchor="w", pady=(0, 4))
        self.start_var = tk.StringVar(value=self.planet_names[0])
        self.start_combo = ttk.Combobox(
            control_frame,
            textvariable=self.start_var,
            state="readonly",
            values=self.planet_names,
            width=20
        )
        self.start_combo.pack(fill="x", pady=(0, 10))

        # Destination planet
        ttk.Label(control_frame, text="Destination Planet:").pack(anchor="w", pady=(0, 4))
        self.destination_var = tk.StringVar(value=self.planet_names[1] if len(self.planet_names) > 1 else self.planet_names[0])
        self.destination_combo = ttk.Combobox(
            control_frame,
            textvariable=self.destination_var,
            state="readonly",
            values=self.planet_names,
            width=20
        )
        self.destination_combo.pack(fill="x", pady=(0, 10))

        # Elapsed days
        ttk.Label(control_frame, text="Elapsed Days (Stage 4):").pack(anchor="w", pady=(0, 4))
        self.elapsed_days_var = tk.StringVar(value="200")
        self.elapsed_days_entry = ttk.Entry(control_frame, textvariable=self.elapsed_days_var, width=22)
        self.elapsed_days_entry.pack(fill="x", pady=(0, 10))

        # Run button
        self.run_button = ttk.Button(control_frame, text="Run Simulation", command=self.run_simulation)
        self.run_button.pack(fill="x", pady=(10, 10))

        # Clear button
        self.clear_button = ttk.Button(control_frame, text="Clear Output", command=self.clear_output)
        self.clear_button.pack(fill="x", pady=(0, 10))

        # Output text
        self.output_text = tk.Text(output_frame, wrap="word", font=("Courier", 11))
        self.output_text.pack(side="left", fill="both", expand=True)

        output_scroll = ttk.Scrollbar(output_frame, orient="vertical", command=self.output_text.yview)
        output_scroll.pack(side="right", fill="y")
        self.output_text.configure(yscrollcommand=output_scroll.set)

        # Canvas
        self.canvas = tk.Canvas(canvas_frame, bg="black", width=700, height=320)
        self.canvas.pack(fill="both", expand=True)

        self.on_stage_change()

    def on_stage_change(self, event=None):
        stage = self.stage_var.get()

        if stage in ["Stage 1", "Stage 2"]:
            self.start_combo.configure(state="disabled")
            self.destination_combo.configure(state="disabled")
            self.elapsed_days_entry.configure(state="disabled")
        elif stage == "Stage 4":
            self.start_combo.configure(state="disabled")
            self.destination_combo.configure(state="disabled")
            self.elapsed_days_entry.configure(state="normal")
        else:
            self.start_combo.configure(state="readonly")
            self.destination_combo.configure(state="readonly")
            self.elapsed_days_entry.configure(state="disabled")

    def clear_output(self):
        self.output_text.delete("1.0", tk.END)
        self.canvas.delete("all")

    def write_output(self, text):
        self.output_text.insert(tk.END, text + "\n")
        self.output_text.see(tk.END)

    def get_planet_by_name(self, name):
        for planet in self.planets:
            if planet.name.lower() == name.lower():
                return planet
        return None

    def run_simulation(self):
        try:
            self.clear_output()
            stage = self.stage_var.get()

            if stage == "Stage 1":
                self.run_stage_1()
            elif stage == "Stage 2":
                self.run_stage_2()
            elif stage == "Stage 3":
                self.run_stage_3()
            elif stage == "Stage 4":
                self.run_stage_4()
            elif stage == "Stage 5":
                self.run_stage_5()
            elif stage == "Stage 6":
                self.run_stage_6()
            else:
                messagebox.showerror("Error", "Invalid stage selected.")

        except Exception as error:
            messagebox.showerror("Error", str(error))

    def validate_route_selection(self):
        start_name = self.start_var.get().strip()
        destination_name = self.destination_var.get().strip()

        start_planet = self.get_planet_by_name(start_name)
        destination_planet = self.get_planet_by_name(destination_name)

        if start_planet is None:
            raise ValueError(f"Start planet '{start_name}' not found.")

        if destination_planet is None:
            raise ValueError(f"Destination planet '{destination_name}' not found.")

        if start_planet.name.lower() == destination_planet.name.lower():
            raise ValueError("Start planet and destination planet must be different.")

        if start_planet.name not in self.orbital_data:
            raise ValueError(f"Missing orbital data for {start_planet.name}.")

        if destination_planet.name not in self.orbital_data:
            raise ValueError(f"Missing orbital data for {destination_planet.name}.")

        return start_planet, destination_planet

    def run_stage_1(self):
        self.write_output("Stage 1 - Escape velocity")
        self.write_output(f"{'Planet':<10} {'Escape Velocity (m/s)':>25}")
        self.write_output("-" * 40)

        for planet in self.planets:
            velocity = escape_velocity(planet)
            self.write_output(f"{planet.name:<10} {velocity:>25.2f}")

    def run_stage_2(self):
        self.write_output("Stage 2 - Time and distance to escape velocity")
        self.write_output(
            f"{'Planet':<10}"
            f"{'Escape Velocity (m/s)':>25}"
            f"{'Time to Escape (s)':>22}"
            f"{'Distance Travelled (km)':>28}"
        )
        self.write_output("-" * 85)

        total_acceleration = self.rocket.get_total_acceleration()

        for planet in self.planets:
            escape_v = escape_velocity(planet)
            time_s = time_to_reach_velocity(escape_v, total_acceleration)
            distance_m = distance_travelled(0, time_s, total_acceleration)

            self.write_output(
                f"{planet.name:<10}"
                f"{escape_v:>25.2f}"
                f"{time_s:>22.2f}"
                f"{distance_m / 1000:>28.2f}"
            )

    def run_stage_3(self):
        start_planet, destination_planet = self.validate_route_selection()
        journey = calculate_journey(start_planet, destination_planet, self.rocket, self.orbital_data)

        self.write_output("Stage 3 - Travel between two planets")
        self.write_output(f"Route: {start_planet.name} -> {destination_planet.name}")
        self.write_output(f"Cruising velocity: {journey['cruising_velocity_m_s']:.2f} m/s")
        self.write_output(f"Acceleration time: {journey['acceleration_time_s']:.2f} s")
        self.write_output(
            f"Distance from {start_planet.name} surface at cruise start: "
            f"{journey['acceleration_distance_km']:.2f} km"
        )
        self.write_output(f"Cruise time: {journey['cruise_time_s']:.2f} s")
        self.write_output(
            f"Distance from {destination_planet.name} surface to start deceleration: "
            f"{journey['deceleration_distance_km']:.2f} km"
        )
        self.write_output(f"Deceleration time: {journey['deceleration_time_s']:.2f} s")
        self.write_output(f"Total travel time: {journey['total_time_s']:.2f} s")
        self.write_output(f"Readable total time: {journey['total_time_readable']}")

    def run_stage_4(self):
        elapsed_days_text = self.elapsed_days_var.get().strip()

        try:
            elapsed_days = float(elapsed_days_text)
        except ValueError:
            raise ValueError("Elapsed days must be a numeric value.")

        if elapsed_days < 0:
            raise ValueError("Elapsed days cannot be negative.")

        positions = calculate_planet_positions(elapsed_days, self.orbital_data)

        self.write_output(f"Stage 4 - Planetary angular positions after {elapsed_days:.2f} days")
        self.write_output(f"{'Planet':<10}{'Angle (degrees)':>20}{'Orbital Radius (AU)':>22}")
        self.write_output("-" * 52)

        for planet_name, data in positions.items():
            self.write_output(
                f"{planet_name:<10}"
                f"{data['angle_degrees']:>20.2f}"
                f"{data['orbital_radius_au']:>22.2f}"
            )

        positions_xy = get_planet_positions_xy(elapsed_days, self.orbital_data)
        self.draw_orbit_view(positions_xy)

    def run_stage_5(self):
        start_planet, destination_planet = self.validate_route_selection()

        result = find_optimal_transfer_window(
            start_planet,
            destination_planet,
            self.planets,
            self.rocket,
            self.orbital_data
        )

        if result is None:
            self.write_output("No suitable transfer window found within 10 years.")
            return

        journey = result["journey"]
        positions_xy = result["positions_xy"]

        self.write_output("Stage 5 - First optimal transfer window")
        self.write_output(f"Route: {start_planet.name} -> {destination_planet.name}")
        self.write_output(f"Start of transfer window: 100 years + {result['wait_days']} days")
        self.write_output(f"Simulation day: {result['start_day']}")
        self.write_output(f"Center-to-center distance: {journey['center_to_center_distance_km']:.2f} km")
        self.write_output(f"Cruising velocity: {journey['cruising_velocity_m_s']:.2f} m/s")
        self.write_output(f"Acceleration time: {journey['acceleration_time_s']:.2f} s")
        self.write_output(
            f"Distance from {start_planet.name} surface at cruise start: "
            f"{journey['acceleration_distance_km']:.2f} km"
        )
        self.write_output(f"Cruise time: {journey['cruise_time_s']:.2f} s")
        self.write_output(
            f"Distance from {destination_planet.name} surface to start deceleration: "
            f"{journey['deceleration_distance_km']:.2f} km"
        )
        self.write_output(f"Deceleration time: {journey['deceleration_time_s']:.2f} s")
        self.write_output(f"Total travel time: {journey['total_time_s']:.2f} s")
        self.write_output(f"Readable total time: {journey['total_time_readable']}")

        self.draw_orbit_view(positions_xy, start_planet.name, destination_planet.name)

    def run_stage_6(self):
        start_planet, destination_planet = self.validate_route_selection()

        result = find_optimal_transfer_window_stage_6(
            start_planet,
            destination_planet,
            self.planets,
            self.rocket,
            self.orbital_data
        )

        if result is None:
            self.write_output("No suitable transfer window found within 10 years.")
            return

        journey = result["journey"]
        positions_xy = result["positions_xy"]

        self.write_output("Stage 6 - Optimal transfer window with moving planets")
        self.write_output(f"Route: {start_planet.name} -> {destination_planet.name}")
        self.write_output(f"Start of transfer window: 100 years + {result['wait_days']} days")
        self.write_output(f"Simulation day: {result['start_day']}")
        self.write_output(f"Center-to-center distance: {journey['center_to_center_distance_km']:.2f} km")
        self.write_output(f"Cruising velocity: {journey['cruising_velocity_m_s']:.2f} m/s")
        self.write_output(f"Acceleration time: {journey['acceleration_time_s']:.2f} s")
        self.write_output(
            f"Distance from {start_planet.name} surface at cruise start: "
            f"{journey['acceleration_distance_km']:.2f} km"
        )
        self.write_output(f"Cruise time: {journey['cruise_time_s']:.2f} s")
        self.write_output(
            f"Distance from {destination_planet.name} surface to start deceleration: "
            f"{journey['deceleration_distance_km']:.2f} km"
        )
        self.write_output(f"Deceleration time: {journey['deceleration_time_s']:.2f} s")
        self.write_output(f"Total travel time: {journey['total_time_s']:.2f} s")
        self.write_output(f"Readable total time: {journey['total_time_readable']}")

        self.draw_orbit_view(positions_xy, start_planet.name, destination_planet.name)

    def draw_orbit_view(self, positions_xy, start_planet_name=None, destination_planet_name=None):
        self.canvas.delete("all")

        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        if canvas_width < 10:
            canvas_width = 700
        if canvas_height < 10:
            canvas_height = 320

        center_x = canvas_width / 2
        center_y = canvas_height / 2

        # Draw sun
        self.canvas.create_oval(
            center_x - 8, center_y - 8,
            center_x + 8, center_y + 8,
            fill="yellow", outline="yellow"
        )

        max_orbit_au = max(data["orbital_radius_au"] for data in self.orbital_data.values() if data["orbital_radius_au"] <= 30.06)
        scale = min(canvas_width, canvas_height) * 0.38 / max_orbit_au

        visible_planets = []
        for name, data in positions_xy.items():
            if data["orbital_radius_au"] <= 30.06:
                visible_planets.append((name, data))

        # Draw orbits
        for name, data in visible_planets:
            r = data["orbital_radius_au"] * scale
            self.canvas.create_oval(
                center_x - r, center_y - r,
                center_x + r, center_y + r,
                outline="gray"
            )

        # Draw transfer line first
        if start_planet_name and destination_planet_name:
            if start_planet_name in positions_xy and destination_planet_name in positions_xy:
                sx = center_x + (positions_xy[start_planet_name]["x_km"] / 149_597_870.7) * scale
                sy = center_y + (positions_xy[start_planet_name]["y_km"] / 149_597_870.7) * scale
                dx = center_x + (positions_xy[destination_planet_name]["x_km"] / 149_597_870.7) * scale
                dy = center_y + (positions_xy[destination_planet_name]["y_km"] / 149_597_870.7) * scale

                self.canvas.create_line(sx, sy, dx, dy, fill="white", width=2)

        # Draw planets
        for name, data in visible_planets:
            x = center_x + (data["x_km"] / 149_597_870.7) * scale
            y = center_y + (data["y_km"] / 149_597_870.7) * scale

            radius = 4
            color = "lightblue"

            if name == start_planet_name:
                color = "green"
                radius = 5
            elif name == destination_planet_name:
                color = "red"
                radius = 5

            self.canvas.create_oval(
                x - radius, y - radius,
                x + radius, y + radius,
                fill=color, outline=color
            )
            self.canvas.create_text(x + 10, y - 10, text=name, fill="white", anchor="w")


def main():
    root = tk.Tk()
    app = SpaceChallengeUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()