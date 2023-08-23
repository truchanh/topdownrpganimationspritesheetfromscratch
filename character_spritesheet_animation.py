import pygame as pg
pg.init()

class Player(pg.sprite.Sprite):
    """docstring for Player"""
    def __init__(self, pos,group):
        super(Player, self).__init__(group)
        self.sheet = pg.image.load('gfx/player.png')
        self.image_w = self.sheet.get_width()//6
        self.image_h = self.sheet.get_height()/10
        self.rects = []
        for i in range(10):
            for j in range(6):
                self.rects.append(
                    pg.Rect(
                        j*self.image_w,
                        i*self.image_h,
                        self.image_w,
                        self.image_h
                        )
                    )
        
        self.anims = {'idle down' : self.rects[:6],
                      'idle left' : self.rects[6:12],
                      'idle right': self.rects[6:12],
                      'idle up'   : self.rects[12:18],
                      'run down'  : self.rects[18:24],
                      'run left'  : self.rects[24:30],
                      'run right' : self.rects[24:30],
                      'run up'    : self.rects[30:36],
                      'atk down'  : self.rects[36:40],
                      'atk left'  : self.rects[42:46],
                      'atk right' : self.rects[42:46],
                      'atk up'    : self.rects[48:52],
                      'die'       : self.rects[54:57]}
        self.index = 0
        self.current_state = 'idle'
        self.current_direction = 'down'
        self.status = f'{self.current_state} {self.current_direction}'
        if len(self.status.split()) == 2:
            self.current_animation = self.anims[self.status]
        else:
            self.current_animation = self.anims['die']
            
        if self.current_direction == 'left':
            self.image = pg.transform.flip(
                self.sheet.subsurface(self.current_animation[self.index]),1,0)
        else:
            
            self.image = self.sheet.subsurface(self.current_animation[self.index])

        bound_rect = self.image.get_bounding_rect(min_alpha=1)
        raw_image = self.image.subsurface(bound_rect)
        raw_img_w, raw_img_h = raw_image.get_size()
        
        ##two required attr: sprite.image and sprite.rect
        self.image = pg.transform.scale(raw_image,(raw_img_w*2,raw_img_h*2))
        self.rect = self.image.get_rect(center=pos)

        self.direction = pg.Vector2()
        self.speed = 250
    def update(self,dt):
        ##move the player
        self.rect.center += self.direction*self.speed*dt

        ##update the current animation depend on status        
        self.status = f'{self.current_state} {self.current_direction}'
        self.current_animation = self.anims[self.status]

        ##animation loop
        self.index += 1
        if self.index > len(self.current_animation)-1:
            self.index = 0

        ##update the corresponding image and rect due to the animation
        if self.current_direction == 'left':
            self.image = pg.transform.flip(
                self.sheet.subsurface(self.current_animation[self.index]),1,0)
        else:    
            self.image = self.sheet.subsurface(self.current_animation[self.index])

        bound_rect = self.image.get_bounding_rect(min_alpha=1)
        raw_image = self.image.subsurface(bound_rect)
        raw_img_w, raw_img_h = raw_image.get_size()

        self.image = pg.transform.scale(raw_image,(raw_img_w*3,raw_img_h*3))
        self.rect = self.image.get_rect(center=self.rect.center)


def keydown_events(e):
    '''when user press a key'''
    match e.key:
        case pg.K_LEFT:
            player.sprite.direction.x = -1
            player.sprite.current_state = 'run'
            player.sprite.current_direction = 'left'
        case pg.K_RIGHT:
            player.sprite.direction.x = 1
            player.sprite.current_state = 'run'
            player.sprite.current_direction = 'right'
        case pg.K_UP:
            player.sprite.direction.y = -1
            player.sprite.current_state = 'run'
            player.sprite.current_direction = 'up'
        case pg.K_DOWN:
            player.sprite.direction.y = 1
            player.sprite.current_state = 'run'
            player.sprite.current_direction = 'down'
        case pg.K_LSHIFT:
            player.sprite.current_state = 'atk'
            
    
            
def keyup_events(e):
    '''when user release/unpress a key from being pressed'''
    match e.key:
        case pg.K_LEFT:
            player.sprite.direction.x = 0
            player.sprite.current_state = 'idle'
            player.sprite.current_direction = 'left'
        case pg.K_RIGHT:
            player.sprite.direction.x = 0
            player.sprite.current_state = 'idle'
            player.sprite.current_direction = 'right'
        case pg.K_UP:
            player.sprite.direction.y = 0
            player.sprite.current_state = 'idle'
            player.sprite.current_direction = 'up'
        case pg.K_DOWN:
            player.sprite.direction.y = 0
            player.sprite.current_state = 'idle'
            player.sprite.current_direction = 'down'
        case pg.K_LSHIFT:  #still running even after stop wielding the weapon?
            if player.sprite.direction.x != 0 and player.sprite.direction.y != 0:
                player.sprite.current_state = 'run'
            else:
                player.sprite.current_state = 'idle'
     

WINW = 640
WINH = 480
player = pg.sprite.GroupSingle()
Player((WINW/2,WINH/2),player)
PLAYER_UPDATE = pg.event.custom_type()
pg.time.set_timer(PLAYER_UPDATE,150)

win = pg.display.set_mode((WINW,WINH),pg.SRCALPHA,16)
clk = pg.time.Clock()

done = 0
while not done:
    time_delta = clk.tick(30)/1000
    for e in pg.event.get():
        if e.type in (pg.QUIT,pg.WINDOWCLOSE):
            done = 1
        elif e.type == PLAYER_UPDATE:
            player.update(time_delta)
        elif e.type == pg.KEYDOWN:
            keydown_events(e)
        elif e.type == pg.KEYUP:
            keyup_events(e)

    win.fill('magenta')
    player.draw(win)
    pg.display.flip()
pg.quit()
