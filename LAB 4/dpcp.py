# # import copy

# # mylst = [
# #   [1,2,3],
# #   [2,3,4,],
# #   [5,6,7]

# # ]
# # mylst2 = copy.deepcopy(mylst)
# # mylst3 = copy.copy(mylst)

# # print(mylst)
# # print(mylst2)
# # print(mylst3)
# # mylst2[1][2] = 100
# # print(mylst[1][2])
# # print(mylst2[1][2])

# # mylst3[1][2] = 10000000
# # print(mylst[1][2])
# # print(mylst3[1][2])
# # print(mylst)
# # print(mylst2)
# # print(mylst3)



# import math
# y = math.factorial(9)
# import time
# lst = [[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']]
# start = time.time()

# for i in range(y):
#   a = TicTacToe_Grid_State(lst)

# print(time.time() - start)

import random
import copy
class Cell():
    def __init__(self):
        self.location=0
        self.mark=' '
flag=0
count=0
def print_grid(grid):
    global flag
    for i in range(6):
        for j in range(6):
            if i==0 or j==0:
                continue
            if i%2==0:
                if j%2==0:
                    print('+',end='')
                else: print('-',end='')
            else:
                if j%2==0:
                    print('|',end='')
                else:
                    if(flag==0):
                        print(grid[int((i+1)/2-1)][int((j+1)/2-1)].location,end='')
                        if i+j==10:
                            print()
                            flag=1
                            return
                    else:
                        print(grid[int((i+1)/2-1)][int((j+1)/2-1)].mark,end='')                      
        print()
    
def utility(grid):
    
    if grid[correct_pos(1)[0]][correct_pos(1)[1]].mark=='O' and grid[correct_pos(2)[0]][correct_pos(2)[1]].mark=='O' and grid[correct_pos(3)[0]][correct_pos(3)[1]].mark=='O':
        return -1
    if grid[correct_pos(1)[0]][correct_pos(1)[1]].mark=='O' and grid[correct_pos(4)[0]][correct_pos(4)[1]].mark=='O' and grid[correct_pos(7)[0]][correct_pos(7)[1]].mark=='O':
        return -1
    if grid[correct_pos(1)[0]][correct_pos(1)[1]].mark=='O' and grid[correct_pos(5)[0]][correct_pos(5)[1]].mark=='O' and grid[correct_pos(9)[0]][correct_pos(9)[1]].mark=='O':
        return -1
    if grid[correct_pos(3)[0]][correct_pos(3)[1]].mark=='O' and grid[correct_pos(5)[0]][correct_pos(5)[1]].mark=='O' and grid[correct_pos(7)[0]][correct_pos(7)[1]].mark=='O':
        return -1
    if grid[correct_pos(7)[0]][correct_pos(7)[1]].mark=='O' and grid[correct_pos(8)[0]][correct_pos(8)[1]].mark=='O' and grid[correct_pos(9)[0]][correct_pos(9)[1]].mark=='O':
        return -1
    if grid[correct_pos(3)[0]][correct_pos(3)[1]].mark=='O' and grid[correct_pos(6)[0]][correct_pos(6)[1]].mark=='O' and grid[correct_pos(9)[0]][correct_pos(9)[1]].mark=='O':
        return -1
    if grid[correct_pos(2)[0]][correct_pos(2)[1]].mark=='O' and grid[correct_pos(5)[0]][correct_pos(5)[1]].mark=='O' and grid[correct_pos(8)[0]][correct_pos(8)[1]].mark=='O':
        return -1
    if grid[correct_pos(4)[0]][correct_pos(4)[1]].mark=='O' and grid[correct_pos(5)[0]][correct_pos(5)[1]].mark=='O' and grid[correct_pos(6)[0]][correct_pos(6)[1]].mark=='O':
        return -1
   
    if grid[correct_pos(1)[0]][correct_pos(1)[1]].mark=='X' and grid[correct_pos(2)[0]][correct_pos(2)[1]].mark=='X' and grid[correct_pos(3)[0]][correct_pos(3)[1]].mark=='X':
        return 1
    if grid[correct_pos(1)[0]][correct_pos(1)[1]].mark=='X' and grid[correct_pos(4)[0]][correct_pos(4)[1]].mark=='X' and grid[correct_pos(7)[0]][correct_pos(7)[1]].mark=='X':
        return 1
    if grid[correct_pos(1)[0]][correct_pos(1)[1]].mark=='X' and grid[correct_pos(5)[0]][correct_pos(5)[1]].mark=='X' and grid[correct_pos(9)[0]][correct_pos(9)[1]].mark=='X':
        return 1
    if grid[correct_pos(3)[0]][correct_pos(3)[1]].mark=='X' and grid[correct_pos(5)[0]][correct_pos(5)[1]].mark=='X' and grid[correct_pos(7)[0]][correct_pos(7)[1]].mark=='X':
        return 1
    if grid[correct_pos(7)[0]][correct_pos(7)[1]].mark=='X' and grid[correct_pos(8)[0]][correct_pos(8)[1]].mark=='X' and grid[correct_pos(9)[0]][correct_pos(9)[1]].mark=='X':
        return 1
    if grid[correct_pos(3)[0]][correct_pos(3)[1]].mark=='X' and grid[correct_pos(6)[0]][correct_pos(6)[1]].mark=='X' and grid[correct_pos(9)[0]][correct_pos(9)[1]].mark=='X':
        return 1
    if grid[correct_pos(2)[0]][correct_pos(2)[1]].mark=='X' and grid[correct_pos(5)[0]][correct_pos(5)[1]].mark=='X' and grid[correct_pos(8)[0]][correct_pos(8)[1]].mark=='X':
        return 1
    if grid[correct_pos(4)[0]][correct_pos(4)[1]].mark=='X' and grid[correct_pos(5)[0]][correct_pos(5)[1]].mark=='X' and grid[correct_pos(6)[0]][correct_pos(6)[1]].mark=='X':
        return 1
   
    else:
        return 0
    
    
   
   
   
def start():
    grid=[]
    count=1
    for i in range(3):
        grid.append([])
    for i in range(3):
        for j in range(3):
            c=Cell()
            c.location=count
            count+=1
            grid[i].append(c)
   
    return play(grid)
def correct_pos(n):
    corr_pos=[[2,2]]
    for i in range(3):
        for j in range(3):
            corr_pos.append([i,j])
    return corr_pos[n]
def play(grid):
    
    
    print("The board locations are as follows:")
    print_grid(grid)
   

    for i in range(9):
        if i%2==0:
            n=int(input("\nEnter position for 0 player \n"))
            if grid[correct_pos(n)[0]][correct_pos(n)[1]].mark=='O' or grid[correct_pos(n)[0]][correct_pos(n)[1]].mark=='X':
                print("Invalid input!  Try again!!")
                print(i)
                i=i-2
                print(i)
                continue
            grid[correct_pos(n)[0]][correct_pos(n)[1]].mark='O'
            print_grid(grid)

        else:
            
            print('========================\nThe AI has played:')
             
            grid=minimax_decision(grid)
            print_grid(grid)
           
            # unmarked_cells=[]
            # for i in range(3):
            #      for j in range(3):
            #          if grid[i][j].mark=='O' or grid[i][j].mark=='X':
            #              continue
            #          else:
            #              unmarked_cells.append([i,j])
            # random.shuffle(unmarked_cells)
            # for i in unmarked_cells:
            #     grid[i[0]][i[1]].mark='X'
            #     minimax_decision(grid)
            #     break
        
        
    
        if(not utility(grid)==0):
            break

    
    if utility(grid)==1:
        print("Player X wins")
       
    elif utility(grid)==-1:
        print("Player O wins")
   
    else:
        print("Draw")
    return grid
def minimax_decision(grid):
    unmarked_cells=[]
    for i in range(3):
            for j in range(3):
                if grid[i][j].mark=='O' or grid[i][j].mark=='X':
                    continue
                else:
                    unmarked_cells.append([i,j])
    #print(unmarked_cells)
    max=-100
    maxstate=[]
    for i in unmarked_cells:
        temp_grid=copy.deepcopy(grid)
        temp_grid[i[0]][i[1]].mark='X'
        current = min_value(temp_grid)
        # print(f'{unmarked_cells.index(i)/len(unmarked_cells)}')
        if(current>max):
            max=current
            maxstate=temp_grid
    return maxstate  

def max_value(grid):
    global count
    if terminal_test(grid):
        count+=1
        return utility(grid)
    v=-100
    unmarked_cells=[]
    for i in range(3):
            for j in range(3):
                if grid[i][j].mark=='O' or grid[i][j].mark=='X':
                    continue
                else:
                    unmarked_cells.append([i,j])
    for i in unmarked_cells:
        temp_grid=copy.deepcopy(grid)
        temp_grid[i[0]][i[1]].mark='X'
        current=min_value(temp_grid)
        if(current>v):
            v=current
    #print(f"Max value = {v}")

    return v

def min_value(grid):
    global count
    #print_grid(grid)
    if terminal_test(grid): 
        count+=1
        #print("True")
        return utility(grid)
    v=100
    unmarked_cells=[]
    for i in range(3):
            for j in range(3):
                if grid[i][j].mark=='O' or grid[i][j].mark=='X':
                    continue
                else:
                    unmarked_cells.append([i,j])
    for i in unmarked_cells:
        temp_grid=copy.deepcopy(grid)
        temp_grid[i[0]][i[1]].mark='O'
        current=max_value(temp_grid)
        if(current<v):
            v=current
    #print(f"Min value = {v}")
    return v


def terminal_test(grid):
    if utility(grid)==1:
        return True
    elif utility(grid)==-1:
        return True
    for i in range(3):
        for j in range(3):
            if grid[i][j].mark==' ':
                return False
            else:
                continue
    return True
    

leaf = start()
print(count)
# def fact(n):
#     pdt=1
#     for i in range(1,n+1,1):
#         pdt=pdt*i
#     return(pdt)

# import time
# start_time = time.time()
# utility(leaf)
# print("--- %s seconds --- for utility()" % ((time.time() - start_time)*count))

