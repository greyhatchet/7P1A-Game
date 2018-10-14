from Platform import *
import unittest

class PlayerTestCase(unittest.TestCase):
    def setUp(self):
        self.player = Player()

    def test_default_size(self):
        self.assertNotEqual(self.player.image, pygame.Surface([40,60]))

    def test_default_speed(self):
        self.assertEqual([self.player.change_x, self.player.change_y], [0,0])

    def test_default_level(self):
        self.assertEqual(self.player.level, None)

    '''
    def test_update(self):
        x = self.player.rect.x
        y = self.player.rect.y
        x_change = self.player.change_x
        y_change = self.player.change_y
        self.player.update()
        self.assertEqual(self.player.rect.x, x + x_change)
        self.assertEqual(self.player.rect.y, y + y_change)
        
    '''

    def test_go_left(self):
        self.player.go_left()
        self.assertEqual(self.player.change_x, -6)

    def test_go_right(self):
        self.player.go_right()
        self.assertEqual(self.player.change_x, 6)

    def test_stop(self):
        self.player.stop()
        self.assertEqual(self.player.change_x, 0)

'''
class ShootTestCase(unittest.TestCase):

    def setUp(self):
        self.shoot = Shoot()

    
    def test_default_size(self):
        self.assertEqual(self.shoot.image, pygame.Surface([2,5]))
    

    def test_default_speed(self):
        self.assertEqual([self.shoot.change_x, self.shoot.change_y], [30,0])

    def test_default_level(self):
        self.assertEqual(self.shoot.level, None)
        
'''

class PlatformTestCase(unittest.TestCase):

    def setUp(self, width = 0, height = 0):
        self.platform = Platform(width, height)
        self.platform.width = width
        self.platform.height = height

    def test_inits(self):
        self.assertEqual(str(self.platform.image), str(pygame.Surface([self.platform.width, self.platform.height])))
        self.assertEqual(self.platform.rect, self.platform.image.get_rect())

class LevelTestCase(unittest.TestCase):

    def setUp(self):
        player = Player()
        self.level = Level(player)

    def test_inits(self):
        self.assertEqual(str(self.level.platform_list), '<Group(0 sprites)>')
        self.assertEqual(str(self.level.enemy_list), '<Group(0 sprites)>')
        self.assertEqual(self.level.world_shift, 0)





if __name__ == '__main__':
    unittest.main()