

def gp(word):
    word_list = []
    if len(word) == 1: 
            return word, word_list.append(word) 
    else: 
        for x in word:
            for i in range(len(word)):       
                rest = gp(word[:i] + word[i+1:])[0]
                # print(rest)
                start = x
                final = start + rest
                word_list.append(final)
        return final, word_list
        

if __name__ == '__main__':
    word = 'wanghao'
    # word = 'zhengfanli'
    print(gp(word))[1]