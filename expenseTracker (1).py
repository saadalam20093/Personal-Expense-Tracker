from datetime import date
import time,os

TodaysDate=date.today()
Date=TodaysDate.strftime("%Y-%m-%d")

reportPath="expenseReport.csv"
totalExpense="expenses.csv"
expenseBudget="budget.csv"

#Introduces the User
def intro():
    name=input("Enter your First Name: ")

    print(f"🎯Hi {name}! I am your Personal Expense Tracker😯")
    time.sleep(1)
    print("🎯 I will keep track all of your expenses for you and let you know how much money you saved up🫰💵\n")
    time.sleep(2)
    os.system('cls')

#Prompts the user for the budget and then write the budget to the list. 
def userBudget():
    while True:
        try:
            with open(expenseBudget, 'r+') as file:
                content1=file.read()
            if content1:
                budget=float(content1)
                
                break
            else:
                while True:
                    try:
                        budget=float(input("Enter your Budget for the Month💵: "))
                        print(f"Your Budget for the Month is ${budget}\n")
                        break
                    except ValueError:
                        print("❌Invalid Input")
                with open(expenseBudget, 'a') as file:
                    file.write(f"{budget}")
        except FileNotFoundError:
            with open(expenseBudget, 'a') as file:
                file.write("")
    return budget

def changeBudget():
    #Clearing users Budget
    print("Clearing in progress🧹....")
    time.sleep(1)
    print("Your budget has been Cleared Successfully😁\n-------------------------------------------")
    with open(expenseBudget, 'r+') as file:
        file.truncate(0)
    while True:
        try:
            changedBudget=float(input("Enter your Budget for the Month💵: "))
            print("----------------------------------\n")
            print(f"Your Budget for the Month is ${changedBudget}\n-----------------------------------------------")
            break
        except ValueError:    
            print("❌Invalid Input")
    with open(expenseBudget, 'a') as file:
        file.write(f"{changedBudget}")
    
    return changedBudget



#prompt the user until the user inputs the correct input and then return the input
def userinput():
    while True:
        try:
            userInput=int(input(f"🎯 Choose one of the following option choices: \n 1. Food😋\n 2. Home🏠\n 3. Work⚒️ \n 4. Fun🎉\n 5. Miscellaneous⛷️\n 6. Display Report📜\n 7. Clear Report📜\n 8. Add New Budget💵\n 0. Exit🏃‍♂️‍➡️ \n(Enter the corresponting Number 0-8)✅: "))
            if userInput>=0 and userInput<=8:
                break
            else:
                print("❌Invalid Input")
        except ValueError:
            print("❌Invalid Input")
    return userInput

def userChoice(userChoicenum):
    while userChoicenum>=1 and userChoicenum<=8:
        while userChoicenum==6:#Display Report
            os.system('cls')
            try:
                with open(reportPath, 'r', encoding='utf-8') as file:
                    content=file.read()
                if content:
                    print(content)
                    
                    with open(expenseBudget, 'r') as file:
                        user_budget=file.read()
                    
                    totalAmount, amountLeft=addExpense(user_budget)
                    
                    #rounding spent amount and total amount by 2
                    totalAmount=round(totalAmount, 2)
                    amountLeft=round(amountLeft, 2)
                    
                    #prints Total Expense
                    print(f"Your total expense is ${totalAmount}\n--------------------------------------")
                    
                    if amountLeft>0:
                        print(f"While you still have ${amountLeft}🤑\n--------------------------------------")
                    else:
                        print(f"❗You have spent {abs(amountLeft)} more then your Budget for the month🥲\n---------------------------------------------------------------------------")
                else:
                    print("Your Report is Empty🥲\n-----------------------")
            except FileNotFoundError:
                with open(reportPath, 'a', encoding='utf-8') as file:
                    file.write("")
                    print("Your Report is Empty🥲")
                
            userChoicenum=userinput()
        
        while userChoicenum==7:#Clear Report
            os.system('cls')
            with open(reportPath, 'r', encoding='utf-8') as file:
                content=file.read()

            with open(totalExpense, 'r') as file:
                content1=file.read()

                if content and content1:
                    #Clearing users report
                    print("Clearing in progress🧹....")
                    time.sleep(1)
                    print("Your report has been Cleared Successfully😁")
                    with open(reportPath, 'r+') as file:
                        file.truncate(0)
                    with open(totalExpense, 'r+') as file:
                        file.truncate(0)
                    userChoicenum=userinput()
                else:
                    print("\nYour Report is already Empty🥲\n")
                    userChoicenum=userinput()
                  

        while userChoicenum==8:#change budget
            os.system('cls')
            with open(expenseBudget, 'r+') as file:
                file.truncate(0)

            user_budget=changeBudget()
            userChoicenum=userinput()

            #Clearing the expense file
            

            #userChoicenum=userinput() 
        
        while userChoicenum>=1 and userChoicenum<=5:#Expense Categories
            category, expensename, expenseamount=getUserExpense(userChoicenum)
            saveToFile(category, expensename, expenseamount)
            userChoicenum=userinput()   
    if userChoicenum==0:
        os.system('cls')
        print("Exiting the Program😔\n")
        quit()       
    
#User input the expense name and amount
def getUserExpense(Category):
    Categories=['Food🍉', 'Home🏠', 'Work⚒️', 'Fun🎉', 'Miscellaneous⛷️', 'Display Report📜']
    category=Categories[Category-1]
    while True:
        expenseName=input(f"Enter the name of the {category} Expense: ")
        if expenseName.replace(" ","").isalpha():
            break
        else:
            print("❌Invalid Input\n")
    while True:
        try:
            expenseAmount=float(input(f"Enter the amount of the {category} Expense: "))
            break
        except ValueError:
            print("❌Invalid Input\n")


        #print(f"Your {category} Expense name is {expenseName} and the expense amount is {expenseAmount}")
    os.system('cls')
    return category, expenseName, expenseAmount


# save the expense name, category, and amount to file 
def saveToFile(category, name, amount):
    amount=round(amount, 2)
    print(f"Saving Expense name: {name}, and Expense amount: ${amount} to {category}  in your report😁......")
    
    #Saving to the Report fpr the User
    with open(reportPath, 'a', encoding='utf-8') as file:
        file.write(f"{category} | {name} | {amount} | {Date} \n")
    
    #Saving to the file that will be used to tll the user their full expense
    with open(totalExpense, 'a') as file:
        file.write(f"{amount}\n")

# read the file thaat has all the amounts entered by the user and add them up and return the value
def addExpense(budget):#adds the expense and expense amoundto the corresponding files 
    with open(totalExpense,'r') as file:
        amounts=file.readlines()
    #line 76 is from Blackbox.ai
    totalAmountspent=sum(float(line.strip()) for line in amounts)
    print(totalAmountspent)
    totalAmountSaved=float(budget)-totalAmountspent
    #print(totalAmountSaved)
    return totalAmountspent, totalAmountSaved

intro()

user_budget=userBudget()

userChoicenum=userinput()

userChoice(userChoicenum)












