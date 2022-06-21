from logging import root
import tkinter as tk
import tkinter.messagebox as tkm

 
def button_click(event):
    btn = event.widget
    num = btn["text"]#クリックされたボタンの文字
    
    if num == "=":
        eqn = entry.get()
        res = eval(eqn)
        entry.delete(0,tk.END)
        entry.insert(tk.END,res)
        
    elif num == "C":
        entry.delete(0,tk.END)
        
    elif num == "2進数":
        eq = int(entry.get())
        entry.delete(0,tk.END)
        a = format(eq,"b")
        entry.insert(tk.END,a)
        
    elif num == "8進数":
        eq = int(entry.get())
        entry.delete(0,tk.END)
        a = format(eq,"o")
        entry.insert(tk.END,a)
        
    elif num == "16進数":
        eq = int(entry.get())
        entry.delete(0,tk.END)
        a = format(eq,"x")
        entry.insert(tk.END,a)
                
    else:  
        entry.insert(tk.END,num)
    
    
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x700")
    root.title("電卓")
    
    entry = tk.Entry(root,
                     justify="right",
                     width=10,
                     font=("Times New Roman",40)
                     )
    entry.grid(row=0,column=0,columnspan=3)
    
    r,c=1,0
    for i,num in enumerate(["2進数","8進数","16進数","C",
                            9,8,7,"/",
                            6,5,4,"*",
                            3,2,1,"-",
                            0,"","=","+",]
                           ):
        
        btn = tk.Button(root,
                        text=f"{num}",
                        width=5,
                        height=1,
                        font=("Times New Roman",30)
                        )
        btn.bind("<1>",button_click)
        btn.grid(row=r,column=c)
        c+=1
        if (i+1)%4==0:
            r+=1
            c=0
    root.mainloop()