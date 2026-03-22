# Space Challenge Simulator

## Overview
This project is a Python implementation of the 2026 Software Challenge.  
It simulates different aspects of interplanetary travel across multiple stages, starting from basic escape velocity calculations and continuing with orbital positions, transfer windows, and a graphical user interface.

The application supports:
- Stage 1 – Escape velocity calculation for all planets
- Stage 2 – Time and distance required to reach escape velocity
- Stage 3 – Travel simulation between two selected planets
- Stage 4 – Planetary angular positions after a given number of days
- Stage 5 – First optimal transfer window with static planetary positions after launch
- Stage 6 – Optimal transfer window while planets continue to move during the journey
- Stage 7 – Graphical user interface built with Tkinter

---

## Project Structure

```text
StraTech/
│
├── data/
│   ├── Planetary_Data.txt
│   ├── Rocket_Data.txt
│   └── Solar_System_Data.txt
│
├── tests/
│   ├── test_parser.py
│   └── test_physics.py
│
├── models.py
├── parser.py
├── physics.py
├── rocket.py
├── main.py
├── ui.py
└── README.md
```
## Input Files

### Planetary_Data.txt

Contains the physical properties of the planets:
- diameter
- mass

Example:

- Earth: diameter = 12800 km, mass = 6 * 10^24 kg
- Mars: diameter = 5800 km, mass = 0.11 Earths


### Rocket_Data.txt

Contains the rocket configuration:

- number of engines
- acceleration per engine

Example:
- engine_count = 4
- acceleration_per_engine_m_s2 = 10

### Solar_System_Data.txt

Contains orbital information:
- orbital period
- orbital radius

Example:
- Earth: period = 365 days, orbital radius = 1 AU
- Mars: period = 687 days, orbital radius = 1.52 AU

# Features by Stage

### Stage 1 – Escape Velocity

The application computes the escape velocity for every planet in the input file using:

v = sqrt(2GM / r)

where:
- G is the gravitational constant
- M is the mass of the planet
- r is the radius of the planet in meters

The result is displayed in a clear console table.

### Stage 2 – Time and Distance to Escape Velocity

For each planet, the application calculates:
- the time required for the rocket to reach escape velocity
- the distance travelled during acceleration
- 
The rocket uses:
- 4 engines
- 10 m/s² acceleration per engine
- total acceleration = 40 m/s²


### Stage 3 – Travel Between Two Planets

The user selects:
- a start planet
- a destination planet
- 
The program calculates:
- cruising velocity
- acceleration time
- cruise time
- deceleration time
- total travel time

### Stage 4 – Planetary Angular Positions

The user enters elapsed time in days.
The application calculates the angular position of each planet based on uniform circular motion.

### Stage 5 – First Optimal Transfer Window
The application searches for the first good transfer opportunity starting at:
- t0 + 100 years
- with a maximum waiting period of 10 years 

A transfer window is considered valid when:
- the planets are as close as possible
- the straight-line path does not intersect another planet
- the solar system is treated as frozen after launch

### Stage 6 – Optimal Transfer Window With Moving Planets

This stage extends Stage 5.
The planets continue to move while the rocket is travelling, and the program checks whether a collision could happen during the journey.

### Stage 7 – Graphical User Interface

A Tkinter-based interface was added to display the simulation results in a more user-friendly way.

The GUI includes:

- stage selection
- planet selection
- elapsed-days input
- result output area
- simple orbital visualization


### How to Run the Project
Console Version

Run:
python main.py

This opens the console menu where you can choose a stage from 1 to 6.

Graphical User Interface

Run:
ui.py

### Requirements
This project uses standard Python libraries only:
- math
- re
- tkinter

No external packages are required.

Recommended Python version:
Python 3.10+

## Testing

The project includes unit tests for the core logic of the application.

The main goal of the test suite is to verify that the most important non-UI parts of the project behave correctly:
- input parsing
- physics calculations
- orbital position calculations
- basic journey simulation logic

### Test Files

The tests are organized in the `tests/` folder:

- `tests/test_parser.py`
- `tests/test_physics.py`

### What Is Tested

#### `test_parser.py`
This file contains tests for the parsing logic:
- parsing mass values expressed in Earth masses
- parsing mass values written in scientific notation
- parsing a full planet input line
- loading rocket data from a text file
- loading orbital data from a text file

These tests help ensure that the application can correctly read and interpret the input files.

#### `test_physics.py`
This file contains tests for the main physics calculations:
- escape velocity calculation
- time required to reach escape velocity
- distance travelled during acceleration
- angular position calculation
- cruising velocity selection
- readable time conversion
- basic journey calculation between two planets

These tests verify that the formulas used in the simulation produce expected and reasonable results.

### Why These Tests Were Chosen

The tests focus on the parts of the project that are most critical for correctness:
- file parsing
- mathematical calculations
- simulation output logic

The graphical user interface was not unit tested, since the most important part of the challenge is the correctness of the simulation and calculations.

### Running the Tests

To run all tests from the root project folder, use:

```bash
python -m unittest discover tests