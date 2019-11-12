from Visualizing_Patterns import Read_Compacted_Solution

class Single_Rule_Test:
    def __init__(self,population_test,paradigm,problem_Id,problem_length):
        print("Start")
        Compare_RCS = Read_Compacted_Solution(population_test)
        Compare_solution=Compare_RCS.population