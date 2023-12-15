import random
import numpy as np

class Confetti:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.speed = random.randint(2, 5)
        self.angle = random.uniform(0, 2 * np.pi)

    def move(self):
        self.x += self.speed * np.cos(self.angle)
        self.y += self.speed * np.sin(self.angle)