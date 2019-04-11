import matplotlib.pyplot as plt
from LogParsing.parsing_utils import *
import numpy as np

px_filepath = "C:/Users/Elijah/Documents/Uni/GDP/Initial Flight Data/Pixhawk Logs/00000005.log"
ard_filepath = "C:/Users/Elijah/Documents/Uni/GDP/Initial Flight Data/Arduino Logs/FLIGHT11.LOG"

t_times, t_data = parse_px_data(px_filepath, "AETR", 2)
v_times, v_data = parse_px_data(px_filepath, "ARSP", 0)
a_v_times, a_v_data = parse_ard_data(ard_filepath, 1)
lc_times, lc_data = parse_ard_data(ard_filepath, 12)

fig, ax1 = plt.subplots()

ax1.set_xlabel("Time (seconds)")
ax1.set_ylabel("Throttle (%)", color="b")
ax1.plot(t_times, t_data, color="b")
# plt.plot(v_times, v_data)
# plt.plot(a_v_times, a_v_data)

ax2 = ax1.twinx()
ax2.set_ylabel("Thrust (kg)", color="orange")
ax2.plot(lc_times, - np.array(lc_data), color="orange")

plt.show()
