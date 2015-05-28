from pygame import Rect

from random import randint

class Player:
    def __init__(self,image_set,sound_set):
        self.rect = Rect(20,50,10,15)

        self.sound_set = sound_set
        self.image_set = image_set

        self.left = False

        self.walking = False
        self.running = False
        self.jumping = False
        self.in_air = False
        self.cheering = False
        self.done = False

        self.alive = True

        self.velocity = [0,0]

        self.jump_height = 0

        self.frame = 0
        self.frame_timer = 0

        self.sound_set['Start'].play()

    def move(self,solids):
        self.rect.left += self.velocity[0]

        if self.alive:
            for solid_object in solids:
                if self.rect.colliderect(solid_object.rect):
                    if self.velocity[0] < 0:
                        if self.rect.left < solid_object.rect.right:
                            self.rect.left = solid_object.rect.right
                            self.velocity[0] = 0
                    elif self.velocity[0] > 0:
                        if self.rect.right > solid_object.rect.left:
                            self.rect.right = solid_object.rect.left
                            self.velocity[0] = 0

        self.rect.top += self.velocity[1]
        was_in_air = self.in_air
        self.in_air = True

        if self.alive:
            for solid_object in solids:
                if self.rect.colliderect(solid_object.rect):
                    if self.velocity[1] < 0:
                        if self.rect.top < solid_object.rect.bottom:
                            self.rect.top = solid_object.rect.bottom
                            self.velocity[1] = 0
                            if self.jumping:
                                self.jumping = False
                    elif self.velocity[1] > 0:
                        if self.rect.bottom > solid_object.rect.top:
                            self.rect.bottom = solid_object.rect.top
                            self.in_air = False
                            self.velocity[1] = 0

        if not self.cheering:
            if was_in_air and not self.in_air:
                self.sound_set['Land'].play()

        if self.rect.top > 260 and self.alive:
            self.sound_set['Die'].play()
            self.alive = False
            self.velocity[1] = -15
            self.velocity[0] = randint(-7,7)

    def check_spikes(self,spikes):
        if self.alive:
            for spike_set in spikes:
                if self.rect.colliderect(spike_set.rect):
                    self.sound_set['Die'].play()
                    self.alive = False
                    self.velocity[1] = -15
                    self.velocity[0] = randint(-7,7)

    def check_goal(self,goal):
        if self.alive:
            if not self.cheering:
                if self.rect.colliderect(goal.rect):
                    self.sound_set['Win'].play()
                    self.walking = False
                    self.running = False
                    self.cheering = True

    def walk(self):
        self.walking = True
        self.running = False

    def run(self):
        self.walking = False
        self.running = True

    def jump(self):
        if not self.in_air and not self.jumping:
            if not self.cheering:
                self.sound_set['Jump'].play()
            self.jump_height = 0
            self.jumping = True

    def update_velocity(self):
        if self.alive:
            if not self.jumping and not self.in_air:
                self.velocity[1] = 1
            if self.walking:
                if self.left:
                    if self.velocity[0] > -4:
                        self.velocity[0] -= 2
                elif not self.left and self.velocity[0] < 4:
                    self.velocity[0] += 2
                elif abs(self.velocity[0]) > 4 and not self.in_air:
                    if self.velocity[0] < 0:
                        self.velocity[0] += 1
                    else:
                        self.velocity[0] -= 1
            elif self.running:
                if self.left and self.velocity[0] > -8:
                    self.velocity[0] -= 2
                elif not self.left and self.velocity[0] < 8:
                    self.velocity[0] += 2
                elif abs(self.velocity[0]) > 8 and not self.in_air:
                    if self.velocity[0] < 0:
                        self.velocity[0] += 1
                    else:
                        self.velocity[0] -= 1
            elif not self.in_air:
                if self.velocity[0] > 3:
                    self.velocity[0] -= 3
                elif self.velocity[0] < -3:
                    self.velocity[0] += 3
                else:
                    self.velocity[0] = 0
            if self.in_air:
                if self.jumping and self.jump_height < 40:
                    if self.jump_height > 30:
                        self.velocity[1] = -4
                        self.jump_height += 4
                    elif self.jump_height > 20:
                        self.velocity[1] = -8
                        self.jump_height += 8
                    else:
                        self.velocity[1] = -10
                        self.jump_height += 10
                else:
                    if self.velocity[1] < 0:
                        self.velocity[1] = 0
                    elif self.velocity[1] < 8:
                        self.velocity[1] += 1
                    self.jumping = False
        else:
            if self.velocity[1] < 10:
                self.velocity[1] += 1

    def update(self,left,walk,run,jump,solids,spikes,goal):
        if self.alive:
            if self.cheering:
                if not self.in_air:
                    self.jump()
                self.frame += 1
                if self.frame >= 75:
                    self.done = True
            else:
                self.frame_timer += 1
                if self.frame_timer >= 2:
                    self.frame_timer = 0
                    self.frame += 1
                    if self.frame > 3:
                        self.frame = 0

                if walk:
                    self.left = left
                    if run: self.run()
                    else: self.walk()
                else:
                    self.walking = False
                    self.running = False

                if jump: self.jump()
                elif self.jumping:
                    self.jumping = False

                if not walk and not run:
                    self.running = False
                    self.walking = False

        self.move(solids)
        self.check_spikes(spikes)
        self.check_goal(goal)
        self.update_velocity()

    def get_frame(self):
        if self.frame == 2:
            return 2
        elif self.frame in [1,3]:
            return 1
        else:
            return 0

    def get_image(self):
        if not self.alive:
            return self.image_set['Dead'][self.left]
        elif self.jumping:
            return self.image_set['Jump'][self.left]
        elif self.in_air:
            return self.image_set['Fall'][self.left]
        elif self.walking:
            return self.image_set['Walk'][self.get_frame()][self.left]
        elif self.running:
            return self.image_set['Run'][self.get_frame()][self.left]
        else:
            return self.image_set['Idle'][self.left]

    def get_blit_info(self):
        image = self.get_image()
        blit_rect = image.get_rect()

        blit_rect.centerx = self.rect.centerx
        blit_rect.bottom = self.rect.bottom

        return image,blit_rect
