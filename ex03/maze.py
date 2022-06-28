import tkinter as tk
import maze_maker as mm

def key_down(event):
    global key
    key = event.keysym
    #print(f"{key}が押されました")


def key_up(event):
    global key
    key = ""
   
    
def main_proc():
    global cx, cy, mx, my
    delta = { 
        ""     : [0,  0],
        "Up"   : [0, -1],
        "Down" : [0, +1],
        "Left" : [-1, 0],
        "Right": [+1, 0]      
    }
    if maze_bg[my+delta[key][1]][mx+delta[key][0]] == 0:
        my, mx = my+delta[key][1], mx+delta[key][0]
        canvas.create_rectangle(cx-50, cy-50, cx+50, cy+50, 
                                fill="blue" )#通った床を青に。
        print(mx,my,cx,cy)
        canvas.create_rectangle(100, 100, 100+100, 100+100, 
                                    fill="red")#スタート地点を赤に。
    
    cx,cy = mx*100+50, my*100+50
    canvas.coords("tori", cx, cy)    
    root.after(100, main_proc)

    
if __name__ == "__main__":
    root = tk.Tk()
    root.title("迷えるこうかとん")
    
    canvas = tk.Canvas(root, width=1500, height=900, bg="black")
    canvas.pack()
    maze_bg = mm.make_maze(15, 9) # 1:壁/2:床を表す二次元リスト
    mm.show_maze(canvas, maze_bg) 
    
    
    tori = tk.PhotoImage(file="fig/2.png")
    
    mx, my = 1, 1
    cx,cy = mx*100+50, my*100+50
    canvas.create_image(cx, cy, image=tori, tag="tori")
    
    key = ""
    root.bind("<KeyPress>",key_down)
    root.bind("<KeyRelease>",key_up)
    
    main_proc()
    root.mainloop()

