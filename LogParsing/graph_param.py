import matplotlib.pyplot as plt
from LogParsing.plotting_utils import plot_two_scale
from LogParsing.parsing_utils import *
import numpy as np

data_dir = "C:/Users/Elijah/Documents/Uni/GDP/Initial Flight Data/"
px_filepath = data_dir + "Pixhawk Logs/00000005.log"
ard_filepath = data_dir + "Arduino Logs/FLIGHT11.LOG"

t_times, t_data = parse_px_data(px_filepath, "AETR", 2)
v_times, v_data = parse_px_data(px_filepath, "ARSP", 0)
pitch_times, pitch_data = parse_px_data(px_filepath, "ATT", 3)
acc_times, acc_data = parse_px_data(px_filepath, "IMU", 3)
a_v_times, a_v_data = parse_ard_data(ard_filepath, 0)
lc_times, lc_data = parse_ard_data(ard_filepath, 11)
aoa_times, aoa_data = parse_ard_data(ard_filepath, 7)

aoa_data = - np.array(aoa_data) + 180
for i, a in enumerate(aoa_data):
    if a > 180:
        aoa_data[i] = a - 360

plt.plot(pitch_times, pitch_data)
plot_two_scale("Time (seconds)",
               acc_times, np.array(acc_data), "X Accel",
               lc_times, -9.81 * np.array(lc_data), "Thrust (N)")
plot_two_scale("Time (seconds)",
               pitch_times, pitch_data, "Pitch",
               aoa_times, aoa_data, "AoA", match_zero=True)
plt.show()