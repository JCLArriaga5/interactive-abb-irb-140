from .utils import *
import numpy as np

class abb_irb_140:
    workspace = [[-0.85, 0.85], [-0.85, 0.85], [0.0, 1.2]]

    def __deg2rad(angles):
        return [deg2rad(angles[i]) for i in range(len(angles))]

    def __movement_area(self):
        area = [[- deg2rad(180), deg2rad(180)], #theta_1
                [- deg2rad(90), deg2rad(110)],  #theta_2
                [- deg2rad(230), deg2rad(50)],  #theta_3
                [- deg2rad(200), deg2rad(200)], #theta_4
                [- deg2rad(115), deg2rad(115)], #theta_5
                [- deg2rad(400), deg2rad(400)]  #theta_6
        ]

        for i in range(len(area)):
            assert area[i][0] <= self.angles[i] <= area[i][1], 'theta_{} is not in the motion area'.format(i + 1)

    def __home_position(self):
        self.angles = abb_irb_140.__deg2rad([0.0, 90, 0.0, 0.0, 0.0, 0.0])
        self.__movement_area()

    def __transformation_matrices(self):
        self.__t01 = mdh(0.07, np.pi / 2, 0.352, self.angles[0])
        self.__t12 = mdh(0.360, 0, 0, self.angles[1])
        self.__t23 = mdh(0, np.pi / 2, 0, self.angles[2])
        self.__t34 = mdh(0, - np.pi / 2, 0.380, self.angles[3])
        self.__t45 = mdh(0, np.pi / 2, 0, self.angles[4])
        self.__t56 = mdh(0, 0, 0.065, self.angles[5])

    def __go_home(self):
        self.__home_position()

    def set_angles(self, angles):
        self.angles = abb_irb_140.__deg2rad(angles)
        self.__movement_area()

    def plot_robot(self, ax, home=False, *args, **kwargs):
        if home:
            self.__home_position()

        self.__transformation_matrices()

        ax.set_xlim(abb_irb_140.workspace[0])
        ax.set_ylim(abb_irb_140.workspace[1])
        ax.set_zlim(abb_irb_140.workspace[2])

        self.__t02 = np.dot(self.__t01, self.__t12)
        self.__t03 = np.dot(self.__t02, self.__t23)
        self.__t04 = np.dot(self.__t03, self.__t34)
        self.__t05 = np.dot(self.__t04, self.__t45)
        self.__t06 = np.dot(self.__t05, self.__t56)

        link_1 = np.array([self.__t01[:3, 3:][i][0] for i in range(3)])
        link_2 = np.array([self.__t02[:3, 3:][i][0] for i in range(3)])
        link_3 = np.array([self.__t05[:3, 3:][i][0] for i in range(3)])
        link_4 = np.array([self.__t06[:3, 3:][i][0] for i in range(3)])

        plot_syscord(ax, [0.0, 0.0, 0.0], np.eye(4) * 0.1)
        plot_syscord(ax, [self.__t01[:3, 3:][i][0] for i in range(3)], self.__t01[:3, :3] * 0.1)
        plot_syscord(ax, [self.__t02[:3, 3:][i][0] for i in range(3)], self.__t02[:3, :3] * 0.1)
        plot_syscord(ax, [self.__t03[:3, 3:][i][0] for i in range(3)], self.__t03[:3, :3] * 0.1)
        plot_syscord(ax, [self.__t04[:3, 3:][i][0] for i in range(3)], self.__t04[:3, :3] * 0.1)
        plot_syscord(ax, [self.__t05[:3, 3:][i][0] for i in range(3)], self.__t05[:3, :3] * 0.1)
        plot_syscord(ax, [self.__t06[:3, 3:][i][0] for i in range(3)], self.__t06[:3, :3] * 0.1)

        color = '#FF6600'
        plot_arm(ax, [0.0, 0.0, 0.0], link_1, color, linewidth=2.5)
        plot_arm(ax, link_1, link_2 - link_1, color, linewidth=2.5)
        plot_arm(ax, link_2, link_3 - link_2, color, linewidth=2.5)
        plot_arm(ax, link_3, link_4 - link_3, color, linewidth=2.5)

        ax.plot([0.0, link_4[0], link_4[0]],
                [0.0, link_4[1], link_4[1]],
                [0.0, 0.0, link_4[2]], '--k', alpha=0.5)

        plt.show()
