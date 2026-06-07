"""
=======================
F1 Telemetry Comparator
=======================
This code compares the telemetry data for each driver's fastest laps in a specific session.
"""

import matplotlib.pyplot as plt
import fastf1.plotting

season = int(input("Select a season (2026, 2025, ...): "))
event = input("Select an event (Spanish Grand Prix, Monaco Grand Prix, ...): ")
session_selected = input("Select a session (FP1, FP2, FP3, Q or R): ")
print("To select a driver, use his abbreviation.")
driver1 = input("Select the first driver: ")
driver2 = input("Select the second driver: ")


# This enables Matplotlib settings to plot 'timedelta' values and loads the FastF1 dark colour scheme
fastf1.plotting.setup_mpl(mpl_timedelta_support = True, color_scheme = 'fastf1')

# This loads a session and it telemetry data
session = fastf1.get_session(season, event, session_selected)
session.load()

# This selects the two laps that we are going to compare
driver1_lap = session.laps.pick_drivers(driver1).pick_fastest()
driver2_lap = session.laps.pick_drivers(driver2).pick_fastest()

# This gets the telemetry data of each lap. Also, we add a 
# "Distance" column to the telemetry dataframe

driver1_tel = driver1_lap.get_car_data().add_distance()
driver2_tel = driver2_lap.get_car_data().add_distance()

# This create the plots

driver1_color = fastf1.plotting.get_team_color(driver1_lap['Team'], session = session)
driver2_color = fastf1.plotting.get_team_color(driver2_lap['Team'], session = session)

if driver1_color == driver2_color:
    driver2_color = 'pink'

fig, (ax1, ax2, ax3, ax4) = plt.subplots(nrows = 4, ncols = 1)
ax1.plot(driver1_tel['Distance'], driver1_tel['Speed'], color = driver1_color, label = driver1)
ax1.plot(driver2_tel['Distance'], driver2_tel['Speed'], color = driver2_color, label = driver2)
#ax1.set_xlabel("Distance [m]")
ax1.set_ylabel("Speed [km/h]")
ax1.legend()

ax2.plot(driver1_tel['Distance'], driver1_tel['Throttle'], color = driver1_color, label = driver1)
ax2.plot(driver2_tel['Distance'], driver2_tel['Throttle'], color = driver2_color, label = driver2)
#ax2.set_xlabel("Distance [m]")
ax2.set_ylabel("Throttle [%]")
ax2.legend()

ax3.plot(driver1_tel['Distance'], driver1_tel['Brake'], color = driver1_color, label = driver1)
ax3.plot(driver2_tel['Distance'], driver2_tel['Brake'], color = driver2_color, label = driver2)
#ax3.set_xlabel("Distance [m]")
ax3.set_ylabel("Brake (ON/OFF)")
ax3.legend()

ax4.plot(driver1_tel['Distance'], driver1_tel['RPM'], color = driver1_color, label = driver1)
ax4.plot(driver2_tel['Distance'], driver2_tel['RPM'], color = driver2_color, label = driver2)
ax4.set_xlabel("Distance [m]")
ax4.set_ylabel("RPM")
ax4.legend()

# This incluides circuit info about the location of the corners

circuit_info = session.get_circuit_info()

# This draws lines to know where are the corners

v_min = driver1_tel['Speed'].min()
v_max = driver1_tel['Speed'].max()
ax1.vlines(x = circuit_info.corners['Distance'], ymin = v_min - 10, ymax = v_max + 10, linestyles = 'dotted', colors = 'grey')

ax2.vlines(x = circuit_info.corners['Distance'], ymin = 0, ymax = 100, linestyles = 'dotted', colors = 'grey')
ax3.vlines(x = circuit_info.corners['Distance'], ymin = 0, ymax = 1, linestyles = 'dotted', colors = 'grey')

rpm_min = driver1_tel['RPM'].min()
rpm_max = driver1_tel['RPM'].max()
ax4.vlines(x = circuit_info.corners['Distance'], ymin = rpm_min, ymax = rpm_max, linestyles = 'dotted', colors = 'grey')

#This writes corner numbers in their position

for _, corner in circuit_info.corners.iterrows():
    txt = f"{corner['Number']}{corner['Letter']}"
    ax1.text(corner['Distance'], v_min - 20, txt, va = 'center_baseline', ha = 'center', size = 'small')
    ax2.text(corner['Distance'], 0, txt, va = 'center_baseline', ha = 'center', size = 'small')
    ax3.text(corner['Distance'], 0, txt, va = 'center_baseline', ha = 'center', size = 'small')
    ax4.text(corner['Distance'], rpm_min - 20, txt, va = 'center_baseline', ha = 'center', size = 'small')

plt.suptitle(f"Fastest Lap Comparison\n"
             f"{session.event['EventName']} {session.event.year} {session_selected}")

plt.show()