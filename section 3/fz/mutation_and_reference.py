fl = "haohan"
hw = fl

print(hex(id(hw)))

import copy 

fl = {"haohan":1}
hw =  fl.copy()

fl['haohan'] = 2.0


print(fl)