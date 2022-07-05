import pygame as pg
import sys
import random
import tkinter.messagebox as tkm
n = 0

def main():
    global n
    clock = pg.time.Clock()
    
    #スクリーンと背景画像
    pg.display.set_caption("逃げろ！こうかとん")
    screen_sfc = pg.display.set_mode((1550, 800))
    screen_rct = screen_sfc.get_rect()
    bgimg_sfc = pg.image.load("fig/pg_bg.jpg")
    bgimg_rct = bgimg_sfc.get_rect()
    screen_sfc.blit(bgimg_sfc, bgimg_rct)
    
    #こうかとん
    kkimg_sfc = pg.image.load("fig/6.png")
    kkimg_sfc = pg.transform.rotozoom(kkimg_sfc, 0, 2.0)
    kkimg_rct = kkimg_sfc.get_rect()
    kkimg_rct.center = 900, 400
    
    #爆弾
    bmimg_sfc = pg.Surface((20, 20))
    bmimg_sfc.set_colorkey(0)
    pg.draw.circle(bmimg_sfc, (255, 0, 0), (10, 10), 10)
    bmimg_rct = bmimg_sfc.get_rect()
    bmimg_rct.centerx = random.randint(0, screen_rct.width)
    bmimg_rct.centery = random.randint(0, screen_rct.height)
    vx, vy = +1, +1
    
    #爆弾生成(させようと頑張ったところ)
    num_key = pg.key.get_pressed()
    if num_key[pg.K_1] == True: n = 1
    if num_key[pg.K_2] == True: n = 2
    if num_key[pg.K_3] == True: n = 3
    if num_key[pg.K_4] == True: n = 4
    if num_key[pg.K_5] == True: n = 5
    if num_key[pg.K_6] == True: n = 6
    if num_key[pg.K_7] == True: n = 7
    if num_key[pg.K_8] == True: n = 8
    if num_key[pg.K_9] == True: n = 9

    for _ in range(n):
        bmimg_sfc = pg.Surface((20, 20))
        bmimg_sfc.set_colorkey(0)
        pg.draw.circle(bmimg_sfc, (255, 0, 0), (10, 10), 10)
        bmimg_rct = bmimg_sfc.get_rect()
        bmimg_rct.centerx = random.randint(0, screen_rct.width)
        bmimg_rct.centery = random.randint(0, screen_rct.height)
        
    while True:
            screen_sfc.blit(bgimg_sfc, bgimg_rct)
            
            for event in pg.event.get():
                if event.type == pg.QUIT: return
            
            key_states = pg.key.get_pressed() #辞書
            if key_states[pg.K_UP] == True: kkimg_rct.centery -= 1
            if key_states[pg.K_DOWN] == True: kkimg_rct.centery += 1
            if key_states[pg.K_LEFT] == True: kkimg_rct.centerx -= 1
            if key_states[pg.K_RIGHT] == True: kkimg_rct.centerx += 1
            if check_bound(kkimg_rct, screen_rct) != (1,1):
                if key_states[pg.K_UP] == True: kkimg_rct.centery += 1
                if key_states[pg.K_DOWN] == True: kkimg_rct.centery -= 1
                if key_states[pg.K_LEFT] == True: kkimg_rct.centerx += 1
                if key_states[pg.K_RIGHT] == True: kkimg_rct.centerx -= 1
            
            screen_sfc.blit(kkimg_sfc, kkimg_rct)
            bmimg_rct.move_ip(vx,vy)
            screen_sfc.blit(bmimg_sfc, bmimg_rct)
            
            yoko, tate =  check_bound(bmimg_rct, screen_rct)
            
            vx *= yoko
            vy *= tate
            if yoko == 1 and tate == -1:
                vx += 0.5
                vy -= 0.5
            if yoko == -1 and tate == 1:
                vy += 0.5
                vx -= 0.5
                    
            
            if kkimg_rct.colliderect(bmimg_rct):
                tkm.showwarning("^^","gameover")
                return
              
            pg.display.update()
            clock.tick(1000)


def check_bound(rct, scr_rct):
    yoko, tate = +1, +1 #領域内
    if rct.left < scr_rct.left or scr_rct.right < rct.right: yoko *= -1.3
    if rct.top < scr_rct.top or scr_rct.bottom < rct.bottom: tate *= -1.3
    return yoko, tate
    
    
if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()