from random import randint
taisyo = 6
kesson = 3
kurikaesi = 5

def main():
    lst = setting()
    kaitou(lst)

def setting():
    s_list = []
    all_alp = list(map(chr, range(97, 123)))
    for i in range(taisyo):
        j = randint(0,len(all_alp))
        s_list.append(all_alp.pop(j))
    print(f"対象文字:{s_list}")
    return s_list

def kaitou(lst):
    global kurikaesi
    kesson_list = []
    for i in range(kesson):
        j = randint(0,len(lst))
        print(j)
        kesson_list.append(lst.pop(j))
    print(lst)
    
    a=input("欠損文字はいくつあるでしょうか？")
    if a==kesson:
        print("正解です。それでは具体的に欠損文字を入力してください。")
        for l in range(kesson):
            ans=input(f"{l}文字目を入力してください")
            if ans in kesson_list:
                kesson_list.remove(ans)
            else:
                ("不正解です。またチャレンジしてください。")
                if  kurikaesi > 0:
                    main()
        print("正解です！おめでとうございます。")
    else:
        print("不正解です。またチャレンジしてください。")
        if  kurikaesi > 0:
            kurikaesi -= 1
            main()
            
if __name__ == "__main__":
    main()