def main():    
    import numpy as np
    import time
    import Grids_Sudokus as gs

    t1=time.perf_counter()

    def check_square(i,j):
        #line index of the square
        line=3*(i//3)
        #column index of the square
        col=3*(j//3)
        for k in range(3):
            for l in range(3):
                if (line+k)!=i or (col+l)!=j:
                    if sol[i,j]==sol[(line+k),(col+l)]  and sol[i,j]!=0:
                        return False
        return True

    def check_line(i,j):
        for k in range(9):
            if k!=j and sol[i,j]==sol[i,k] and sol[i,j]!=0:
                return False
        return True

    def check_column(i,j):
        for k in range(9):
            if k!=i and sol[i,j]==sol[k,j]  and sol[i,j]!=0:
                return False
        return True       

    def solve(i,j):
        if check_square(i,j) and check_line(i,j) and check_column(i,j):
            return True
        else:
            if sol[i,j]==9:
                return False
            else:        
                sol[i,j]+=1
                return solve(i,j)    



    def backtrack(a,b):
        if sol[a,b]!=grid[a,b]:
            sol[a,b]=0
        else:
            if a==0 and b==0:
                print("This sudoku is not solvable!!")
                return[9,9]
        if b==0:
            b=8
            a-=1
        else:
            b-=1

        if sol[a,b]==grid[a,b]:
            return backtrack(a,b)
        elif sol[a,b]==9:
            return backtrack(a,b)
        else:
            return [a,b]        
            

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

    #quick checking of the initial grid
    for i in range(9):
        for j in range(9):
            if not(check_square(i,j)) or not(check_line(i,j)) or not(check_column(i,j)):
                print("The initial grid has conflicts. The sudoku is not solvable")
                return

    i=0
    j=0
    #line
    while i<9:
        #column
        while j<9:
            
            if sol[i,j]==0:#if the cell is "empty", fill it with 1
                sol[i,j]=1
            
            
            if sol[i,j]==grid[i,j]: #if this number is fixed, don't change it
                j+=1
            
            else:#if it's a "normal case":
                if solve(i,j):
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
                        sol[i,j]+=1
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