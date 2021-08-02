import time
import numpy as np

clean_string = []
text_file = open("/home/rope/Desktop/Robot_Program/Programs/execute_script.txt",'r+')
code_string = text_file.readlines() # this is list where each index is one line of code. Each index needs to be aditionaly processed
code_len = len(code_string)
#data_split = code_string.split(b',')
#print(data_split)

text_file.close()
valid_data = 0

# data = [1,2,3,4,5,6,7]
# if __name__ == "__main__":

#     print("here")
#     for i in range(0,len(data)):
#         if data[i] != 5:
#             clean_string.append(data[i])
#         else:
#             continue
        
#         print(data[i])
#     print(clean_string)

if __name__ == "__main__":

    # this code cleans string data
    for i in range(0,code_len):
        if code_string[i] == '\n':
            continue
        else:
            clean_string.append(code_string[i])

    if clean_string[len(clean_string)-1] == 'end\n' or clean_string[len(clean_string)-1] == 'loop\n':
        valid_data = 1
    else:
        valid_data = 0

    #####

    print(valid_data)
    print(clean_string)

    code2execute = clean_string[0].split(',')
    code2execute = code2execute[:-1]
    if(code2execute[0] == 'pos'):
        print("1")
    elif(code2execute[0] == 'delay'):
        print("2")
    elif(code2execute[0] == 'end'):
        print("3")
    
    print(code2execute)

    #print(int('0.5\n'))

    a = [1, 2, 3, 4, 3]
    b = [9, 8, 7, 6, 5]
    if np.any(np.array(a)>np.array(b)):
        print("yes")
    else:
        print("no")

   # print(set(a) & set(b))



