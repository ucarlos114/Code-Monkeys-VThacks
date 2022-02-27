#checks the input
def get_digit(msg):
        while True:
            result = input(msg)
            try:
                val = int(result)
                break;
            except ValueError:
                print("Please enter a valid number")
    
        return val
    
class UserInfo:
    
    def __init__(self): 
        self.name="" 
        self.exp = 0
        self.days = 0
        
    #setter for name
    def setName(self, u_name):
        self.name.replace(u_name)
        
    #setter for exp
    def setExp(self, u_exp):
        self.exp.replace(u_exp)
        
    #setter for days  
    def setDays(self, u_days):
        self.u_days.replace(u_days)

    

    #quetionare function
    def questionnaire():
        name = input("Hello user! What is your name? ")
        print("")
        print("I'm happy to help, " + name)
        
        print("")
        print("I have a couple of questions to ask you before I build your workout program.")
        print("")
    
        print("What is your experience level when it comes to lifting?")
        print("\nExamples: <1 year of lifting -> beginner, 1-2 years of lifting -> intermediate, 2+ years -> advanced\n")
        # offer examples for each, 1 year, 2-3 years etc
        exp = get_digit("Enter 1 for beginner, 2 for intermediate, 3 for advanced: ")
        while not(1 <= exp <= 3):
            exp = get_digit("Please enter a number between 1 and 3: ")
    
        # limit based on experience
        print("How many days of the week would you like to work out?")
        days = get_digit("(Between 2 and " + str(exp + 3) + ") ")