def main():    
    import numpy as np
    import time
    import Grids_Sudokus as gs

    def check_square(i,j,value):
        #line index of the square
        line=3*(i//3)
        #column index of the square
        col=3*(j//3)
        for k in range(3):
            for l in range(3):
                if (line+k)!=i or (col+l)!=j:
                    if value==sol[(line+k),(col+l)]  and value!=0:
                        return False
        return True

    def check_line(i,j,value):
        for k in range(9):
            if k!=j and value==sol[i,k] and value!=0:
                return False
        return True

    def check_column(i,j,value):
        for k in range(9):
            if k!=i and value==sol[k,j]  and value!=0:
                return False
        return True       

    def change_domains(i,j,current):
        #current = the current value that need to be replaced by the value "replace" in the domains array
        #erase/fill again this solution in the domains of all cells related to this one

        #on the column
        for line in range(9):
            if line != i and (sol[line,j]==0 or sol[line,j]!=grid[line,j]): #only if it's an unfixed variable    
                domains[line,j,np.where(domains[line,j]==current)[0]]=0
                domains[line,j].sort()
                lcv(line,j)

        #on the line
        for col in range(9):
            if col != j and (sol[i,col]==0 or sol[i,col]!=grid[i,col]): #only if it's an unfixed variable
                domains[i,col,np.where(domains[i,col]==current)[0]]=0
                domains[i,col].sort()
                lcv(i,col)

        #in the square (2x2 because the line and column are already changed)

        line=3*(i//3) #line index of the square
        col=3*(j//3) #column index of the square
        for k in range(3):
            for l in range(3):
                if line+k!=i and col+l!=j and (sol[line+k,col+l]==0 or sol[line+k,col+l]!=grid[line+k,col+l]): 
                #only if it's an unfixed variable)
                    domains[line+k,col+l,np.where(domains[line+k,col+l]==current)[0]]=0
                    domains[line+k,col+l].sort()
                    lcv(line+k,col+l)


    def solve(i,j):
        if check_square(i,j,sol[i,j]) and check_line(i,j,sol[i,j]) and check_column(i,j,sol[i,j]):
            change_domains(i,j,sol[i,j])
            return True
        else:
            after=domains[i,j,np.where(domains[i,j] == sol[i,j])[0]-1]
            if after==0 or sol[i,j]==1:
                return False
            else:       
                sol[i,j]=after
                return solve(i,j)    


    def backtrack(w):
        i=history_w[w,0]
        j=history_w[w,1]
        if sol[i,j]==grid[i,j]:
            return backtrack(w-1)
        else:

            if history_domains[w-1,i,j,np.where(domains[i,j] == sol[i,j])[0]-1]==0 or history_sol[w,i,j]==1:
                return backtrack(w-1)
            else:
                return w   


    def mcv(w): #most constrained variable
        keep=0
        constrained=0
        after=np.array([0,0])
        #finding the most constrained variable
        for i in range(9):
            for j in range(9):
                if sol[i,j]==0:    
                    keep=constrained
                    constrained=len(np.where(domains[i,j]==0)[0])
                    if keep>constrained: #more 0 before
                        constrained=keep
                    else: #more 0 now
                        after=[i,j]
        return after
    

    def lcv(i,j): # order the domain with the least constraining value first
        dtype=[('number',int),('weight',int)]
        length=9-len(np.where(domains[i,j]==0)[0])
        table=np.zeros((length), dtype=dtype)
        
        for a in range(length):     
            appear=0
            b=8-a
            #on the column
            for line in range(9):
                if line != i and (sol[line,j]==0 or sol[line,j]!=grid[line,j]): #only if it's an unfixed variable    
                    if len(np.where(domains[line,j]==domains[i,j,b])[0])!=0:
                        appear+=1

            #on the line
            for col in range(9):
                if col != j and (sol[i,col]==0 or sol[i,col]!=grid[i,col]): #only if it's an unfixed variable
                    if len(np.where(domains[i,col]==domains[i,j,b])[0])!=0:
                        appear+=1

            #in the square (2x2 because the line and column are already changed)

            line=3*(i//3) #line index of the square
            col=3*(j//3) #column index of the square
            for k in range(3):
                for l in range(3):
                    if line+k!=i and col+l!=j and (sol[line+k,col+l]==0 or sol[line+k,col+l]!=grid[line+k,col+l]): 
                    #only if it's an unfixed variable)
                        if len(np.where(domains[line+k,col+l]==domains[i,j,b])[0])!=0:
                            appear+=1

            table[a]=(domains[i,j,b],appear)
        
        table.sort(order='weight')

        for a in range(length):
            b=8-a
            domains[i,j,b]=table[a]['number']


        




    #array of all possible values for each cell
    domains=np.zeros((9,9,9), dtype=int)


    print()
    num=input("Enter a number between 1 and 10 to select the sudoku you want to resolve: ")
    print()
    print()
    t1=time.perf_counter()
    index=int(num)-1
    if index in range(10):
        grid=np.copy(gs.grids[index])
    else:
        print("please run the program again and give an integer between 1 and 10 (included)")
        return


    sol=np.copy(grid)

    given=0
    #initiate the array "domains" with the domain of each cell at the begining 
    for i in range(9):
        for j in range(9):
            #if this cell is empty for now, it is an unfixed cell -> domain = [1-9]
            if sol[i,j]==0:
                domains[i,j,:]=np.array([1,2,3,4,5,6,7,8,9])
            
            #fixed cells
            else:
                domains[i,j,:]=np.array([sol[i,j],sol[i,j],sol[i,j],sol[i,j],sol[i,j],sol[i,j],sol[i,j],sol[i,j],sol[i,j]])
                given+=1


    #quick checking of the initial grid
    # + change the cells' domains depending on the fixed ones
    for i in range(9):
        for j in range(9):
            if not(check_square(i,j,sol[i,j])) or not(check_line(i,j,sol[i,j])) or not(check_column(i,j,sol[i,j])):
                print("The initial grid has conflicts. The sudoku is not solvable")
                return
            
            if grid[i,j]!=0:
                change_domains(i,j,grid[i,j]) 



    history_sol=np.zeros((81-given+1,9,9), dtype=int)
    history_domains=np.zeros((81-given+1,9,9,9), dtype=int)
    history_w=np.zeros((81-given+1,2), dtype=int)

    history_sol[0]=sol
    history_domains[0]=domains

    i=0
    j=0
    w=0
    history_w[0]=mcv(w)

    #actual algorithm
    while w<(81-given):
        i=history_w[w][0]
        j=history_w[w][1]
        #if the cell is "empty", fill it with the last value in its domain
        if sol[i,j]==0:
            sol[i,j]=domains[i,j,8]
        
        #if this number is fixed, don't change it
        if sol[i,j]==grid[i,j] and sol[i,j]!=0: 
            j+=1
        #if it's unfixed:
        else:
            if sol[i,j]==0:
                w-=1
                if w<0:
                    print("--This sudoku is not solvable!!")
                    return
                w=backtrack(w)
                
                i=history_w[w,0]
                j=history_w[w,1]
                sol=history_sol[w] # takes the solution after the cell was fixed
                domains=history_domains[w-1] # takes the domain before the cell was fixed
                sol[i,j]=domains[i,j,np.where(domains[i,j] == sol[i,j])[0]-1] # change the solution
            
            elif solve(i,j):
                history_sol[w]=sol
                history_domains[w]=domains
                for a in range(9):
                    domains[i,j,a]=(a+1) #its domain has to be full so that we don't pick this one twice 
                w+=1
                history_w[w]=mcv(w)
            
            else:
                if w==0:
                    print("This sudoku is not solvable!!")
                    return
                else:
                    w-=1
                    w=backtrack(w)
                    i=history_w[w,0]
                    j=history_w[w,1]
                    sol=history_sol[w]#takes the solution after the cell was fixed
                    domains=history_domains[w-1]
                    sol[i,j]=domains[i,j,np.where(domains[i,j] == sol[i,j])[0]-1]#change the solution


    
    print("here is the solution:")
    print()
    print(sol)
    t2=time.perf_counter()
    print()
    print("Time needed: ",t2-t1," sec")


if __name__ == "__main__":
    main()