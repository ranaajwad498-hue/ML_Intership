import numpy as np
children_array= np.array([])

class children_weight:
    def __init__(self,child1, child2, child3, child4, child5, child6, child7, child8, child9, child10):
        self.child1= child1
        self.child2= child2
        self.child3= child3
        self.child4= child4
        self.child5= child5
        self.child6= child6
        self.child7= child7
        self.child8= child8
        self.child9= child9
        self.child10=child10 



    def weight():
        global children_array
        print("    ---- Enter Children Weight ----")
        child1= float(input("Enter the Weight of Child1: "))
        child2= float(input("Enter the Weight of Child2: "))
        child3= float(input("Enter the Weight of Child3: "))
        child4= float(input("Enter the Weight of Child4: "))
        child5= float(input("Enter the Weight of Child5: "))
        child6= float(input("Enter the Weight of Child6: "))
        child7= float(input("Enter the Weight of Child7: "))
        child8= float(input("Enter the Weight of Child8: "))
        child9= float(input("Enter the Weight of Child9: "))
        child10=float(input("Enter the Weight of Child10: " ))

        children=children_weight(child1, child2, child3, child4, child5, child6, child7, child8, child9, child10)
    
        children_array = np.array([
            children.child1, children.child2, children.child3, children.child4, children.child5, children.child6, children.child7, children.child8, children.child9, children.child10
    ])
    

# --- display weight with 2 decimal places
    def display_weight():
        print("\n ----   CHILD WEIGHT ANALYSIS REPORT    -----\n") 
        print("Weight of ALL the Children: ", np.round(children_array,2))


#--- calculate_average
    def calculate_average():
        avg=np.mean(children_array)
        print("Average Weight of the Children: ",np.round(avg , 2))
        return avg

#---- minimum_weight
    def minimum_weight():
        mini= np.min(children_array)
        print("Minimum Weight of Children: ",np.round(mini , 2))
   
#---- maximum_weight
    def maximun_weight():
        maxi=  np.max(children_array)
        print("Maximun weight of the Children: ", np.round(maxi , 2))

#--- calculate_standard_deviation
    def calculate_standard_deviation():
        std= np.std(children_array)
        print("Standard Daviation of Weight: ",np.round(std , 2))

#--- calculate_total_weight
    def calculate_total_weight():
        total= np.sum(children_array)
        print("Total Weight of Children: ",np.round(total , 2) )

#--- calculate_median_weight()
    def calculate_median_weight():
        med= np.median(children_array)
        print("Median of Weight: ",np.round(med))

#--- count_children_above_average()
    def count_children_above_average():
        avg=np.average(children_array)
        print("Number Of Children whose Weight is Greator than Average: ",np.sum(children_array > avg))

          
children_weight.weight()
children_weight.display_weight()
children_weight.calculate_average()
children_weight.minimum_weight()
children_weight.maximun_weight()
children_weight.calculate_standard_deviation()
children_weight.calculate_total_weight()
children_weight.calculate_median_weight()
children_weight.count_children_above_average()



