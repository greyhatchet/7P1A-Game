import unittest
import pygame

class PlayerTestCase(unittest.TestCase):
    def setUp(self):
        self.player = Player()

    def test_default_size(self):
        self.assertEqual(self.image, pygame.Surface([40,60]))

    def test_default_speed(self):
        self.assertEqual([self.change_x, self.change_y], [0,0])

    def test_default_level(self):
        self.assertEqual(self.level, None)

    def test_update(self):
        x = self.rect.x
        y = self.rect.y
        x_change = self.change_x
        y_change = self.change_y
        self.update()
        self.assertEqual(self.rect.x, x + x_change)
        self.assertEqual(self.rect.y, y + y_change)

    def test_go_left(self):
        self.assertEqual(self.change_x, -6)

    def test_go_right(self):
        self.assertEqual(self.change_x, 6)

    def test_stop(self):
        self.assertEqual(self.change_x, 0)

class ShootTestCase(unittest.TestCase):

    def setUp(self):
        self.shoot = Shoot(Player)

    def test_default_size(self):
        self.assertEqual(self.image, pygame.Surface([2,5]))

    def test_default_speed(self):
        self.assertEqual([self.change_x, self.change_y], [30,0])

    def test_default_level(self):
        self.assertEqual(self.level, None)

