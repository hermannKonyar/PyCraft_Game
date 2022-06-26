from fileinput import close
from turtle import position
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from perlin_noise import PerlinNoise
from random import randint

app = Ursina()
grass_texture = load_texture('assets/grass_block.png')
stone_texture = load_texture('assets/stone_block.png')
brick_texture = load_texture('assets/brick_block.png')
dirt_texture = load_texture('assets/dirt_block.png')
sky_texture = load_texture('assets/skybox.png')
arm_texture = load_texture('assets/arm_texture.png')
creeper = load_model('creeper.obj')
tree=load_model('Minecraft Tree.obj')
punch_sound = Audio('assets/punch_sound', loop=False, autoplay=False)
block_pick = 1

window.fps_counter.enabled = False
window.exit_button.visible = False

amp = 24
freq = 100
noise = PerlinNoise(octaves=2, seed=99)
blocks = []


def update():
    global block_pick

    if held_keys['left mouse'] or held_keys['right mouse']:
        hand.active()
    else:
        hand.passive()

    if held_keys['1']:
        block_pick = 1
    if held_keys['2']:
        block_pick = 2
    if held_keys['3']:
        block_pick = 3
    if held_keys['4']:
        block_pick = 4
    if held_keys['0']:
        app.closeWindow()


class Voxel(Button):
    def __init__(self, position=(0, 0, 0), texture=grass_texture):
        super().__init__(
            parent=scene,
            position=position,
            model='assets/block',
            origin_y=0.5,
            texture=texture,
            color=color.color(0, 0, random.uniform(0.9, 1)),
            scale=0.5)

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                punch_sound.play()
                if block_pick == 1:
                    voxel = Voxel(position=self.position +
                                  mouse.normal, texture=grass_texture)
                if block_pick == 2:
                    voxel = Voxel(position=self.position +
                                  mouse.normal, texture=stone_texture)
                if block_pick == 3:
                    voxel = Voxel(position=self.position +
                                  mouse.normal, texture=brick_texture)
                if block_pick == 4:
                    voxel = Voxel(position=self.position +
                                  mouse.normal, texture=dirt_texture)

            if key == 'right mouse down':
                punch_sound.play()
                destroy(self)


class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent=scene,
            model='sphere',
            texture=sky_texture,
            scale=150,
            double_sided=True)
        
class Monster(Entity):
    def __init__(self,x,y,z):
        super().__init__(
            position=(x,y,z),
            parent=scene,
            model=creeper,
            scale=0.09,
            double_sided=True
            
        )
        

# class Tree(Entity):
#     def __init__(self,x,y,z):
#         super().__init__(
#             position=(x,y,z),
#             parent=scene,
#             model=tree,
#             scale=0.02,
#             double_sided=True
#         )

class Hand(Entity):
    def __init__(self):
        super().__init__(
            parent=camera.ui,
            model='assets/arm',
            texture=arm_texture,
            scale=0.2,
            rotation=Vec3(150, -10, 0),
            position=Vec2(0.4, -0.6))

    def active(self):
        self.position = Vec2(0.3, -0.5)

    def passive(self):
        self.position = Vec2(0.4, -0.6)

# def moveMonster():
#     blocky=blocks[randint(0,len(blocks)-1)]
#     vincent.position=Vec3(blocky.x,blocky.y+1,blocky.z)


def generateVoxel():
    global blocks
    quan = 6
    for z in range(80):
        for x in range(80):
            y = floor((noise([x / freq, z / freq])) * amp)
            voxel = Voxel(position=(x, y, z))
            rando=randint(1,200)
            if rando == 1 and quan>0:
                mons=Monster(x,y+1,z)
                # treen=Tree(x+10,y+1,z)
                quan -= 1


vincent = Entity(model=creeper, scale=0.09, x=22, z=16,
                 y=2, texture='creeper.png', double_sided=True)
generateVoxel()
# moveMonster()

player = FirstPersonController()
sky = Sky()
hand = Hand()

app.run()



