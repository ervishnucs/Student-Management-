def flames_game(name1, name2):
    name1 = name1.replace(" ", "").lower()
    name2 = name2.replace(" ", "").lower()

    name1_list = list(name1)
    name2_list = list(name2)

    
    for ch in name1[:]:
        if ch in name2_list:
            name1_list.remove(ch)
            name2_list.remove(ch)

    count = len(name1_list) + len(name2_list)

    flames = ["Friends", "Love", "Affection", "Marriage", "Enemy", "Siblings"]

    while len(flames) > 1:
        
        for _ in range(count - 1):
            flames.append(flames.pop(0))
        
        flames.pop(0)

    return flames[0]


result = flames_game("Vishnupriya", "kishorekumar")
print("Result:", result)
