from turtle import window_width
import pygame as pg
import sys
import random
import tkinter.messagebox as tkm
import tkinter as tk

#基本コード　野々上

tmr = 0 #八亀

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
        self.sfc = pg.transform.rotozoom(self.sfc, -90, size)  # Surface
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
        self.sfc = pg.image.load("image_gl/bullet.png")
        self.sfc = pg.transform.rotozoom(self.sfc, -90, 1.0)  # Surface
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


class Player:
    #コンストラクタ
    def __init__(self, image: str, size: float, xy):
        self.sfc = pg.image.load(image)    # Surface
        self.sfc = pg.transform.rotozoom(self.sfc, -90, size)  # Surface
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


class Enemy:
    def __init__(self,image, size, vxy, scr: Screen):
        self.sfc = pg.image.load(image)
        self.sfc = pg.transform.rotozoom(self.sfc, -90, size)
        self.rct = self.sfc.get_rect() # Rect
        self.rct.centerx = scr.rct.width
        self.rct.centery = random.randint(0, scr.rct.height)
        self.vx, self.vy = vxy # 練習6


    def blit(self, scr: Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self,scr: Screen):
        # 練習6
        self.rct.move_ip(self.vx, self.vy)
        # 練習7
        yoko, tate = check_bound(self.rct, scr.rct)
        self.vy *= tate
        self.blit(scr)
    

class Boss:
    def __init__(self,image, size, vxy, scr: Screen):
        self.sfc = pg.image.load(image)
        self.sfc = pg.transform.rotozoom(self.sfc, 0, size)
        self.rct = self.sfc.get_rect() # Rect
        self.rct.centerx = scr.rct.width / 2
        #self.rct.centery = random.randint(0, scr.rct.height)
        self.rct.centery = scr.rct.height / 2

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

def main():
    global tmr

    screen = pg.display.set_mode((1600,900))           #1600x900のウィンドウ作成
    clock = pg.time.Clock()
    scr = Screen("宇宙伝説",(1600,900),"fig/town.jpg")
    kkt = Player("image_gl/starship.png", 1.0, (900, 400))
    enemy1 = Enemy("image_gl/enemy3.png", 0.7, (-2, 1), scr)
    boss = 0
    bkd = Bomb((255,0,0), 10, (+1, +1), scr)
    bkd2 = Bomb((255,0,0), 10, (+1, +1), scr)
    bkd3 = Bomb((255,0,0), 10, (+1, +1), scr)
    kill = 0#撃破数
    hp = 10#もともと10
    tmr = 0#八亀
    root = tk.Tk()#引地
    root.withdraw()#引地

    t_bgimg_sfc = pg.image.load("fig/Snapshot.png")#野々上
    t_bgimg_sfc = pg.transform.rotozoom(t_bgimg_sfc, 0, 0.80) #サイズ変更
    t_bgimg_rect = t_bgimg_sfc.get_rect()
    screen.blit(t_bgimg_sfc, t_bgimg_rect)
    while True:
        screen.blit(t_bgimg_sfc, t_bgimg_rect)
        # font = pg.font.Font(None,70)
        # txt = font.render("Select Level and push the button",True, "BLUE")
        # screen.blit(txt,[400,600])
        font = pg.font.Font(None,80)
        txt = font.render("Press 1 to start",True, "YELLOW")
        screen.blit(txt,[500,700])
        for event in pg.event.get():
            if event.type == pg.QUIT or event.type == pg.K_q:#引地
                pg.quit()#引地
                sys.exit()#引地
        key_states = pg.key.get_pressed() 
        pg.display.update()
#レベル1
        if key_states[pg.K_1] == True:#野々上
            beams = []
            pg.time.set_timer(35, 7000)
            while True:
                tmr += 1 #八亀
                time = tmr/200


                scr.blit()
                txt = font.render(f"Time:{time}",True, "yellow")#八亀
                screen.blit(txt,[50,50])
                font = pg.font.Font(None,70)#川島
                txt = font.render(f"kill:{kill}",True, "BLUE")#川島
                screen.blit(txt,[50,800])#川島
                if boss != 0:#加藤
                    font = pg.font.Font(None,70)#加藤
                    txt = font.render(f"Boss HP:{hp}",True, "RED")#加藤
                    screen.blit(txt,[1100,100])#加藤
                for event in pg.event.get():
                    if event.type == pg.QUIT or event.type == pg.K_q:#引地
                        pg.quit()#引地
                        sys.exit()#引地
                    if event.type == pg.KEYDOWN and event.key == pg.K_e:
                        pg.mixer.music.load("music/大爆発2.mp3")#野々上
                        pg.mixer.music.play(-1)
                        beams.append(kkt.attack())
                    if event.type == 35:
                        enemy1 = Enemy("image_gl/enemy3.png", 0.7, (-2, 1), scr)


                kkt.update(scr)
                enemy1.update(scr)
                if boss != 0:#加藤
                    boss.update(scr)#加藤
                            
                if len(beams) != 0:
                    for beam in beams:
                        beam.update(scr)
                        if enemy1.rct.colliderect(beam.rct):
                            del enemy1#加藤
                            enemy1 = Enemy("image_gl/enemy3.png", 0.7, (-2, 1), scr)#川島
                            kill += 1#川島
                        if boss != 0:#加藤
                            if boss.rct.colliderect(beam.rct):#加藤
                                beams = []#加藤
                                hp -= 1#加藤
                            if hp == 0:#加藤
                                tkm.showinfo("GG", "ゲームクリア！"+"\n"+f"クリアタイム：{time}")#加藤
                                return
                        if boss == 0:#加藤
                            if kill == 5:#加藤
                                boss = Boss("image_gl/enemy_boss.png", 0.5, (-2, -2), scr)#加藤
                                #hp = 10
                            
                if kkt.rct.colliderect(enemy1.rct): #爆弾インスタンスのrect変数
                    tkm.showwarning("お前が殺した。","あなたが殺した。")
                    return
                if boss != 0:
                    if kkt.rct.colliderect(boss.rct):
                        tkm.showwarning("お前が殺した。","あなたが殺した。")
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
                enemy1.update(scr)
                bkd2.update(scr)
                if len(beams) != 0:
                    for beam in beams:
                        beam.update(scr)
                        if enemy1.rct.colliderect(beam.rct):
                            del enemy1
                            tkm.showinfo("すばらすぃ","やるやん。")
                            return
                        if bkd2.rct.colliderect(beam.rct):
                            del bkd2
                            tkm.showinfo("すばらすぃ","やるやん。")
                            return
                if kkt.rct.colliderect(enemy1.rct): #爆弾インスタンスのrect変数
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
                enemy1.update(scr)
                bkd2.update(scr)
                bkd3.update(scr)
                if len(beams) != 0:
                    for beam in beams:
                        beam.update(scr)
                        if enemy1.rct.colliderect(beam.rct):
                            del enemy1
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
    while True:#引地
        main()#引地