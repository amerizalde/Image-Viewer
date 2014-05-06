from pprint import pprint
import pygame
import basic_modes as basic
import advanced_modes as adv

from sys import argv


class Layer(object):
    
    blend_mode = 'normal'
    active = True

    apply_filter = {
        'multiply':     (lambda x: x[0].filter(basic.multiply, x[1])),
        'color_burn':   (lambda x: x[0].filter(basic.color_burn, x[1])),
        'linear_burn':  (lambda x: x[0].filter(basic.linear_burn, x[1])),
        'screen':       (lambda x: x[0].filter(basic.screen, x[1])),
        'color_dodge':  (lambda x: x[0].filter(basic.color_dodge, x[1])),
        'linear_dodge': (lambda x: x[0].filter(basic.linear_dodge, x[1])),
        'subtract':     (lambda x: x[0].filter(basic.subtract, x[1])),
        'divide':       (lambda x: x[0].filter(basic.divide, x[1])),
        'darken':       (lambda x: x[0].filter(basic.darken, x[1])),
        'lighten':      (lambda x: x[0].filter(basic.lighten, x[1])),
        'overlay':      (lambda x: x[0].filter(adv.overlay, x[1])),
        'soft_light':   (lambda x: x[0].filter(adv.soft_light, x[1])),
        'hard_light':   (lambda x: x[0].filter(adv.hard_light, x[1])),
        'vivid_light':  (lambda x: x[0].filter(adv.vivid_light, x[1])),
        'linear_light': (lambda x: x[0].filter(adv.linear_light, x[1])),
        'pin_light':    (lambda x: x[0].filter(adv.pin_light, x[1])),
        'hard_mix':     (lambda x: x[0].filter(adv.hard_mix, x[1]))
    }

    def __init__(self, filename):
        try:
            self._pixels = pygame.surfarray.array3d(
                pygame.image.load(filename))
            self.pixels = self._pixels
        except pygame.error, message:
            print "Cannot load image:", filename
            raise SystemExit, message

    def filter(self, func, other_image):
        """ break both layers down to the pixel level, and apply the selected
        blend_mode to every channel of the pixel of self.
        """
        for i in self.pixels:
            pprint(i)
            for j in other_image.pixels:
                i_r, i_g, i_b = i[0], i[1], i[2]
                j_r, j_g, j_b = j[0], j[1], j[2]

                i_r = func(i_r, j_r)
                i_g = func(i_g, j_g)
                i_b = func(i_b, j_b)
                i[0], i[1], i[2] = i_r, i_g, i_b

    def saveLayer(self, filename):
        try:
            surf = pygame.surfarray.make_surface(self.pixels)
        except IndexError:
            (width, height, colors) = self.pixels.shape
            surf = pygame.display.set_mode((width, height))
            pygame.surfarray.blit_array(surf, self.pixels)

        pygame.image.save(surf, filename)

    def reset(self):
        self.pixels = self._pixels


class Stack(object):
    """ the layer stack. produces the final image from all of its child
    Layers.
    """

    layers = []

    def add_new_layer(self, layer):
        self.layers.append(layer)

    def remove_layer(self, layer):
        try:
            self.layers.remove(layer)
        except Exception, message:
            print message
            pass

    def save(self, filename):
        for layer in self.layers:
            if layer.blend_mode != 'normal':
                # assuming index 0 is always the background layer and 'normal'...
                layer.apply_filter[layer.blend_mode]((
                                    # passing the layer, and the previous layer
                                    layer,
                                    self.layers[self.layers.index(layer) - 1]))
        # save the top layer
        self.layers[-1].saveLayer(filename)



def getPixelArray(filename):
    try:
        image = pygame.image.load(filename)
    except pygame.error, message:
        print "Cannot load image:", filename
        raise SystemExit, message
    return pygame.surfarray.array3d(image)


def saveSurface(pixels, filename):
    try:
        surf = pygame.surfarray.make_surface(pixels)
    except IndexError, message:
        print message
        (width, height, colors) = pixels.shape
        surf = pygame.display.set_mode((width, height))
        pygame.surfarray.blit_array(surf, pixels)

    pygame.image.save(surf, filename)



if __name__ == "__main__":
    
    a = Layer('gollum.jpg')
    red_channel = Layer('gollum.jpg')
    green_channel = Layer('gollum.jpg')
    blue_channel = Layer('gollum.jpg')
    x, y, z = a.pixels.shape
    for i in xrange(x):
        for j in xrange(y):
            ii = i
            jj = j
            red_channel.pixels[ii, jj] = a.pixels[ii, jj] * [1, 0, 0]
            green_channel.pixels[ii, jj] = a.pixels[ii, jj] * [0, 1, 0]
            blue_channel.pixels[ii, jj] = a.pixels[ii, jj] * [0, 0, 1]

    red_channel.saveLayer('red_channel.jpg')
    green_channel.saveLayer('green_channel.jpg')
    blue_channel.saveLayer('blue_channel.jpg')
