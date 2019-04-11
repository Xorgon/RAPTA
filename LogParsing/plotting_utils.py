import matplotlib.pyplot as plt


def plot_two_scale(x_label, x1, y1, y1_label, x2, y2, y2_label, match_zero=False):
    fig, ax1 = plt.subplots()

    ax1.set_xlabel(x_label)
    ax1.set_ylabel(y1_label, color="b")
    ax1.plot(x1, y1, color="b")

    ax2 = ax1.twinx()
    ax2.set_ylabel(y2_label, color="orange")
    ax2.plot(x2, y2, color="orange")
    if match_zero:
        align_yaxis(ax1, 0, ax2, 0)


def align_yaxis(ax1, v1, ax2, v2):
    """
    https://stackoverflow.com/a/10482477/5270376
    adjust ax2 ylimit so that v2 in ax2 is aligned to v1 in ax1
    """
    _, y1 = ax1.transData.transform((0, v1))
    _, y2 = ax2.transData.transform((0, v2))
    inv = ax2.transData.inverted()
    _, dy = inv.transform((0, 0)) - inv.transform((0, y1 - y2))
    miny, maxy = ax2.get_ylim()
    ax2.set_ylim(miny + dy, maxy + dy)
