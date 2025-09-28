# Table of Contents

1. [PROJECT_OVERVIEW]
2. [PROBLEM_STATEMENT]
3. [FUNCTIONAL_REQUIREMENTS]
4. [TECHNICAL_REQUIREMENTS]
5. [DEVELOPMENT_PLAN]

# PROJECT OVERVIEW :

- PROJECT NAME : `BudgetFlow`
- PROGRAMMING LANGUAGE : `Python`
- GOAL : `To create an expense tracker where a user can input their expenses & categorize them (e.g. food, entertainment, trasnport ...) and the tracker will calculate the total spent on each category and display them on a bar chart.`

# PROBLEM STATEMENT :

- PROBLEM DESCRIPTION : `Users need to be able to track their expenses easily, creating an expense tracker that can take in as many expenses as the user would to put in and calculate how much is spent on each category would make it easier for the user to manage their finances.`

- DESIRED OUTCOME : `The tracker should return a bar chart of all the categories and the amount spent on each.`

# FUNCTIONAL REQUIREMENTS :

- FEATURES : ` ~ Take in user input.`
             ` ~ Categorize each expense.`
             ` ~ Categorize each expense.`
             ` ~ Add together the amount of each expense for each category.`
             ` ~ Put each category on a bar chart.`

- INPUT : `An expense, it's amount and it's category.`

- OUTPUT : ` A graph that represents each catergory of the expense and the amount spent on each.`

# TECHNICAL REQUIREMENTS :

- Variables, data types (integer, float, string, list, dictionary)
- Functions (custom and built-in functions like input(), print())
- Operators (arithmetic, comparison, logical)
- Conditional statements (if-else), loops (for, while)
- Working with lists, dictionaries, and basic user input
- Python packages (use matplotlib for visualizing expenses)

# DEVELOPMENT PLAN :

_TODO:_

## STEP 1:
Use the input() function to take in user input(expenses) and create options of the categories for the user to choose from after each expense.
I can prompt the user to input data 3 times(1 for the expense, 2 for the amount, 3 for the category) 
The amount needs to be a floating point number to account for decimals
Use a while loop to control the flow of the tracker to allow the user to put in as many expenses as they see fit.


## STEP 2:

Could have a nested dictionary where the category is the key and the expenses are the keys of each nested category and their amounts as the values. 
If the user chooses a certain category, the expense gets put in a dictionary as the key and it's amount as the value. 

### EXAMPLE:
 ```python
Expenses ={"Food" :{"pizza":50, "chocolate": 5}, "Entertainment" :{"Netflix": 250}, "Transport" : {"Uber": 50}} 
```
## STEP 3:
Add all the amounts of the expenses in each category.

## STEP 4:
Use the matplotlib library to plot the graph using the totals of each category then save the graph as a picture(png).





