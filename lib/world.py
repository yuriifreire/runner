from pygame import Rect,Surface
from pygame.locals import SRCALPHA

from terrain import TerrainTile, Goal
from player import Player

from random import choice, randint, random, shuffle

class LevelSegment:
    def __init__(self,number,layout_type,tile_images,previous_segment_data):
        self.terrain_tiles = []
        self.spike_tiles = []

        self.goal = None

        self.data = {}

        if 'height' in previous_segment_data.keys():
            if previous_segment_data['height'] > 21:
                previous_segment_data['height'] = 21

        if layout_type == 'Flat':
            self.data['height'] = previous_segment_data['height']

            for height in range(self.data['height'],25):
                self.terrain_tiles += [TerrainTile([spam+(24*number),height],tile_images[False],False) for spam in range(0,24)]
        if layout_type == 'Start':
            self.data['height'] = randint(16,20)

            for height in range(self.data['height'],25):
                self.terrain_tiles += [TerrainTile([spam,height],tile_images[False],False)
                                        for spam in range(24)]

            for height in range(1,self.data['height']):
                self.terrain_tiles.append(TerrainTile([0,height],tile_images[False],False))
        if layout_type == 'End':
            self.data['height'] = previous_segment_data['height']

            for height in range(self.data['height'],25):
                self.terrain_tiles += [TerrainTile([spam+(number*24),height],tile_images[False],False)
                                        for spam in range(24)]

            for height in range(1,self.data['height']):
                self.terrain_tiles.append(TerrainTile([23+(number*24),height],tile_images[False],False))

            self.goal = Goal([randint(6,16)+(number*24),self.data['height']-1],tile_images['Goal'])
        if layout_type == 'Uneven':
            self.data['height'] = previous_segment_data['height']

            breaks = 1

            if randint(0,6) < 4:
                breaks = 4
            elif randint(0,3) < 2:
                breaks = 2

            self.data['height'] = self.data['height'] + randint(-1,2)

            last_had_spikes = False
            number_of_spikes = 0

            for piece in range(breaks):
                tile_range = [0,0]
                tile_range[0] = (24 // breaks) * piece
                tile_range[1] = tile_range[0] + (24 // breaks)

                for height in range(self.data['height'],25):
                    self.terrain_tiles += [TerrainTile([spam+(24*number),height],tile_images[False],False) for
                                spam in range(*tile_range)]

                ground_mod = randint(-2,2)

                if self.data['height'] + ground_mod <= 8:
                    ground_mod = randint(1,2)
                elif self.data['height'] + ground_mod >= 18:
                    ground_mod = randint(-2,-1)

                if number_of_spikes < 2 and last_had_spikes == False:
                    if number > 0 or piece > 2:
                        if breaks == 4 and ground_mod > 0:
                            if randint(0,7) < 6:
                                number_of_spikes += 1
                                last_had_spikes = True
                                range_mod = [0,0]
                                range_mod[0] = randint(0,3)
                                range_mod[1] = randint(0,(4 - range_mod[0]))
                                tile_range[0] += range_mod[0]
                                tile_range[1] -= range_mod[1]
                                self.spike_tiles += [TerrainTile([eggs+(24*number),self.data['height']-1],tile_images[True],True) for
                                        eggs in range(*tile_range)]
                        elif breaks == 2 and ground_mod >= 0:
                            if randint(0,7) < 5:
                                range_mod = [0,0]
                                range_mod[0] = randint(3,6)
                                range_mod[1] = randint(3,(9 - range_mod[0]))
                                tile_range[0] += range_mod[0]
                                tile_range[1] -= range_mod[1]
                                self.spike_tiles += [TerrainTile([eggs+(24*number),self.data['height']-1],tile_images[True],True) for
                                        eggs in range(*tile_range)]
                        elif number_of_spikes < 2:
                            last_had_spikes = False

                self.data['height'] += ground_mod
        if layout_type == 'Platform':
            self.data['height'] = previous_segment_data['height']

            self.data['platforms'] = []

            number_of_platforms = randint(2,3)

            current_height = self.data['height'] - randint(2,3)

            for platform in range(number_of_platforms+1):
                platform_rect = Rect((((24//number_of_platforms)*platform)+randint(0,4)),
                                    current_height,
                                    randint(3,5),1)

                current_height += randint(-2,2)

                if (current_height - self.data['height']) > -3:
                    current_height = self.data['height'] - 3
                elif current_height < 8:
                    current_height = 8

                self.terrain_tiles += [TerrainTile([(spam+platform_rect.left)+(number*24),
                                                current_height], tile_images[False],False)
                                                for spam in range(platform_rect.width)]

                self.data['platforms'].append(platform_rect)

            under_platform = 'Flat'

            if random() < 0.5:
                under_platform = 'Spike Pit'
            elif random() < 0.9:
                under_platform = 'Bottomless Pit'

            if 'Pit' in under_platform:
                pit_width = randint(4,8)
                pit_offset = randint(-4,4)

                pit_left = 24 - (pit_width // 2)
                pit_left += pit_offset

                if pit_left < 3:
                    pit_left = 3
                elif (pit_left + pit_width) > 21:
                    pit_left = 21 - pit_width

                pit_depth = -1

                if 'Bottomless' not in under_platform:
                    pit_depth = randint(3,(self.data['height']-2))


                for height in range(self.data['height'],25):
                    self.terrain_tiles += [TerrainTile([spam+(number*24),height],tile_images[False],False)
                                    for spam in range(0,pit_left)]
                    self.terrain_tiles += [TerrainTile([eggs+(number*24),height],tile_images[False],False)
                                    for eggs in range((pit_left+(pit_width+1)),25)]

                if pit_depth != -1:
                    for height in range((self.data['height']+pit_depth),25):
                        self.terrain_tiles += [TerrainTile([bacon+(number*24),height],tile_images[False],False)
                                    for bacon in range(pit_left,(pit_left+pit_width)+1)]

                if 'Spike' in under_platform:
                    self.spike_tiles += [TerrainTile([toast+(number*24),(self.data['height']+(pit_depth-1))],
                                                tile_images[True],True)
                                                    for toast in range(pit_left,(pit_left+pit_width)+1)]
            else:
                for height in range(self.data['height'],25):
                    self.terrain_tiles += [TerrainTile([spam+(number*24),height],
                                                tile_images[False],False) for
                                                        spam in range(24)]
        elif 'Platform_Chain' in layout_type:
            platform_start_height = previous_segment_data['height']
            platform_start_height += randint(-2,2)

            number_of_platforms = randint(3,4)

            self.data['platforms'] = []

            if 'Start' in layout_type:

                start_ledge_width = randint(3,8)
                start_ledge_height = previous_segment_data['height']

                if start_ledge_height > 23:
                    start_ledge_height = 23

                self.data['height'] = platform_start_height

                for height in range(start_ledge_height,25):
                    self.terrain_tiles += [TerrainTile([spam+(number*24),height],
                                            tile_images[False],False) for spam in range(start_ledge_width)]

            elif 'End' in layout_type:
                end_ledge_width = randint(3,8)
                end_ledge_height = previous_segment_data['height']
                end_ledge_height += randint(-1,3)

                if end_ledge_height > 23:
                    end_ledge_height = 23

                self.data['height'] = end_ledge_height

                for height in range(end_ledge_height,25):
                    self.terrain_tiles += [TerrainTile([(eggs+(number*24))-(end_ledge_width+1),height],
                                            tile_images[False],False) for eggs in range(end_ledge_width)]

            if 'End' not in layout_type:
                self.data['height'] = previous_segment_data['height']

            for spam in range(number_of_platforms+1):
                self.data['platforms'].append(Rect((randint(1,3)+(spam*(24//number_of_platforms)))+(number*24),
                                platform_start_height,randint(3,(24//number_of_platforms)),1))

                platform_start_height += randint(-2,2)

                if platform_start_height >= 20:
                    platform_start_height += randint(-2,-1)
                elif platform_start_height >= 16:
                    platform_start_height += randint(-2,1)
                elif platform_start_height < 8:
                    platform_start_height += randint(1,2)
                elif platform_start_height < 10:
                    platform_start_height += randint(-1,2)

            if 'End' not in layout_type:
                self.data['height'] = self.data['platforms'][-1].top

            for platform in self.data['platforms']:
                self.terrain_tiles += [TerrainTile([platform.left+spam,platform.top],
                                        tile_images[False],False)for spam in range(platform.width)]

class GameWorld:
    def __init__(self,length,image_set,sound_set,**favors):
        self.area = Rect(0,0,(length*240),240)
        self.image_set = image_set
        self.sound_set = sound_set

        self.completion_score = 0

        self.favors = favors
        for needed_key in ['Flat','Uneven','Platform','Platform_Chain']:
            if needed_key not in self.favors.keys():
                self.favors[needed_key] = 0.5

        previous_type = 'Flat'
        segments = []

        segments.append(LevelSegment(0,'Start',self.image_set['Terrain'],{}))

        for number in range(1,length+1):
            next_type = self.choose_segment_type(previous_type)
            previous_type = next_type

            if next_type == 'Uneven':
                self.completion_score += 500
            elif next_type == 'Platform':
                self.completion_score += 250
            elif 'Platform Chain' in next_type:
                self.completion_score += 750
            segments.append(LevelSegment(number,
                    next_type,
                        self.image_set['Terrain'], segments[-1].data))

        segments.append(LevelSegment(length+1,'End',self.image_set['Terrain'],segments[-1].data))

        self.goal = None
        self.player = Player(self.image_set['Player'],self.sound_set['Player'])

        self.completion_score *= (length//2)

        self.terrain_tiles = []
        self.spike_tiles = []

        for segment in segments:
            self.terrain_tiles += segment.terrain_tiles
            self.spike_tiles += segment.spike_tiles
            if not self.goal:
                self.goal = segment.goal

    def reset_player(self):
        self.player = Player(self.image_set['Player'],self.sound_set['Player'])

    def update(self,left,walk,run,jump):
        self.player.update(left,walk,run,jump,
                            self.terrain_tiles,self.spike_tiles,self.goal)

    def choose_segment_type(self,previous_type):
        for segment_type in self.favors.keys():
            if segment_type in previous_type:
                if 'Start' in previous_type:
                    if random() < self.favors[previous_type.replace(' Start','')]:
                        return previous_type.replace(' Start','')
                    else:
                        return previous_type.replace(' Start', ' End')
                elif 'End' in previous_type:
                    types_to_check = list(self.favors.keys())
                    shuffle(types_to_check)
                    for next_type in types_to_check:
                        if next_type != previous_type.replace(' End',''):
                            if random() < self.favors[next_type]:
                                if next_type == 'Platform_Chain':
                                    return next_type + ' Start'
                                else:
                                    return next_type
                        return choice(['Flat','Uneven'])
                else:
                    if previous_type == 'Platform_Chain':
                        if random() < self.favors[previous_type]:
                            return previous_type
                        else:
                            return previous_type + ' End'
                    else:
                        types_to_check = list(self.favors.keys())
                        shuffle(types_to_check)
                        for next_type in types_to_check:
                            if random() < self.favors[next_type]:
                                if next_type == 'Platform_Chain':
                                    return next_type + ' Start'
                                else:
                                    return next_type
                            return choice(['Flat','Uneven','Platform'])
