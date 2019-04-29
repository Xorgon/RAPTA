import matplotlib.pyplot as plt
from LogParsing.plotting_utils import plot_two_scale
from LogParsing.parsing_utils import *
import numpy as np
from scipy.integrate import cumtrapz

np.seterr("raise")

data_dir = "C:/Users/Elijah/Documents/Uni/GDP/Initial Flight Data/"
px_filepath = data_dir + "Pixhawk Logs/00000005.log"
ard_filepath = data_dir + "Arduino Logs/FLIGHT11.LOG"

t_times, t_data = parse_px_data(px_filepath, "AETR", 2)
elev_times, elev_data = parse_px_data(px_filepath, "AETR", 1)
v_times, v_data = parse_px_data(px_filepath, "ARSP", 0)
des_pitch_times, des_pitch_data = parse_px_data(px_filepath, "ATT", 2)
pitch_times, pitch_data = parse_px_data(px_filepath, "ATT", 3)
des_yaw_times, des_yaw_data = parse_px_data(px_filepath, "ATT", 4)
yaw_times, yaw_data = parse_px_data(px_filepath, "ATT", 5)
des_roll_times, des_roll_data = parse_px_data(px_filepath, "ATT", 0)
roll_times, roll_data = parse_px_data(px_filepath, "ATT", 1)
x_acc_times, x_acc_data = parse_px_data(px_filepath, "IMU", 3)
z_acc_times, z_acc_data = parse_px_data(px_filepath, "IMU", 5)
gyr_y_times, gyr_y_data = parse_px_data(px_filepath, "IMU", 1)
mode_times, mode_data = parse_px_data(px_filepath, "MODE", 1)
alt_times, alt_data = parse_ard_data(ard_filepath, 1)
a_v_times, a_v_data = parse_ard_data(ard_filepath, 0)
lc_times, lc_data = parse_ard_data(ard_filepath, 11)
aoa_times, aoa_data = parse_ard_data(ard_filepath, 7)
pida_des_times, pida_des_data = parse_px_data(px_filepath, "PIDP", 0)
pida_p_times, pida_p_data = parse_px_data(px_filepath, "PIDP", 1)
pida_i_times, pida_i_data = parse_px_data(px_filepath, "PIDP", 2)
pida_d_times, pida_d_data = parse_px_data(px_filepath, "PIDP", 3)

filt_v_times, filt_v_data = zip(*filter(lambda x: 169 < x[0] < 500, zip(v_times, v_data)))
print("Distance travelled: ", np.trapz(filt_v_data, filt_v_times))

thrust_times = lc_times
thrust_data = -9.81 * np.array(lc_data)

aoa_data = - np.array(aoa_data) + 180
for i, a in enumerate(aoa_data):
    if a > 180:
        aoa_data[i] = a - 360

rot_acc = np.gradient(gyr_y_data, gyr_y_times)

synced_rot_acc = []
synced_times = []
synced_thrust = []
synced_aoa = []
synced_x_acc = []
synced_z_acc = []
synced_pitch = []
synced_roll = []
synced_vel = []

for i, t in enumerate(thrust_times):
    rot = np.interp(t, gyr_y_times, rot_acc)
    x_acc = np.interp(t, x_acc_times, x_acc_data)
    z_acc = np.interp(t, z_acc_times, z_acc_data)
    pitch = np.interp(t, pitch_times, pitch_data)
    roll = np.interp(t, roll_times, roll_data)
    vel = np.interp(t, v_times, v_data)

    if all([rot, x_acc, z_acc, pitch, vel, roll]):
        synced_times.append(t)
        synced_thrust.append(thrust_data[i])
        synced_aoa.append(np.mean(aoa_data[np.max([0, i - 8]):np.min([i + 8, len(aoa_data)])]))  # Moving average filter
        synced_rot_acc.append(rot)
        synced_x_acc.append(x_acc)
        synced_z_acc.append(z_acc)
        synced_pitch.append(pitch)
        synced_roll.append(roll)
        synced_vel.append(vel)

synced_thrust = np.array(synced_thrust)
synced_aoa = np.radians(np.array(synced_aoa) / 1.3298)
synced_x_acc = np.array(synced_x_acc)
synced_z_acc = np.array(synced_z_acc)
synced_pitch = np.radians(np.array(synced_pitch))
synced_roll = np.radians(np.array(synced_roll))
synced_vel = np.array(synced_vel)
synced_rot_acc = np.array(synced_rot_acc)

engine_mass = 0.471
aircraft_mass = 7
acc = synced_x_acc * np.cos(synced_aoa) + (synced_z_acc - synced_rot_acc * 0.315) * np.sin(synced_aoa)
drag_data = (synced_thrust + engine_mass * (9.81 * np.sin(synced_pitch) + acc)) * np.cos(synced_aoa) \
            - aircraft_mass * acc

filt_drag_times, filt_drag = zip(*filter(lambda x: 216.5 <= x[0] <= 219, zip(synced_times, drag_data)))
print("Mean drag between 216.5s and 219s:", np.mean(filt_drag))
filt_aoa_times, filt_aoa = zip(*filter(lambda x: 216.5 <= x[0] <= 219, zip(aoa_times, aoa_data)))
print("Mean AoA between 216.5s and 219s:", np.mean(filt_aoa))
filt_v_times, filt_v_data = zip(*filter(lambda x: 216.5 <= x[0] <= 219, zip(v_times, v_data)))
print("Mean speed between 216.5s and 219s:", np.mean(filt_v_data))

pitch_rate = np.gradient(np.radians(pitch_data), pitch_times)
plt.figure(num="Angular Speed")
plt.plot(gyr_y_times, gyr_y_data, label="Gyro")
plt.plot(pitch_times, pitch_rate,
         label="Pitch")
plt.xlabel("Time (s)")
plt.ylabel("Angular speed (?)")
plt.legend()

plt.figure(num="Acceleration Check")
plt.plot(x_acc_times, cumtrapz(np.array(x_acc_data) - 0.51, x_acc_times, initial=0), label="x acc")
plt.plot(v_times, v_data, label="IAS data")
plt.xlabel("Time (s)")
plt.ylabel("Speed ($ms^{-1}$")
plt.legend()

plot_two_scale("Time (s)",
               x_acc_times, x_acc_data, "x acc",
               v_times, v_data, "speed",
               title="IAS/x acc")

plt.figure(num="Rotational acceleration")
plt.plot(synced_times, synced_z_acc, label="z_acc")
plt.plot(synced_times, synced_z_acc - synced_rot_acc * 0.315, label="adj")
plt.xlabel("Time (s)")
plt.ylabel("Rotational acceleration")
plt.legend()
plt.title("Testing")

plt.figure(num="Force components")
plt.plot(synced_times, -aircraft_mass * 9.81 * np.sin(synced_pitch - synced_aoa), label="Weight")
plt.plot(synced_times, aircraft_mass * acc, label="ma")
plt.plot(synced_times, (synced_thrust + engine_mass * (9.81 * np.sin(synced_pitch) + acc)) * np.cos(synced_aoa),
         label="Thrust")
plt.xlabel("Time (s)")
plt.ylabel("Force (N)")
plt.legend()

plt.figure(num="pitch - aoa")
plt.plot(synced_times, np.degrees(synced_pitch - synced_aoa))
plt.xlabel("Time (s)")
plt.ylabel("pitch - aoa")

plot_two_scale("Time (s)",
               pitch_times, pitch_data, "Pitch (degrees)",
               z_acc_times, np.array(z_acc_data) / 9.81, "z acc",
               title="Pitch/z acc")

fig, _, _ = plot_two_scale("Time (s)",
                           synced_times, drag_data, "Drag (N)",
                           synced_times, np.degrees(synced_aoa), "AoA (degrees)",
                           title="Drag/AoA")
for t in mode_times:
    fig.gca().axvline(t, linestyle="--", color="grey")

plt.figure(num="Thrust/Drag")
plt.plot(synced_times, synced_thrust, label="Thrust")
plt.plot(synced_times, drag_data, label="Drag")
plt.legend()
plt.xlabel("Time (s)")
plt.ylabel("Force (N)")

plt.figure(num="Altitude")
plt.plot(alt_times, alt_data)
plt.xlabel("Time (s)")
plt.ylabel("Altitude (m, QFE)")
for t in mode_times:
    plt.axvline(t, linestyle="--", color="grey")

plot_two_scale("Time (s)",
               synced_times, np.degrees(synced_aoa), "AoA (degrees)",
               alt_times, alt_data, "Altitude (m, QFE)",
               title="Altitude/AoA")

plot_two_scale("Time (s)",
               synced_times, np.degrees(synced_aoa), "AoA (degrees)",
               roll_times, roll_data, "Roll (degrees)",
               title="AoA/Roll")

plt.figure(num="Pitch/Roll")
plt.plot(pitch_times, pitch_data, label="Pitch (degrees)")
plt.plot(roll_times, roll_data, label="Roll (degrees)")
plt.xlabel("Time (s)")
plt.legend()

plt.figure(num="AoA")
plt.plot(synced_times, np.degrees(synced_aoa))
plt.plot(aoa_times, np.array(aoa_data) / 1.3298)
plt.plot(aoa_times, aoa_data)
plt.xlabel("Time (s)")
plt.ylabel("AoA (degrees)")

plt.figure(num="Speed/Drag")
plt.scatter(synced_vel, drag_data)
plt.xlabel("Speed (m/s)")
plt.ylabel("Drag (N)")

plot_two_scale("Time (seconds)",
               synced_times, acc, "Accel ($m/s^2$)",
               lc_times, -9.81 * np.array(lc_data), "Thrust (N)",
               title="Accel/Thrust")

fig, ax1, ax2 = plot_two_scale("Time (seconds)",
                               pitch_times, pitch_data, "Pitch",
                               v_times, v_data, "IAS (m/s)",
                               title="Pitch/AoA/IAS")
ax1.plot(aoa_times, aoa_data, label="AoA")
ax1.legend()

plot_two_scale("Time (seconds)",
               v_times, v_data, "IAS (m/s)",
               t_times, t_data, "Throttle (%)",
               title="IAS/Throttle")

plot_two_scale("Time (seconds)",
               v_times, v_data, "IAS (m/s)",
               pitch_times, pitch_data, "Pitch",
               title="IAS/Pitch")

plt.figure(num="roll/Des roll")
plt.plot(roll_times, roll_data, label="roll")
plt.plot(des_roll_times, des_roll_data, label="Des roll")
plt.xlabel("Time (s)")
plt.ylabel("Angle (deg)")
plt.legend()
for t in mode_times:
    plt.axvline(t, linestyle="--", color="grey")

plt.figure(num="Pitch/Des Pitch")
plt.plot(pitch_times, pitch_data, label="Pitch")
plt.plot(des_pitch_times, des_pitch_data, label="Des Pitch")
plt.xlabel("Time (s)")
plt.ylabel("Angle (deg)")
plt.legend()
for t in mode_times:
    plt.axvline(t, linestyle="--", color="grey")

plt.figure(num="yaw/Des yaw")
plt.plot(yaw_times, yaw_data, label="yaw")
plt.plot(des_yaw_times, des_yaw_data, label="Des yaw")
plt.xlabel("Time (s)")
plt.ylabel("Angle (deg)")
plt.legend()
for t in mode_times:
    plt.axvline(t, linestyle="--", color="grey")

plt.figure(num="PIDA")
plt.plot(pida_des_times, pida_des_data, label="des")
plt.plot(pida_p_times, pida_p_data, label="p")
plt.plot(pida_i_times, pida_i_data, label="i")
plt.plot(pida_d_times, pida_d_data, label="d")
plt.xlabel("Time (s)")
plt.ylabel("Value")
plt.legend()
for t in mode_times:
    plt.axvline(t, linestyle="--", color="grey")

plt.show()
