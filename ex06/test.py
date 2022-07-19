import pygame as pg
import sys
import random
import tkinter.messagebox as tkm

kill = 0
tmr = 0

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
        self.sfc = pg.image.load(image)    # Surface
        self.sfc = pg.transform.rotozoom(self.sfc, 0, size)  # Surface
        self.rct = self.sfc.get_rect()          # Rect
        self.rct.center = xy

    def blit(self, scr: Screen):
        #screen_sfc.blit(kkimg_sfc, kkimg_rct)
        scr.sfc.blit(self.sfc, self.rct) 

    def update(self, scr:Screen):
        key_states = pg.key.get_pressed() # 辞書
        if key_states[pg.K_UP]:
             self.rct.centery -= 1
        if key_states[pg.K_DOWN]: 
            self.rct.centery += 1
        if key_states[pg.K_LEFT]: 
            self.rct.centerx -= 1
        if key_states[pg.K_RIGHT]: 
            self.rct.centerx += 1

        if check_bound(self.rct, scr.rct) != (1, 1): # 領域外だったら
            if key_states[pg.K_UP]: 
                self.rct.centery += 1
            if key_states[pg.K_DOWN]: 
                self.rct.centery -= 1
            if key_states[pg.K_LEFT]: 
                self.rct.centerx += 1
            if key_states[pg.K_RIGHT]: 
                self.rct.centerx -= 1
        self.blit(scr)
        
    def attack(self):
        return Shot(self)

class Bomb:
    def __init__(self, color, size, vxy, scr: Screen):
        # self.sfc = pg.Surface((2*size, 2*size)) # Surface
        # self.sfc.set_colorkey((0, 0, 0)) 
        # pg.draw.circle(self.sfc, color, (size, size), size)
        self.sfc = pg.image.load("fig/6.png")    # Surface
        self.sfc = pg.transform.rotozoom(self.sfc, 0, 1)  # Surface
        self.rct = self.sfc.get_rect() # Rect
        self.rct = self.sfc.get_rect()
        self.rct.centerx = 1599
        self.rct.centery = random.randint(0, scr.rct.height)
        self.vx, self.vy = vxy # 練習6


    def blit(self, scr: Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self,scr: Screen):
        # 練習6
        self.rct.move_ip(self.vx, 0)
        # 練習7
        yoko, tate = check_bound(self.rct, scr.rct)
        #self.vx = -3
        self.vy *= tate
        self.blit(scr)

class Bomb2:
    def __init__(self, color, size, vxy, scr: Screen):
        self.sfc = pg.Surface((2*size, 2*size)) # Surface
        self.sfc.set_colorkey((0, 0, 0)) 
        pg.draw.circle(self.sfc, color, (size, size), size)
        self.rct = self.sfc.get_rect() # Rect
        self.rct.centerx = 1599
        self.rct.centery = random.randint(0, scr.rct.height)
        self.vx, self.vy = vxy # 練習6

    def blit(self, scr: Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self,scr: Screen):
        # 練習6
        self.rct.move_ip(self.vx, 0)
        # 練習7
        yoko, tate = check_bound(self.rct, scr.rct)
        self.vx -= yoko
        self.vy *= tate
        self.blit(scr)

class Bomb3:
    def __init__(self, color, size, vxy, scr: Screen):
        self.sfc = pg.Surface((2*size, 2*size)) # Surface
        self.sfc.set_colorkey((0, 0, 0)) 
        pg.draw.circle(self.sfc, color, (size, size), size)
        self.rct = self.sfc.get_rect() # Rect
        self.rct.centerx = random.randint(0, scr.rct.width)
        self.rct.centery = random.randint(0, scr.rct.height)
        self.vx, self.vy = vxy # 練習6

    def blit(self, scr: Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self,scr: Screen):
        # 練習6
        self.rct.move_ip(self.vx, self.vy)
        # 練習7
        yoko, tate = check_bound(self.rct, scr.rct)
        self.vx *= yoko
        self.vy *= tate
        self.blit(scr)

class Shot:
    def __init__(self, chr: Bird):
        self.sfc = pg.image.load("fig/bullet.png")
        self.sfc = pg.transform.rotozoom(self.sfc, -90, 1)  # Surface
        self.rct = self.sfc.get_rect()          # Rect
        self.rct.midleft = chr.rct.center
    
    def blit(self, scr: Screen):
        scr.sfc.blit(self.sfc, self.rct)
        
    def update(self, scr: Screen):
        # 練習6
        self.rct.move_ip(+2, 0) #右方向に速度1で移動する。
        # 練習7
        self.blit(scr)
        if check_bound(self.rct, scr.rct) != (1,1): #領域外に出たらインスタンスを消す
            del self


def main():
    global kill
    global tmr
    
    screen = pg.display.set_mode((1600,900))           #1600x900のウィンドウ作成
    clock = pg.time.Clock()
    scr = Screen("逃げろ!こうかとん",(1600,900),"fig/hiru.jpeg")
    kkt = Bird("fig/free.png", 0.3, (900, 400))
    bkd = Bomb((255,0,0), 10, (-2, +1), scr)
    bkd2 = Bomb2((255,0,0), 10, (+1, +1), scr)
    bkd3 = Bomb3((255,0,0), 10, (+1, +1), scr)

    t_bgimg_sfc = pg.image.load("fig/utyu.png")
    t_bgimg_sfc = pg.transform.rotozoom(t_bgimg_sfc, 0, 1.35) #サイズ変更
    t_bgimg_rect = t_bgimg_sfc.get_rect()
    screen.blit(t_bgimg_sfc, t_bgimg_rect)
    while True:
        screen.blit(t_bgimg_sfc, t_bgimg_rect)
        font = pg.font.Font(None,70)
        txt = font.render("Select Level and push the button",True, "BLUE")
        screen.blit(txt,[400,600])
        font = pg.font.Font(None,80)
        txt = font.render("1:easy 2: nomal 3:hard",True, "YELLOW")
        screen.blit(txt,[500,700])
        for event in pg.event.get():
            if event.type == pg.QUIT: return
        key_states = pg.key.get_pressed() 
        pg.display.update()
    
        
#レベル1
        if key_states[pg.K_1] == True:
            beams = []
            pg.time.set_timer(35,3000)
            while True:
                tmr += 1
                score = tmr+kill*1000
                scr.blit()
                txt = font.render(f"kill:{kill}",True, "Blue")
                screen.blit(txt,[50,800])
                txt = font.render(f"score:{score}",True, "yellow")
                screen.blit(txt,[50,50])
                
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        return
                    if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                        pg.mixer.music.load("music/大爆発2.mp3")
                        pg.mixer.music.play(-1)
                        beams.append(kkt.attack())
                    if event.type==35:
                        bkd = Bomb((255,0,0), 10, (-2, +1), scr) 

                kkt.update(scr)
                bkd.update(scr)
                if len(beams) != 0:
                    for beam in beams:
                        beam.update(scr)
                        if bkd.rct.colliderect(beam.rct):
                            del bkd
                            bkd = Bomb((255,0,0), 10, (-2, +1), scr)
                            kill += 1
                            
                if kkt.rct.colliderect(bkd.rct): #爆弾インスタンスのrect変数
                    tkm.showwarning("お前が殺した。",f"score:{score}")
                    #txt = font.render("Select Level and push the button",True, "BLUE")
                    #screen.blit(txt,[400,600])
                    return
                pg.display.update()
                clock.tick(1000)
#レベル2
        if key_states[pg.K_2] == True:
            beams = []
            while True:
                scr.blit()
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        return
                    if event.type == pg.KEYDOWN and event.key == pg.K_e:
                        pg.mixer.music.load("music/大爆発2.mp3")
                        pg.mixer.music.play(-1)
                        beams.append(kkt.attack())

                kkt.update(scr)
                bkd.update(scr)
                bkd2.update(scr)
                if len(beams) != 0:
                    for beam in beams:
                        beam.update(scr)
                        if bkd.rct.colliderect(beam.rct):
                            del bkd
                            tkm.showinfo("すばらすぃ","やるやん。")
                            return
                        if bkd2.rct.colliderect(beam.rct):
                            del bkd2
                            tkm.showinfo("すばらすぃ","やるやん。")
                            return
                if kkt.rct.colliderect(bkd.rct): #爆弾インスタンスのrect変数
                    tkm.showwarning("お前が殺した。","あなたが殺した。")
                    return
                if kkt.rct.colliderect(bkd2.rct): #爆弾インスタンスのrect変数
                    tkm.showwarning("お前が殺した。","あなたが殺した。")
                    return
                pg.display.update()
                clock.tick(1000)

#レベル3
        if key_states[pg.K_3] == True:
            beams = []
            while True:
                scr.blit()
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        return
                    if event.type == pg.KEYDOWN and event.key == pg.K_e:
                        pg.mixer.music.load("music/大爆発2.mp3") #効果音を追加
                        pg.mixer.music.play(-1)
                        beams.append(kkt.attack())

                kkt.update(scr)
                bkd.update(scr)
                bkd2.update(scr)
                bkd3.update(scr)
                if len(beams) != 0:
                    for beam in beams:
                        beam.update(scr)
                        if bkd.rct.colliderect(beam.rct):
                            del bkd
                            tkm.showinfo("すばらすぃ","やるやん。")
                            return
                        if bkd2.rct.colliderect(beam.rct):
                            del bkd2
                            tkm.showinfo("すばらすぃ","やるやん。")
                            return
                        if bkd3.rct.colliderect(beam.rct):
                            del bkd3
                            tkm.showinfo("すばらすぃ","やるやん。")
                            return
                if kkt.rct.colliderect(bkd.rct): #爆弾インスタンスのrect変数
                    tkm.showwarning("お前が殺した。","あなたが殺した。")
                    return
                if kkt.rct.colliderect(bkd2.rct): #爆弾インスタンスのrect変数
                    tkm.showwarning("お前が殺した。","あなたが殺した。")
                    return
                if kkt.rct.colliderect(bkd3.rct): #爆弾インスタンスのrect変数
                    tkm.showwarning("お前が殺した。","あなたが殺した。")
                    return
                pg.display.update()
                clock.tick(1000)
        
def check_bound(rct, scr_rct):
    '''
    [1] rct: こうかとん or 爆弾のRect
    [2] scr_rct: スクリーンのRect
    '''
    yoko, tate = +1, +1 # 領域内
    if rct.left < scr_rct.left or scr_rct.right  < rct.right : yoko = -1 # 領域外
    if rct.top  < scr_rct.top  or scr_rct.bottom < rct.bottom: tate = -1 # 領域外
    return yoko, tate

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()