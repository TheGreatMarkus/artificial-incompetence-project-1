import numpy as np

#open and read the file
with open('test.txt') as f:
    file_data = f.read()

inputs = file_data.split("\n")


#check if goal is met
def winCheck(state):
    if np.array_equal(state, goalArr):
        return True
    return False

#flip the peg to opposite value
def flip(x):
    if(x == 1):
        return 0
    return 1




   
#implementation of dfs 
def dfs(maxd, state, p):
    if winCheck(state):
        p.append(stringVal(state))
        return state
    
    if maxd == 0:
        return 
    
    if stringVal(state) in states:
        return 
    for i in range (len(state)):
        for j in range (len(state[i])):
            
            states.add(stringVal(state))
            
            
            if state[i][j] == 1:
                p.append(stringVal(state))
                dfs(maxd-1, move(i, j, state),p)
                if stringVal(goalArr) in p:
                    return p
                else:
                        p.pop()
            
                
    return p

#turns matrix to a string to add to states set        
def stringVal(matrix):
    s = ""
    for i in range (len(matrix)):
        for j in range (len(matrix[i])):
              s = s + str(matrix[i][j])
              
    return s
        
        

#moves each piece related to a single mobvement
def move(xSpot, ySpot, arr):
    arr[xSpot][ySpot] = flip(arr[xSpot][ySpot])
    if xSpot-1 >= 0:
        arr[xSpot-1][ySpot] = flip(arr[xSpot-1][ySpot])
       
        
    if xSpot+1 < size :
        arr[xSpot+1][ySpot] = flip(arr[xSpot+1][ySpot])
        
    if ySpot-1 >= 0:
        arr[xSpot][ySpot-1] = flip(arr[xSpot][ySpot-1])
        
        
    if ySpot+1 < size :
        arr[xSpot][ySpot+1] = flip(arr[xSpot][ySpot+1])
    
    return arr
        
        


#loop through each of the file input rows.
for row in inputs:
    if row == "":
        break;
    #initilize the values from the read file
    values = row.split(" ")
    size = int(values[0])
    maxd = int(values[1]) #the max depth for dfs
    maxl = int(values[2]) #the max depth for bfs and A*
    board = values[3]
    x = 0
    y = 0
    states = set()
    path = []
    #declare the goal board based on size
    goal = '0' * board.__len__()
    goalArr = []
    for i in goal:
        goalArr.append(int(i))
    goalArr = np.array(goalArr)
    goalArr = np.reshape(goalArr, (size, size))
    boardArr = []

    #turn the string into an array.
    for i in board:
        boardArr.append(int(i))
        
    #create a matrix with the board
    boardArr = np.array(boardArr)
    boardArr = np.reshape(boardArr, (size, size))
    print(maxd)
    print("start board: \n" , boardArr, "\n\n")
    print(dfs(maxd, boardArr, path))
  # print("\n\n", states)
    
   


