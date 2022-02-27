import xlsxwriter
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from  sqlalchemy.sql.expression import func

import random


def prog_create(name, days, expLevel):
    ############################## DECLARING VARIABLES #########################################
    #BEGINNER SPLIT
    upLow = ["chestC", "shoulders", "triceps", "back", "biceps", "legsC", "backC", "legs", "legs", "legs",
             "chestC", "shoulders", "triceps", "back", "biceps", "legsC", "backC", "legs", "legs", "legs",
             "chestC", "shoulders", "triceps", "back", "biceps", "legsC", "backC", "legs", "legs", "legs",
             "chestC", "shoulders", "triceps", "back", "biceps", "legsC", "backC", "legs", "legs", "legs"]
    
    #INTERMEDIATE SPLIT
    ppl = ["chestC", "shoulders", "chest", "triceps", "triceps", "backC", "back", "back","biceps", "biceps","legsC", "legs", "legs", "legs", "legs",
    "chestC", "shoulders", "chest", "triceps", "triceps", "backC", "back", "back","biceps", "biceps","legsC", "legs", "legs", "legs", "legs"]
   
   #ADVANCED SPLIT
    muscleSplit = ["chestC", "chest", "chest", "triceps", "triceps","backC", "back", "back","biceps", "biceps","shoulders", "legsC", "legs", "legs", "legs",
    "chestC", "chest", "chest", "triceps", "triceps","backC", "back", "back","biceps", "biceps","shoulders", "legsC", "legs", "legs", "legs"]

    bp = "Bench Press"
    setRange = [3, 4]#used to get a set range 
    repRange = [6, 8, 10, 12]#used to get a rep range

    position = 5 #cell position
    ############################## END DECLARING VARS #########################################

    ############################## CONNECT TO DATABASE #####################################

    app = Flask(__name__)


    db_name = 'exercises.db'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db = SQLAlchemy(app)

    class Accessories(db.Model):
        __tablename__ = "accessories"
        id = db.Column(db.Integer, primary_key=True)
        muscle = db.Column(db.String)
        name = db.Column(db.String)

    ############################ END DATABASE STUFF ###############################################

    chestQuery = Accessories.query.filter_by(muscle = "chest").order_by(Accessories.name)
    backQuery = Accessories.query.filter_by(muscle = "back").order_by(Accessories.name)
    shoulderQuery = Accessories.query.filter_by(muscle = "shoulders").order_by(Accessories.name)
    biQuery = Accessories.query.filter_by(muscle = "biceps").order_by(Accessories.name)
    triQuery = Accessories.query.filter_by(muscle = "triceps").order_by(Accessories.name)
    legQuery = Accessories.query.filter_by(muscle = "legs").order_by(Accessories.name)

    


    #takes one arguement which is the file name
    workbook = xlsxwriter.Workbook(name+'.xlsx')

    #adds new worksheet
    worksheet = workbook.add_worksheet("Week 1")
    worksheet1 = workbook.add_worksheet("Week 2")
    worksheet2 = workbook.add_worksheet("Week 3")
    worksheet3 = workbook.add_worksheet("Week 4")

    ######################################## FORMATS FOR WORKBOOK #################################################
    red = workbook.add_format({'color': 'red'})
    blue = workbook.add_format({'color': 'blue'})
    cell_format = workbook.add_format({'align': 'center',
                                    'valign': 'vcenter',
                                    'border': 2, 'bold': True})

    weekCellFormat = workbook.add_format({'align': 'center',
                                    'valign': 'vcenter','bold': True, })#Week cell formatting
    weekCellFormat.set_font_size(20)#increases size of text in week cell

    dayCellFormat = workbook.add_format({'align': 'center',
                                    'valign': 'vcenter','bold': True, 'border':2 })# day cell formatting

    movementFormat = workbook.add_format({'align': 'center',
                                    'valign': 'vcenter','bold': True, 'border':2})
    movementFormat.set_text_wrap()

    ######################################### END FORMATS FOR WORKBOOK #############################################

    ################################### CHOOSING SPLIT/EXP LEVEL ###################################################
    
    #Beginner
    if (int(expLevel) == 1):
#**************************** WEEK 1 **************************************#
        worksheet.merge_range('A1:F3', "", cell_format)#-----WEEK Formatting (Static)
        for i in range(int(days)):
            
            temp = i #just to calculate
            dayNum = i+1 #gets the day number
            weekNum = dayNum - temp #gets the week number
            worksheet.write('A1', u'WEEK '+str(weekNum), weekCellFormat)#----Week Number

            worksheet.merge_range('A'+str(position)+":B"+str(position)+"", "", cell_format)#-----Format cells for day
            worksheet.write('A'+str(position)+"", u'DAY '+str(dayNum)+"",dayCellFormat)#----Day number
            worksheet.merge_range('C'+str(position)+":D"+str(position)+"", "", cell_format)#-----Format cells for label
            if (i % 2 == 0):
                worksheet.write('C'+str(position)+"", u'UPPER BODY ',dayCellFormat)#----Label
            else:
                worksheet.write('C'+str(position)+"", u'LOWER BODY ',dayCellFormat)#----Label

            position+=2 #update position for exercises
            chosenList = []
            for x in range(5):#picks and writes the 5 exercises
                tempList = []
                
                
                #picks a random exercise from the muscle group obtained from ppl
                for exercise in Accessories.query.filter_by(muscle = upLow[x + 5*i]).order_by(Accessories.name):
                    print(exercise.name)
                    print(str(len(tempList)))
                    tempList.append(exercise.name)
                
                choice = random.choice(tempList)
                while (choice in chosenList):
                    choice = random.choice(tempList)
                    
                worksheet.merge_range("A"+str(position)+":C"+str(position)+"", "", dayCellFormat)#merge cells for exercise name            
                worksheet.write('A'+str(position)+"",choice, movementFormat)#inputs exercise name
                worksheet.write("D"+str(position)+"", ""+str(random.choice(setRange))+"x"+str(random.choice(repRange))+"", movementFormat) #inputs setxrep range
                chosenList.append(choice)
                position +=1#updates position

            position += 2
        #*********************************** WEEK 2 *******************************#
        position = 5
        worksheet1.merge_range('A1:F3', "", cell_format)#-----WEEK Formatting (Static)
        for i in range(int(days)):
            
            temp = i #just to calculate
            dayNum = i+1 #gets the day number
            weekNum = dayNum - temp #gets the week number
            worksheet1.write('A1', u'WEEK 2', weekCellFormat)#----Week Number

            worksheet1.merge_range('A'+str(position)+":B"+str(position)+"", "", cell_format)#-----Format cells for day
            worksheet1.write('A'+str(position)+"", u'DAY '+str(dayNum)+"",dayCellFormat)#----Day number
            worksheet1.merge_range('C'+str(position)+":D"+str(position)+"", "", cell_format)#-----Format cells for label
            if (i % 2 == 0):
                worksheet1.write('C'+str(position)+"", u'UPPER BODY ',dayCellFormat)#----Label
            else:
                worksheet1.write('C'+str(position)+"", u'LOWER BODY ',dayCellFormat)#----Label

            position+=2 #update position for exercises
            chosenList = []
            for x in range(5):#picks and writes the 5 exercises
                tempList = []
                
                
                #picks a random exercise from the muscle group obtained from ppl
                for exercise in Accessories.query.filter_by(muscle = upLow[x + 5*i]).order_by(Accessories.name):
                    tempList.append(exercise.name)
                
                choice = random.choice(tempList)
                while (choice in chosenList):
                    choice = random.choice(tempList)
                worksheet1.merge_range("A"+str(position)+":C"+str(position)+"", "", dayCellFormat)#merge cells for exercise name            
                worksheet1.write('A'+str(position)+"",choice, movementFormat)#inputs exercise name
                worksheet1.write("D"+str(position)+"", ""+str(random.choice(setRange))+"x"+str(random.choice(repRange))+"", movementFormat) #inputs setxrep range
                chosenList.append(choice)
                position +=1#updates position

            position += 2
            
        
        #*********************************** WEEK 3 *******************************#
        position = 5
        worksheet2.merge_range('A1:F3', "", cell_format)#-----WEEK Formatting (Static)
        for i in range(int(days)):
            
            temp = i #just to calculate
            dayNum = i+1 #gets the day number
            weekNum = dayNum - temp #gets the week number
            worksheet2.write('A1', u'WEEK 3', weekCellFormat)#----Week Number

            worksheet2.merge_range('A'+str(position)+":B"+str(position)+"", "", cell_format)#-----Format cells for day
            worksheet2.write('A'+str(position)+"", u'DAY '+str(dayNum)+"",dayCellFormat)#----Day number
            worksheet2.merge_range('C'+str(position)+":D"+str(position)+"", "", cell_format)#-----Format cells for label
            if (i % 2 == 0):
                worksheet2.write('C'+str(position)+"", u'UPPER BODY ',dayCellFormat)#----Label
            else:
                worksheet2.write('C'+str(position)+"", u'LOWER BODY ',dayCellFormat)#----Label

            position+=2 #update position for exercises
            chosenList = []
            for x in range(5):#picks and writes the 5 exercises
                tempList = []
                
                
                #picks a random exercise from the muscle group obtained from ppl
                for exercise in Accessories.query.filter_by(muscle = upLow[x + 5*i]).order_by(Accessories.name):
                    tempList.append(exercise.name)
                
                choice = random.choice(tempList)
                while (choice in chosenList):
                    choice = random.choice(tempList)
                worksheet2.merge_range("A"+str(position)+":C"+str(position)+"", "", dayCellFormat)#merge cells for exercise name            
                worksheet2.write('A'+str(position)+"",choice, movementFormat)#inputs exercise name
                worksheet2.write("D"+str(position)+"", ""+str(random.choice(setRange))+"x"+str(random.choice(repRange))+"", movementFormat) #inputs setxrep range
                chosenList.append(choice)
                position +=1#updates position

            position += 2
        
         #*********************************** WEEK 4 *******************************#
        position = 5
        worksheet3.merge_range('A1:F3', "", cell_format)#-----WEEK Formatting (Static)
        for i in range(int(days)):
            
            temp = i #just to calculate
            dayNum = i+1 #gets the day number
            weekNum = dayNum - temp #gets the week number
            worksheet3.write('A1', u'WEEK 4', weekCellFormat)#----Week Number

            worksheet3.merge_range('A'+str(position)+":B"+str(position)+"", "", cell_format)#-----Format cells for day
            worksheet3.write('A'+str(position)+"", u'DAY '+str(dayNum)+"",dayCellFormat)#----Day number
            worksheet3.merge_range('C'+str(position)+":D"+str(position)+"", "", cell_format)#-----Format cells for label
            if (i % 2 == 0):
                worksheet3.write('C'+str(position)+"", u'UPPER BODY ',dayCellFormat)#----Label
            else:
                worksheet3.write('C'+str(position)+"", u'LOWER BODY ',dayCellFormat)#----Label
            position+=2 #update position for exercises
            chosenList = []
            for x in range(5):#picks and writes the 5 exercises
                tempList = []
                
                
                #picks a random exercise from the muscle group obtained from ppl
                for exercise in Accessories.query.filter_by(muscle = upLow[x + 5*i]).order_by(Accessories.name):
                    tempList.append(exercise.name)
                
                choice = random.choice(tempList)
                while (choice in chosenList):
                    choice = random.choice(tempList)
                worksheet3.merge_range("A"+str(position)+":C"+str(position)+"", "", dayCellFormat)#merge cells for exercise name            
                worksheet3.write('A'+str(position)+"",choice, movementFormat)#inputs exercise name
                worksheet3.write("D"+str(position)+"", ""+str(random.choice(setRange))+"x"+str(random.choice(repRange))+"", movementFormat) #inputs setxrep range
                chosenList.append(choice)
                position +=1#updates position

            position += 2
    #Intermediate
    if(int(expLevel) == 2):
        
        #**************************** WEEK 1 **************************************#
        worksheet.merge_range('A1:F3', "", cell_format)#-----WEEK Formatting (Static)
        for i in range(int(days)):
            
            temp = i #just to calculate
            dayNum = i+1 #gets the day number
            weekNum = dayNum - temp #gets the week number
            worksheet.write('A1', u'WEEK '+str(weekNum), weekCellFormat)#----Week Number

            worksheet.merge_range('A'+str(position)+":B"+str(position)+"", "", cell_format)#-----Format cells for day
            worksheet.write('A'+str(position)+"", u'DAY '+str(dayNum)+"",dayCellFormat)#----Day number
            worksheet.merge_range('C'+str(position)+":D"+str(position)+"", "", cell_format)#-----Format cells for label
            if (i % 3 == 0):
                worksheet.write('C'+str(position)+"", u'PUSH ',dayCellFormat)#----Label
            elif (i % 3 == 1):
                worksheet.write('C'+str(position)+"", u'PULL ',dayCellFormat)#----Label
            else:
                worksheet.write('C'+str(position)+"", u'LEGS ',dayCellFormat)#----Label

            position+=2 #update position for exercises
            chosenList = []
            for x in range(5):#picks and writes the 5 exercises
                tempList = []
                
                
                #picks a random exercise from the muscle group obtained from ppl
                for exercise in Accessories.query.filter_by(muscle = ppl[x + 5*i]).order_by(Accessories.name):
                    tempList.append(exercise.name)
                
                choice = random.choice(tempList)
                while (choice in chosenList):
                    choice = random.choice(tempList)
                    
                worksheet.merge_range("A"+str(position)+":C"+str(position)+"", "", dayCellFormat)#merge cells for exercise name            
                worksheet.write('A'+str(position)+"",choice, movementFormat)#inputs exercise name
                worksheet.write("D"+str(position)+"", ""+str(random.choice(setRange))+"x"+str(random.choice(repRange))+"", movementFormat) #inputs setxrep range
                chosenList.append(choice)
                position +=1#updates position

            position += 2
        #*********************************** WEEK 2 *******************************#
        position = 5
        worksheet1.merge_range('A1:F3', "", cell_format)#-----WEEK Formatting (Static)
        for i in range(int(days)):
            
            temp = i #just to calculate
            dayNum = i+1 #gets the day number
            weekNum = dayNum - temp #gets the week number
            worksheet1.write('A1', u'WEEK 2', weekCellFormat)#----Week Number

            worksheet1.merge_range('A'+str(position)+":B"+str(position)+"", "", cell_format)#-----Format cells for day
            worksheet1.write('A'+str(position)+"", u'DAY '+str(dayNum)+"",dayCellFormat)#----Day number
            worksheet1.merge_range('C'+str(position)+":D"+str(position)+"", "", cell_format)#-----Format cells for label
            if (i % 3 == 0):
                worksheet1.write('C'+str(position)+"", u'PUSH ',dayCellFormat)#----Label
            elif (i % 3 == 1):
                worksheet1.write('C'+str(position)+"", u'PULL ',dayCellFormat)#----Label
            else:
                worksheet1.write('C'+str(position)+"", u'LEGS ',dayCellFormat)#----Label

            position+=2 #update position for exercises
            chosenList = []
            for x in range(5):#picks and writes the 5 exercises
                tempList = []
                
                
                #picks a random exercise from the muscle group obtained from ppl
                for exercise in Accessories.query.filter_by(muscle = ppl[x + 5*i]).order_by(Accessories.name):
                    tempList.append(exercise.name)
                
                choice = random.choice(tempList)
                while (choice in chosenList):
                    choice = random.choice(tempList)
                worksheet1.merge_range("A"+str(position)+":C"+str(position)+"", "", dayCellFormat)#merge cells for exercise name            
                worksheet1.write('A'+str(position)+"",choice, movementFormat)#inputs exercise name
                worksheet1.write("D"+str(position)+"", ""+str(random.choice(setRange))+"x"+str(random.choice(repRange))+"", movementFormat) #inputs setxrep range
                chosenList.append(choice)
                position +=1#updates position

            position += 2
            
        
        #*********************************** WEEK 3 *******************************#
        position = 5
        worksheet2.merge_range('A1:F3', "", cell_format)#-----WEEK Formatting (Static)
        for i in range(int(days)):
            
            temp = i #just to calculate
            dayNum = i+1 #gets the day number
            weekNum = dayNum - temp #gets the week number
            worksheet2.write('A1', u'WEEK 3', weekCellFormat)#----Week Number

            worksheet2.merge_range('A'+str(position)+":B"+str(position)+"", "", cell_format)#-----Format cells for day
            worksheet2.write('A'+str(position)+"", u'DAY '+str(dayNum)+"",dayCellFormat)#----Day number
            worksheet2.merge_range('C'+str(position)+":D"+str(position)+"", "", cell_format)#-----Format cells for label
            if (i % 3 == 0):
                worksheet2.write('C'+str(position)+"", u'PUSH ',dayCellFormat)#----Label
            elif (i % 3 == 1):
                worksheet2.write('C'+str(position)+"", u'PULL ',dayCellFormat)#----Label
            else:
                worksheet2.write('C'+str(position)+"", u'LEGS ',dayCellFormat)#----Label

            position+=2 #update position for exercises
            chosenList = []
            for x in range(5):#picks and writes the 5 exercises
                tempList = []
                
                
                #picks a random exercise from the muscle group obtained from ppl
                for exercise in Accessories.query.filter_by(muscle = ppl[x + 5*i]).order_by(Accessories.name):
                    tempList.append(exercise.name)
                
                choice = random.choice(tempList)
                while (choice in chosenList):
                    choice = random.choice(tempList)
                worksheet2.merge_range("A"+str(position)+":C"+str(position)+"", "", dayCellFormat)#merge cells for exercise name            
                worksheet2.write('A'+str(position)+"",choice, movementFormat)#inputs exercise name
                worksheet2.write("D"+str(position)+"", ""+str(random.choice(setRange))+"x"+str(random.choice(repRange))+"", movementFormat) #inputs setxrep range
                chosenList.append(choice)
                position +=1#updates position

            position += 2
        
         #*********************************** WEEK 4 *******************************#
        position = 5
        worksheet3.merge_range('A1:F3', "", cell_format)#-----WEEK Formatting (Static)
        for i in range(int(days)):
            
            temp = i #just to calculate
            dayNum = i+1 #gets the day number
            weekNum = dayNum - temp #gets the week number
            worksheet3.write('A1', u'WEEK 4', weekCellFormat)#----Week Number

            worksheet3.merge_range('A'+str(position)+":B"+str(position)+"", "", cell_format)#-----Format cells for day
            worksheet3.write('A'+str(position)+"", u'DAY '+str(dayNum)+"",dayCellFormat)#----Day number
            worksheet3.merge_range('C'+str(position)+":D"+str(position)+"", "", cell_format)#-----Format cells for label
            if (i % 3 == 0):
                worksheet3.write('C'+str(position)+"", u'PUSH ',dayCellFormat)#----Label
            elif (i % 3 == 1):
                worksheet3.write('C'+str(position)+"", u'PULL ',dayCellFormat)#----Label
            else:
                worksheet3.write('C'+str(position)+"", u'LEGS ',dayCellFormat)#----Label

            position+=2 #update position for exercises
            chosenList = []
            for x in range(5):#picks and writes the 5 exercises
                tempList = []
                
                
                #picks a random exercise from the muscle group obtained from ppl
                for exercise in Accessories.query.filter_by(muscle = ppl[x + 5*i]).order_by(Accessories.name):
                    tempList.append(exercise.name)
                
                choice = random.choice(tempList)
                while (choice in chosenList):
                    choice = random.choice(tempList)
                worksheet3.merge_range("A"+str(position)+":C"+str(position)+"", "", dayCellFormat)#merge cells for exercise name            
                worksheet3.write('A'+str(position)+"",choice, movementFormat)#inputs exercise name
                worksheet3.write("D"+str(position)+"", ""+str(random.choice(setRange))+"x"+str(random.choice(repRange))+"", movementFormat) #inputs setxrep range
                chosenList.append(choice)
                position +=1#updates position

            position += 2
    #Advanced 
    if(int(expLevel) == 3):
        #**************************** WEEK 1 **************************************#
        worksheet.merge_range('A1:F3', "", cell_format)#-----WEEK Formatting (Static)
        for i in range(int(days)):
            
            temp = i #just to calculate
            dayNum = i+1 #gets the day number
            weekNum = dayNum - temp #gets the week number
            worksheet.write('A1', u'WEEK '+str(weekNum), weekCellFormat)#----Week Number

            worksheet.merge_range('A'+str(position)+":B"+str(position)+"", "", cell_format)#-----Format cells for day
            worksheet.write('A'+str(position)+"", u'DAY '+str(dayNum)+"",dayCellFormat)#----Day number
            worksheet.merge_range('C'+str(position)+":D"+str(position)+"", "", cell_format)#-----Format cells for label
            if (i % 3 == 0):
                worksheet.write('C'+str(position)+"", u'CHEST/TRICEPS ',dayCellFormat)#----Label
            elif (i % 3 == 1):
                worksheet.write('C'+str(position)+"", u'BACK/BICEPS ',dayCellFormat)#----Label
            else:
                worksheet.write('C'+str(position)+"", u'LEGS/SHOULDERS ',dayCellFormat)#----Label

            position+=2 #update position for exercises
            chosenList = []
            for x in range(5):#picks and writes the 5 exercises
                tempList = []
                
                
                #picks a random exercise from the muscle group obtained from ppl
                for exercise in Accessories.query.filter_by(muscle = muscleSplit[x + 5*i]).order_by(Accessories.name):
                    tempList.append(exercise.name)
                
                choice = random.choice(tempList)
                while (choice in chosenList):
                    choice = random.choice(tempList)
                    
                worksheet.merge_range("A"+str(position)+":C"+str(position)+"", "", dayCellFormat)#merge cells for exercise name            
                worksheet.write('A'+str(position)+"",choice, movementFormat)#inputs exercise name
                worksheet.write("D"+str(position)+"", ""+str(random.choice(setRange))+"x"+str(random.choice(repRange))+"", movementFormat) #inputs setxrep range
                chosenList.append(choice)
                position +=1#updates position

            position += 2
        #*********************************** WEEK 2 *******************************#
        position = 5
        worksheet1.merge_range('A1:F3', "", cell_format)#-----WEEK Formatting (Static)
        for i in range(int(days)):
            
            temp = i #just to calculate
            dayNum = i+1 #gets the day number
            weekNum = dayNum - temp #gets the week number
            worksheet1.write('A1', u'WEEK 2', weekCellFormat)#----Week Number

            worksheet1.merge_range('A'+str(position)+":B"+str(position)+"", "", cell_format)#-----Format cells for day
            worksheet1.write('A'+str(position)+"", u'DAY '+str(dayNum)+"",dayCellFormat)#----Day number
            worksheet1.merge_range('C'+str(position)+":D"+str(position)+"", "", cell_format)#-----Format cells for label
            if (i % 3 == 0):
                worksheet1.write('C'+str(position)+"", u'CHEST/TRICEPS ',dayCellFormat)#----Label
            elif (i % 3 == 1):
                worksheet1.write('C'+str(position)+"", u'BACK/BICEPS ',dayCellFormat)#----Label
            else:
                worksheet1.write('C'+str(position)+"", u'LEGS/SHOULDERS ',dayCellFormat)#----Label

            position+=2 #update position for exercises
            chosenList = []
            for x in range(5):#picks and writes the 5 exercises
                tempList = []
                
                
                #picks a random exercise from the muscle group obtained from ppl
                for exercise in Accessories.query.filter_by(muscle = muscleSplit[x + 5*i]).order_by(Accessories.name):
                    tempList.append(exercise.name)
                
                choice = random.choice(tempList)
                while (choice in chosenList):
                    choice = random.choice(tempList)
                worksheet1.merge_range("A"+str(position)+":C"+str(position)+"", "", dayCellFormat)#merge cells for exercise name            
                worksheet1.write('A'+str(position)+"",choice, movementFormat)#inputs exercise name
                worksheet1.write("D"+str(position)+"", ""+str(random.choice(setRange))+"x"+str(random.choice(repRange))+"", movementFormat) #inputs setxrep range
                chosenList.append(choice)
                position +=1#updates position

            position += 2
            
        
        #*********************************** WEEK 3 *******************************#
        position = 5
        worksheet2.merge_range('A1:F3', "", cell_format)#-----WEEK Formatting (Static)
        for i in range(int(days)):
            
            temp = i #just to calculate
            dayNum = i+1 #gets the day number
            weekNum = dayNum - temp #gets the week number
            worksheet2.write('A1', u'WEEK 3', weekCellFormat)#----Week Number

            worksheet2.merge_range('A'+str(position)+":B"+str(position)+"", "", cell_format)#-----Format cells for day
            worksheet2.write('A'+str(position)+"", u'DAY '+str(dayNum)+"",dayCellFormat)#----Day number
            worksheet2.merge_range('C'+str(position)+":D"+str(position)+"", "", cell_format)#-----Format cells for label
            if (i % 3 == 0):
                worksheet2.write('C'+str(position)+"", u'CHEST/TRICEPS ',dayCellFormat)#----Label
            elif (i % 3 == 1):
                worksheet2.write('C'+str(position)+"", u'BACK/BICEPS ',dayCellFormat)#----Label
            else:
                worksheet2.write('C'+str(position)+"", u'LEGS/SHOULDERS ',dayCellFormat)#----Label

            position+=2 #update position for exercises
            chosenList = []
            for x in range(5):#picks and writes the 5 exercises
                tempList = []
                
                
                #picks a random exercise from the muscle group obtained from ppl
                for exercise in Accessories.query.filter_by(muscle = muscleSplit[x + 5*i]).order_by(Accessories.name):
                    tempList.append(exercise.name)
                
                choice = random.choice(tempList)
                while (choice in chosenList):
                    choice = random.choice(tempList)
                worksheet2.merge_range("A"+str(position)+":C"+str(position)+"", "", dayCellFormat)#merge cells for exercise name            
                worksheet2.write('A'+str(position)+"",choice, movementFormat)#inputs exercise name
                worksheet2.write("D"+str(position)+"", ""+str(random.choice(setRange))+"x"+str(random.choice(repRange))+"", movementFormat) #inputs setxrep range
                chosenList.append(choice)
                position +=1#updates position

            position += 2
        
         #*********************************** WEEK 4 *******************************#
        position = 5
        worksheet3.merge_range('A1:F3', "", cell_format)#-----WEEK Formatting (Static)
        for i in range(int(days)):
            
            temp = i #just to calculate
            dayNum = i+1 #gets the day number
            weekNum = dayNum - temp #gets the week number
            worksheet3.write('A1', u'WEEK 4', weekCellFormat)#----Week Number

            worksheet3.merge_range('A'+str(position)+":B"+str(position)+"", "", cell_format)#-----Format cells for day
            worksheet3.write('A'+str(position)+"", u'DAY '+str(dayNum)+"",dayCellFormat)#----Day number
            worksheet3.merge_range('C'+str(position)+":D"+str(position)+"", "", cell_format)#-----Format cells for label
            if (i % 3 == 0):
                worksheet3.write('C'+str(position)+"", u'CHEST/TRICEPS ',dayCellFormat)#----Label
            elif (i % 3 == 1):
                worksheet3.write('C'+str(position)+"", u'BACK/BICEPS ',dayCellFormat)#----Label
            else:
                worksheet3.write('C'+str(position)+"", u'LEGS/SHOULDERS ',dayCellFormat)#----Label

            position+=2 #update position for exercises
            chosenList = []
            for x in range(5):#picks and writes the 5 exercises
                tempList = []
                
                
                #picks a random exercise from the muscle group obtained from ppl
                for exercise in Accessories.query.filter_by(muscle = muscleSplit[x + 5*i]).order_by(Accessories.name):
                    tempList.append(exercise.name)
                
                choice = random.choice(tempList)
                while (choice in chosenList):
                    choice = random.choice(tempList)
                worksheet3.merge_range("A"+str(position)+":C"+str(position)+"", "", dayCellFormat)#merge cells for exercise name            
                worksheet3.write('A'+str(position)+"",choice, movementFormat)#inputs exercise name
                worksheet3.write("D"+str(position)+"", ""+str(random.choice(setRange))+"x"+str(random.choice(repRange))+"", movementFormat) #inputs setxrep range
                chosenList.append(choice)
                position +=1#updates position

            position += 2






    ################################### END CHOOSING SPLIT/EXP LEVEL ###############################################

    #close the worksheet
    workbook.close()

    if (__name__ == "__main__"):
        app.run(debug=True)
