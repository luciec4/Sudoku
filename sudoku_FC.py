def main():    
    import numpy as np
    import time
    import Grids_Sudokus as gs

    t1=time.perf_counter()

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

    def change_domains(i,j,current,replace):
        #current = the current value that need to be replaced by the value "replace" in the domains array
        #erase/fill again this solution in the domains of all cells related to this one

        #on the column
        for line in range(9):
            if line != i and (sol[line,j]==0 or sol[line,j]!=grid[line,j]): #only if it's an unfixed variable    
                if current==0 and check_line(line,j,replace) and check_square(line,j,replace):
                    domains[line,j,0]=replace
                if current!=0:
                    spot=np.where(domains[line,j]==current)[0]
                    domains[line,j,spot]=replace
                domains[line,j].sort()

        #on the line
        for col in range(9):
            if col != j and (sol[i,col]==0 or sol[i,col]!=grid[i,col]): #only if it's an unfixed variable
                if current==0 and check_column(i,col,replace) and check_square(i,col,replace):
                    domains[i,col,0]=replace
                if current!=0:
                    spot=np.where(domains[i,col]==current)[0]
                    domains[i,col,spot]=replace
                domains[i,col].sort()

        #in the square (2x2 because the line and column are already changed)

        line=3*(i//3) #line index of the square
        col=3*(j//3) #column index of the square
        for k in range(3):
            for l in range(3):
                if line+k!=i and col+l!=j and (sol[line+k,col+l]==0 or sol[line+k,col+l]!=grid[line+k,col+l]): #only if it's an unfixed variable):
                    if current==0 and check_line(line+k,col+l,replace) and check_column(line+k,col+l,replace):
                        domains[line+k,col+l,0]=replace
                    if current!=0:
                        spot=np.where(domains[line+k,col+l]==current)[0]
                        domains[line+k,col+l,spot]=replace
                    domains[line+k,col+l].sort()


    def solve(i,j):
        if check_square(i,j,sol[i,j]) and check_line(i,j,sol[i,j]) and check_column(i,j,sol[i,j]):
            change_domains(i,j,sol[i,j],0)
            return True
        else:
            after=domains[i,j,np.where(domains[i,j] == sol[i,j])[0]-1]
            if after==0 or sol[i,j]==1:
                return False
            else:       
                sol[i,j]=after
                return solve(i,j)    



    def backtrack(a,b):
        if sol[a,b]!=grid[a,b]:
            sol[a,b]=0
            
        else:
            if a==0 and b==0:
                print("--This sudoku is not solvable!!")
                return[9,9]
        
        if b==0:
            b=8
            a-=1
        else:
            b-=1
        if sol[a,b]==grid[a,b]:
            return backtrack(a,b)
        elif domains[a,b,np.where(domains[a,b] == sol[a,b])[0]-1]==0 or sol[a,b]==1:
            keep=sol[a,b]
            sol[a,b]=0
            change_domains(a,b,0,keep)
            return backtrack(a,b)
        else:
            return [a,b]    



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

    #initiate the array "domains" with the domain of each cell at the begining 
    for i in range(9):
        for j in range(9):
            #if this cell is empty for now, it is an unfixed cell -> domain = [1-9]
            if sol[i,j]==0:
                domains[i,j,:]=np.array([1,2,3,4,5,6,7,8,9])
            
            #fixed cells
            else:
                domains[i,j,:]=np.array([sol[i,j],sol[i,j],sol[i,j],sol[i,j],sol[i,j],sol[i,j],sol[i,j],sol[i,j],sol[i,j]])


    #quick checking of the initial grid
    # + change the cells' domains depending on the fixed ones
    for i in range(9):
        for j in range(9):
            if not(check_square(i,j,sol[i,j])) or not(check_line(i,j,sol[i,j])) or not(check_column(i,j,sol[i,j])):
                print("The initial grid has conflicts. The sudoku is not solvable")
                return
            
            if grid[i,j]!=0:
                change_domains(i,j,grid[i,j],0) 


    i=0
    j=0

    #actual algorithm
    while i<9:
        #column
        while j<9:
            #if the cell is "empty", fill it with the last value in its domain
            if sol[i,j]==0:
                sol[i,j]=domains[i,j,8]
            
            #if this number is fixed, don't change it
            if sol[i,j]==grid[i,j] and sol[i,j]!=0: 
                j+=1
            #if it's unfixed:
            else:
                if sol[i,j]==0:
                    a=backtrack(i,j)
                    i=a[0]
                    j=a[1]
                    keep=sol[i,j]
                    sol[i,j]=domains[i,j,np.where(domains[i,j] == sol[i,j])[0]-1]
                    change_domains(i,j,0,keep)

                elif solve(i,j):
                    j+=1
                
                else:
                    if j==0 and i==0:
                        print("This sudoku is not solvable!!")
                        j=9
                        i=9
                    else:
                        a=backtrack(i,j)
                        i=a[0]
                        j=a[1]
                        keep=sol[i,j]
                        sol[i,j]=domains[i,j,np.where(domains[i,j] == sol[i,j])[0]-1]
                        change_domains(i,j,0,keep)
        i+=1  
        j=0   
    print("here is the solution:")
    print()
    print(sol)
    t2=time.perf_counter()
    print()
    print("Time needed: ",t2-t1," sec")

if __name__ == "__main__":
    main()