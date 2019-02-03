

def gp(word):
    word_list = []
    if len(word) == 1: 
            return word 
    else: 
        for x in word:
            for i in range(len(word)):       
                rest = word[:i] + word[i+1:]
                # print(rest)
                start = x
                final = start + rest
                print(final)
        # print(word_list)
  
    #         word_list.append(final)
    # return word_list
        

if __name__ == '__main__':
    # word = 'wanghaohan'
    word = 'zhengfanli'
    print(gp(word))