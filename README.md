# 🪐 Exoplanets Project

is based on [Kepler Project](https://www.asterank.com/kepler) from Asterank📚 

This project used the open-source Python framework Dash created by plotly. [Read the documentation here](https://dash.plotly.com/introduction).

<br>

## 🚀 Get Started Quickly with PIP

	pip install dash                          # The core dash backend
	pip install dash-renderer                 # The dash front-end
	pip install dash-html-components          # HTML components
	pip install dash-core-components          # Supercharged components
	pip install plotly                        # Plotly graphing library
	pip install pandas                        # Data manipulation
	pip install dash-bootstrap-components     # Dash bootstrap components
	pip install numpy                         # Scientific computing in Python
	pip install dash-iconify                  # Display icons

[Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/) is a library of Bootstrap components for Plotly Dash, that makes it easier to build consistently styled apps. 

<br>

## 📃 Description:

First, we filter all existing planets by the "PER" column, which is responsible for the direction of rotation of the planet along the axis. Values greater than zero are responsible for planets spinning clockwise.

<br>

### Planet Temperature ~ Distance to the Star Chart 🌡

The graph shows the dependence of the temperature of the planet and its distance from the star. For clarity, the planets were divided by size. We call planets up to 80% of the size of a star **small**. Whose size is in the range of 80 - 120% of the size of the star were called **similar**. All other planets are **bigger**.

<br>

### Position on the Celestial Sphere Chart 📊

The graph represents the coordinates of objects on the celestial sphere. Every object has gravity and temperature values. Based on the input data, the graph displays planets with statuses:
- **extreme** - planets with unsuitable conditions for life
- **challenging** - planets with difficult conditions for life
- **promissing** - planets with suitable conditions for life

<br>

### Relative Distance (AU/Sol radii) Chart ☀️

The graph shows the relative distance from the planet to the star. Also, for a better understanding, the indicator of the planet Earth is shown. All planets are divided into categories according to the conditions of life on the planet:
- **extreme** - planets with unsuitable conditions for life
- **challenging** - planets with difficult conditions for life
- **promissing** - planets with suitable conditions for life

<br>

### Star Mass ~ Star Temperature Chart ⭐️

The graph depicts the relationship between the mass of a star and its temperature. For a more visual representation of the data, the planets are divided according to the complexity of living conditions:
- **extreme** - planets with unsuitable conditions for life
- **challenging** - planets with difficult conditions for life
- **promissing** - planets with suitable conditions for life

<hr>

All used data for this project are in Data Tab.
