import pygame
import basic_modes as basic
import advanced_modes as adv

from sys import argv


class Layer(object):
    
    blend_mode = 'normal'
    active = True

    apply_filter = {
        'multiply':     (lambda (self, other): self.filter(basic.multiply, other)),
        'color_burn':   (lambda (self, other): self.filter(basic.color_burn, other)),
        'linear_burn':  (lambda (self, other): self.filter(basic.linear_burn, other)),
        'screen':       (lambda (self, other): self.filter(basic.screen, other)),
        'color_dodge':  (lambda (self, other): self.filter(basic.color_dodge, other)),
        'linear_dodge': (lambda (self, other): self.filter(basic.linear_dodge, other)),
        'subtract':     (lambda (self, other): self.filter(basic.subtract, other)),
        'divide':       (lambda (self, other): self.filter(basic.divide, other)),
        'darken':       (lambda (self, other): self.filter(basic.darken, other)),
        'lighten':      (lambda (self, other): self.filter(basic.lighten, other)),
        'overlay':      (lambda (self, other): self.filter(adv.overlay, other)),
        'soft_light':   (lambda (self, other): self.filter(adv.soft_light, other)),
        'hard_light':   (lambda (self, other): self.filter(adv.hard_light, other)),
        'vivid_light':  (lambda (self, other): self.filter(adv.vivid_light, other)),
        'linear_light': (lambda (self, other): self.filter(adv.linear_light, other)),
        'pin_light':    (lambda (self, other): self.filter(adv.pin_light, other)),
        'hard_mix':     (lambda (self, other): self.filter(adv.hard_mix, other))
    }

    def __init__(self, filename):
        try:
            self.pixels = pygame.surfarray.array3d(
                pygame.image.load(filename))
        except pygame.error, message:
            print "Cannot load image:", filename
            raise SystemExit, message

    def filter(self, func, other_image):
        """ break both layers down to the pixel level, and apply the selected
        blend_mode to every channel of the pixel of self.
        """
        for i in self.pixels:
            for j in other_image.pixels:
                i_r, i_g, i_b = i[:, :, 0], i[:, :, 1], i[:, :, 2]
                j_r, j_g, j_b = j[:, :, 0], j[:, :, 1], j[:, :, 2]

                i_r = func(i_r, j_r)
                i_g = func(i_g, j_g)
                i_b = func(i_b, j_b)
                i[:, :, 0], i[:, :, 1], i[:, :, 2] = i_r, i_g, i_b

    def saveLayer(self, filename):
        try:
            surf = pygame.surfarray.make_surface(self.pixels)
        except IndexError, message:
            (width, height, colors) = self.pixels.shape
            surf = pygame.display.set_mode((width, height))
            pygame.surfarray.blit_array(surf, self.pixels)

        pygame.image.save(surf, filename)


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
                layer.apply_filter[layer.blend_mode](self.layers[self.layers.index(layer) - 1])
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
    pixels = getPixelArray("gollum.jpg")
    print type(pixels)

    curr_pixels = pixels
    curr_pixels[100] = 0
    saveSurface(curr_pixels, "gollum_black_column.jpg")

    # [from_left:from_right, from_top:from_bottom, red:green:blue]
    curr_pixels = pixels[50:-50, 200:, :]
    saveSurface(curr_pixels, 'gollum_crop.jpg')

    curr_pixels = pixels[::2, ::2, :]
    saveSurface(curr_pixels, 'gollum_scaled.jpg')

    curr_pixels = pixels[::-1, ::-1, :]
    saveSurface(curr_pixels, 'gollum_flip.jpg')

    stack = Stack()
    layer_1 = Layer('gollum.jpg')
    layer_2 = Layer('gollum.jpg')
    layer_2.blend_mode = 'multiply'
    stack.add_new_layer(layer_1)
    stack.add_new_layer(layer_2)
    stack.save('gollum_multiply.jpg')