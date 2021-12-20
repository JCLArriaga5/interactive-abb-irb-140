import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import *

def deg2rad(angle):
    return angle * (np.pi / 180)

def rad2deg(angle):
    return angle * (180 / np.pi)

def mdh(ai, alphai, di, thetai):
    m = np.array([
        [np.cos(thetai), - np.sin(thetai) * np.cos(alphai),
        np.sin(thetai) * np.sin(alphai), ai * np.cos(thetai)],
        [np.sin(thetai),   np.cos(thetai) * np.cos(alphai),
        - np.cos(thetai) * np.sin(alphai), ai * np.sin(thetai)],
        [0, np.sin(alphai), np.cos(alphai), di], [0, 0, 0, 1]
    ])
    return m

def plot_syscord(ax, pos, rot):
    colors = ['r', 'g', 'b']

    for i in range(len(colors)):
        r_x = rot[:, i:i + 1][0][0]
        r_y = rot[:, i:i + 1][1][0]
        r_z = rot[:, i:i + 1][2][0]
        ax.quiver(pos[0], pos[1], pos[2],
                  r_x, r_y, r_z,
                  color=colors[i])

def plot_arm(ax, p_i, p_f, *args, **kwargs):
    ax.plot([p_i[0], p_i[0] + p_f[0]],
            [p_i[1], p_i[1] + p_f[1]],
            [p_i[2], p_i[2] + p_f[2]], *args, **kwargs)
    # If the color is not specified, the np.scatter decorator will default to itself.
    if len(args) == 0:
        ax.scatter([p_i[0]], [p_i[1]], [p_i[2]])
    # Otherwise the color is used regardless of the line style. Since the line
    # style does not attribute to np.sactter.
    else:
        color = ''.join([args[0][i] for i in range(len(args[0]))
                         if args[0][i] not in list(plt.Line2D.lineStyles) + ['.']])
        ax.scatter3D(p_i[0], p_i[1], p_i[2], s=30, facecolor=color)
