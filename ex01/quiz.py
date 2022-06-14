def shutudai():
    from random import randint
    q_list=["サザエの旦那の名前は？",
            "カツオの妹の名前は？",
            "タラオはカツオからみてどんな関係？"]
    a_list=[["ますお","マスオ"],
            ["わかめ","ワカメ"],
            ["おい","甥","甥っ子","おいっこ"]]
    r=randint(0,2)
    print(q_list[r])
    a=a_list[r]
    return a
        

def kaitou(seikai):
    ans=input("答えを入力してください→")
    if ans in seikai:
        print("正解！")
    else:
        print("不正解!")
    
seikai = shutudai()
kaitou(seikai)