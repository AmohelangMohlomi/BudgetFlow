import sys
import matplotlib
import matplotlib.pyplot as plt   
import numpy as np
matplotlib.use("TkAgg")


# Initialize nested dictionary
expenses = {"Food" :{}, "Entertainment" :{}, "Transport" : {}, "Housing" : {}, "Healthcare" : {} } 
# Initialize a list of all categories
categories = ["Food","Entertainment","Transport", "Housing","Healthcare"]


# Define a function to get the expense and it's amount
def get_expense(expense):
    
    expense_amount = 0
    expense_name =""
    for item in expense.split():
        if item.isdigit(): # .isdigit() does not account for floats
            expense_amount = float(item)
        else:
            expense_name = item
    return expense_name,expense_amount
       

# Define a function to display all the categories
def show_category():
    y = 1 
    for category in categories:
        print("{}) {} ".format(y,category))
        y+=1
 
# Define a function to control whether a user wants to add a function or not
def add_new_expense(add_expense):
    
    if add_expense.lower().startswith("y"):
        return True
    else:
        return False


# Define the main function that controls the flow of the expense tracker.
def main():
    food_total= 0
    entertainment_total= 0
    transport_total=0
    housing_total=0
    healthcare_total=0
    ask= True
    
    while ask:
        add_expense  = input("Do you want to add an expense? ")
        print(" ")
        print("-----------------------------------------")
        if add_new_expense(add_expense):
            
            expense = input("Enter expense and amount (e.g Pizza 30): ")
            print(" ")
            print("-----------------------------------------")
            expense_name,expense_amount= get_expense(expense)
            show_category()
            print(" ")
            print("-----------------------------------------")
            chosen_category=int(input("Which category? ")) 
            if chosen_category == 1:
                expenses["Food"][expense_name] = expense_amount
                food_total += expense_amount
            elif chosen_category == 2:
                expenses["Entertainment"][expense_name] = expense_amount
                entertainment_total += expense_amount
            elif chosen_category == 3:
                expenses["Transport"][expense_name] = expense_amount
                transport_total += expense_amount
            elif chosen_category == 4:
                expenses["Housing"][expense_name] = expense_amount
                housing_total += expense_amount
            elif chosen_category == 5:
                expenses["Healthcare"][expense_name] = expense_amount
                healthcare_total += expense_amount
        else:
            ask= False
            print(f"""Food total: {food_total} \n
Entertainment total: {entertainment_total} \n
Transport total: {transport_total} \n
Housing total: {housing_total} \n
Healthcare total: {healthcare_total}
                """)
            
# Assign the x and y coordinates for the bar graph
    x = np.array(["Food", "Entertainment", "Transport", "Housing", "Healthcare"])
    y = np.array([food_total, entertainment_total,transport_total,housing_total,healthcare_total])

# Plot the graph and save it as a picture
    plt.bar(x,y)
    plt.savefig("expenses_graph.png")

    plt.savefig(sys.stdout.buffer)
    sys.stdout.flush


          

if __name__ == "__main__":
    main()
            










    



















