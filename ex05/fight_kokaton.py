from calendar import c
import pygame as pg
import sys
import random

c = 0 #爆発が実行してないときは０　した後は１

class Screen:
    def __init__(self, title, wh, image):
        pg.display.set_caption(title)
        self.sfc = pg.display.set_mode(wh)     # Surface
        self.rct = self.sfc.get_rect()         # Rect
        self.bgi_sfc = pg.image.load(image)    # Surface
        self.bgi_rct = self.bgi_sfc.get_rect() # Rect
        
    def blit(self):
        self.sfc.blit(self.bgi_sfc, self.bgi_rct)
        

class Bird:
    def __init__(self, image: str, size: float, xy):
        self.sfc = pg.image.load(image)                      # Surface
        self.sfc = pg.transform.rotozoom(self.sfc, 0, size)  # Surface
        self.rct = self.sfc.get_rect()                       # Rect
        self.rct.center = xy
    
    def blit(self, scr: Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr: Screen):
        key_states = pg.key.get_pressed() # 辞書
        if key_states[pg.K_UP]    :
            self.rct.centery -= 1
        if key_states[pg.K_DOWN]  :
            self.rct.centery += 1
        if key_states[pg.K_LEFT]  :
            self.rct.centerx -= 1
        if key_states[pg.K_RIGHT] :
            self.rct.centerx += 1
        # 練習7
        if check_bound(self.rct, scr.rct) != (1, 1): # 領域外だったら
            if key_states[pg.K_UP]    :
                self.rct.centery += 1
            if key_states[pg.K_DOWN]  :
                self.rct.centery -= 1
            if key_states[pg.K_LEFT]  :
                self.rct.centerx += 1
            if key_states[pg.K_RIGHT] :
                self.rct.centerx -= 1
        self.blit(scr)
 

class Bomb:
    def __init__(self, color, size, vxy, scr):
        self.sfc = pg.Surface((2*size, 2*size)) # Surface
        self.sfc.set_colorkey((0, 0, 0)) 
        pg.draw.circle(self.sfc, color, (size, size), size)
        self.rct = self.sfc.get_rect() # Rect
        self.rct.centerx = random.randint(0, scr.rct.width)
        self.rct.centery = random.randint(0, scr.rct.height)
        self.vx, self.vy = vxy
    
    def blit(self, scr: Screen):
        scr.sfc.blit(self.sfc, self.rct)
                
    def update(self, scr: Screen):
        self.rct.move_ip(self.vx, self.vy)
        yoko, tate = check_bound(self.rct, scr.rct)
        self.vx *= yoko
        self.vy *= tate
        self.blit(scr)


class Bakuhatu:
    def __init__(self, chr: Bird):
        self.sfc = pg.image.load("fig/images.jpg")
        self.sfc = pg.transform.rotozoom(self.sfc, 0, 10)
        self.rct = self.sfc.get_rect()
        self.rct.center = chr.rct.center
    
    def blit(self, scr: Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr: Screen):
        self.blit(scr)
 
        
def main():
    clock = pg.time.Clock()
    scr = Screen("こうかとん",(1600, 900), "fig/pg_bg.jpg")
    kkt = Bird("fig/6.png", 2.0, (900, 400))
    bkd = Bomb((255,0,0), 10, (+1, +1), scr)
    bkh = Bakuhatu(kkt)
    
    while True:
        global c
        scr.blit()
        for event in pg.event.get():
            if event.type == pg.QUIT: return
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                bkh.update(scr)
                c += 1
                

                
        kkt.update(scr)
        if c == 0:
            bkd.update(scr)
        if kkt.rct.colliderect(bkd.rct): return 

        pg.display.update()
        clock.tick(100000)


def check_bound(rct, scr_rct):
    yoko, tate = +1, +1 # 領域内
    if rct.left < scr_rct.left or scr_rct.right  < rct.right : yoko = -1 # 領域外
    if rct.top  < scr_rct.top  or scr_rct.bottom < rct.bottom: tate = -1 # 領域外
    return yoko, tate


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()