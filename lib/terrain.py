from pygame import Rect

class TerrainTile:
    def __init__(self,location,image,is_spikes=False):
        location[0] *= 10
        location[1] *= 10

        self.rect = Rect(location,[10,10])
        self.image = image
        self.is_spikes = is_spikes

class Goal:
    def __init__(self,location,image):
        self.image = image

        location[0] *= 10
        location[1] *= 10

        self.rect = Rect(location,[8,16])

        self.rect.top -= 6
        self.rect.left += 1
