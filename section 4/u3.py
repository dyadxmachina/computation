
print("looping like crazy")

def gp(s):
   if len(s) == 1:
     return [s]

   perm_list = [] # resulting list
   
   for a in s:
     remaining_elements = [x for x in s if x != a]
     z = gp(remaining_elements) # permutations of sublist

     for t in z:
       perm_list.append([a] + t)

   return(perm_list)

print(gp("me"))