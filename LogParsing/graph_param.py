import matplotlib.pyplot as plt
from LogParsing.plotting_utils import plot_two_scale
from LogParsing.parsing_utils import *
import numpy as np

data_dir = "C:/Users/Elijah/Documents/Uni/GDP/Initial Flight Data/"
px_filepath = data_dir + "Pixhawk Logs/00000005.log"
ard_filepath = data_dir + "Arduino Logs/FLIGHT11.LOG"

t_times, t_data = parse_px_data(px_filepath, "AETR", 1)
elev_times, elev_data = parse_px_data(px_filepath, "AETR", 1)
v_times, v_data = parse_px_data(px_filepath, "ARSP", 0)
pitch_times, pitch_data = parse_px_data(px_filepath, "ATT", 3)
roll_times, roll_data = parse_px_data(px_filepath, "ATT", 1)
x_acc_times, x_acc_data = parse_px_data(px_filepath, "IMU", 3)
z_acc_times, z_acc_data = parse_px_data(px_filepath, "IMU", 5)
mode_times, mode_data = parse_px_data(px_filepath, "MODE", 1)
alt_times, alt_data = parse_ard_data(ard_filepath, 1)
a_v_times, a_v_data = parse_ard_data(ard_filepath, 0)
lc_times, lc_data = parse_ard_data(ard_filepath, 11)
aoa_times, aoa_data = parse_ard_data(ard_filepath, 7)

thrust_times = lc_times
thrust_data = -9.81 * np.array(lc_data)

aoa_data = - np.array(aoa_data) + 180
for i, a in enumerate(aoa_data):
    if a > 180:
        aoa_data[i] = a - 360

synced_times = []
synced_thrust = []
synced_aoa = []
synced_x_acc = []
synced_z_acc = []
synced_pitch = []
synced_vel = []

for i, t in enumerate(thrust_times):
    print(100 * i / len(thrust_times))
    x_acc = np.interp(t, x_acc_times, x_acc_data)
    z_acc = np.interp(t, z_acc_times, z_acc_data)
    pitch = np.interp(t, pitch_times, pitch_data)
    vel = np.interp(t, v_times, v_data)

    if all([x_acc, z_acc, pitch, vel]):
        synced_times.append(t)
        synced_thrust.append(thrust_data[i])
        synced_aoa.append(np.mean(aoa_data[i - 8:i + 8]))  # Moving average filter
        synced_x_acc.append(x_acc)
        synced_z_acc.append(z_acc)
        synced_pitch.append(pitch)
        synced_vel.append(vel)

synced_thrust = np.array(synced_thrust)
synced_aoa = np.radians(np.array(synced_aoa) / 1.3298)
synced_x_acc = np.array(synced_x_acc)
synced_z_acc = np.array(synced_z_acc)
synced_pitch = np.radians(np.array(synced_pitch))
synced_vel = np.array(synced_vel)

engine_mass = 0.471
aircraft_mass = 7
drag_data = (synced_thrust + engine_mass * 9.81 * np.sin(synced_pitch)) * np.cos(synced_aoa) \
            - aircraft_mass * (synced_x_acc * np.cos(synced_aoa) + synced_z_acc * np.sin(synced_aoa))
# - aircraft_mass * 9.81 * np.sin(synced_pitch - synced_aoa)

fig, _, _ = plot_two_scale("Time (s)",
                           synced_times, drag_data, "Drag (N)",
                           synced_times, np.degrees(synced_aoa), "AoA (degrees)")
for t in mode_times:
    fig.gca().axvline(t, linestyle="--", color="grey")

plt.figure()
plt.plot(synced_times, synced_thrust, label="Thrust")
plt.plot(synced_times, drag_data, label="Drag")
plt.legend()
plt.xlabel("Time (s)")
plt.ylabel("Force (N)")

plt.figure()
plt.plot(alt_times, alt_data)
plt.xlabel("Time (s)")
plt.ylabel("Altitude (m, QFE)")
for t in mode_times:
    plt.axvline(t, linestyle="--", color="grey")

plot_two_scale("Time (s)",
               synced_times, np.degrees(synced_aoa), "AoA (degrees)",
               alt_times, alt_data, "Altitude (m, QFE)")

plot_two_scale("Time (s)",
               synced_times, np.degrees(synced_aoa), "AoA (degrees)",
               roll_times, roll_data, "Roll (degrees)")

plt.figure()
plt.plot(pitch_times, pitch_data, label="Pitch (degrees)")
plt.plot(roll_times, roll_data, label="Roll (degrees)")
plt.xlabel("Time (s)")
plt.legend()

plt.figure()
plt.plot(synced_times, np.degrees(synced_aoa))
plt.plot(aoa_times, np.array(aoa_data) / 1.3298)
plt.plot(aoa_times, aoa_data)
plt.xlabel("Time (s)")
plt.ylabel("AoA (degrees)")

plt.figure()
plt.scatter(synced_vel, drag_data)
plt.xlabel("Speed (m/s)")
plt.ylabel("Drag (N)")

plot_two_scale("Time (seconds)",
               x_acc_times, np.array(x_acc_data), "X Accel",
               lc_times, -9.81 * np.array(lc_data), "Thrust (N)")
fig, ax1, ax2 = plot_two_scale("Time (seconds)",
                               pitch_times, pitch_data, "Pitch",
                               v_times, v_data, "IAS (m/s)")
ax1.plot(aoa_times, aoa_data, label="AoA")
ax1.legend()
plot_two_scale("Time (seconds)",
               v_times, v_data, "IAS (m/s)",
               t_times, t_data, "Throttle (%)")
plot_two_scale("Time (seconds)",
               v_times, v_data, "IAS (m/s)",
               pitch_times, pitch_data, "Pitch")
plt.show()
