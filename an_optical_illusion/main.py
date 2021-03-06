import numpy as np
import matplotlib.pyplot as plt

class Square(object):
    def __init__(
            self,
            length = 1,
            rotation = 0,
            color = 'k',
            center = (0,0),
            linewidth = 1,
        ):
        self.length = length
        self.rotation = rotation
        self.color = color
        self.center = np.array(center)
        self.linewidth = linewidth

        self.sw = np.array([-self.length/2, -self.length/2])
        self.nw = np.array([-self.length/2, self.length/2])
        self.ne = np.array([self.length/2, self.length/2])
        self.se = np.array([self.length/2, -self.length/2])
        self.edges = np.array([self.sw, self.nw, self.ne, self.se, self.sw])

        R = np.array([
            [np.cos(self.rotation), np.sin(self.rotation)],
            [-np.sin(self.rotation), np.cos(self.rotation)]
        ])
        self.edges = self.center + np.dot(self.edges, R)
    def plot(self):

        plt.plot(self.edges[:,0], self.edges[:,1], color = self.color, linewidth = self.linewidth)

class DottedCircle(object):
    def __init__(
            self,
            center = (0,0),
            radius = 1,
            ndots = 10,
            offset = 0,
        ):
        self.center = np.array(center)
        self.radius = radius
        self.ndots = ndots
        self.offset = offset

        self.angles = np.arange(
            0 + self.offset * np.pi / ndots,
            2 * np.pi + self.offset * np.pi / ndots,
            2 * np.pi / ndots
        )
        self.dots = self.center + self.radius * np.array([[np.cos(a), np.sin(a)] for a in self.angles])

    def plot(self):
        plt.scatter(self.dots[:,0], self.dots[:,1])

class DoubleCircledSquares(object):
    def __init__(self, nsquares = 10, radius = 10,  colors = ['k', 'g'], offset = 0):
        self.nsquares = nsquares
        self.radius = radius

        self.c1 = DottedCircle(radius = self.radius, ndots = self.nsquares, offset = 0)
        self.c2 = DottedCircle(radius = self.radius, ndots = self.nsquares, offset = 1)

        self.squares = []
        for i in range(self.nsquares):
            self.squares.append(Square(
                length = 2 * self.radius / self.nsquares,
                center = self.c1.dots[i],
                rotation = self.c1.angles[i] + 1.5 * np.pi / nsquares + offset,
                color = colors[0],
                linewidth = 2
            ))
            self.squares.append(Square(
                length = 2 * self.radius / self.nsquares,
                center = self.c2.dots[i],
                rotation = self.c2.angles[i] + 1.5 * np.pi / nsquares + offset,
                color = colors[1],
                linewidth = 2
            ))

    def plot(self, circle = False):
        for s in self.squares:
            s.plot()
        if circle:
            t = np.linspace(0, 2 * np.pi, 1000)
            x = np.cos(t) * self.radius
            y = np.sin(t) * self.radius
            plt.plot(x, y, linewidth = 1, color = 'b')

class Illusion(object):
    def __init__(
            self,
            ncircles = 4,
            offsets = [],
        ):

        radii = [11 + 9 * i for i in range(ncircles)]
        if not len(offsets):
            offsets = np.random.random(len(radii)) * np.pi

        self.dcs = []
        for i, r in enumerate(radii):
            self.dcs.append(DoubleCircledSquares(
                nsquares = r,
                radius = r,
                colors = ['k', 'w'],
                offset = offsets[i]
            ))

    def plot(self):
        plt.figure(figsize = [16,8])
        plt.subplot(1,2,1)
        for dc in self.dcs:
            dc.plot(circle = False)

        plt.axvspan(
            plt.gca().get_xlim()[0],
            plt.gca().get_xlim()[1],
            color = 'grey',
            alpha = 1,
            zorder = -10
        )
        plt.gca().set_aspect('equal', 'box')
        plt.xticks([])
        plt.yticks([])
        plt.box(False)


        plt.subplot(1,2,2)
        for dc in self.dcs:
            dc.plot(circle = True)

        plt.axvspan(
            plt.gca().get_xlim()[0],
            plt.gca().get_xlim()[1],
            color = 'grey',
            alpha = 1,
            zorder = -10
        )
        plt.gca().set_aspect('equal', 'box')
        plt.xticks([])
        plt.yticks([])
        plt.box(False)
        plt.show()


if__name__ == '__main__':
    f = Illusion(ncircles = 4)
    f.plot()
    plt.show()
