list = []
 
def gp(word):
    for idx, x in enumerate(word):
        start = x
        rest = gp(word[:idx] + word[idx + 1:])
        if rest == None:
            rest = x 
        final = start + rest
        print("Iteration # ", idx)
        print(final)
        list.append(final)
        return list
        
    print(list)

if __name__ == "__main__":
    gp("word")
        