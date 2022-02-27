import xlsxwriter
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import random


def prog_create(name, days, expLevel):
    ############################## DECLARING VARIABLES #########################################
    #BEGINNER SPLIT
    upLow = ["chest", "shoulder", "triceps", "back", "biceps", "legs", "legs", "legs", "legs", "legs",
            "chest", "shoulder", "triceps", "back", "biceps", "legs", "legs", "legs", "legs", "legs"]
    
    #INTERMEDIATE SPLIT
    ppl = ["chest", "shoulder", "chest", "triceps", "triceps", "back", "back", "back","biceps", "biceps","legs", "legs", "legs", "legs", "legs",
    "chest", "shoulder", "chest", "triceps", "triceps", "back", "back", "back","biceps", "biceps","legs", "legs", "legs", "legs", "legs"]
   
   #ADVANCED SPLIT
    muscleSplit = ["chest", "chest", "chest", "triceps", "triceps","back", "back", "back","biceps", "biceps","shoulders", "legs", "legs", "legs", "legs",
    "chest", "chest", "chest", "triceps", "triceps","back", "back", "back","biceps", "biceps","shoulders", "legs", "legs", "legs", "legs"]

    eRange = 5 #static number of excercises
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
    worksheet = workbook.add_worksheet()

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
        worksheet.merge_range('A1:S3', "", cell_format)#-----WEEK Formatting (Static)
        for i in range(int(days)):
        
            temp = i #just to calculate
            dayNum = i+1 #gets the day number
            weekNum = dayNum - temp #gets the week number
            worksheet.write('A1', u'WEEK '+str(weekNum), weekCellFormat)#----Week Number

            worksheet.merge_range('A'+str(position)+":B"+str(position)+"", "", cell_format)#-----Format cells for day
            worksheet.write('A'+str(position)+"", u'DAY '+str(dayNum)+"",dayCellFormat)#----Day number

            position+=2 #update position for excercises

            for x in range(eRange):#picks and writes the 5 excercises
                selection = "NULL" #Holds the selection
                
                #picks a random excercise from the muscle group obtained from upLow
                for excercise in Accessories.query.filter_by(muscle = upLow[x]).order_by(Accessories.name):
                    selection = random.choice(excercise.name)

                worksheet.merge_range("A"+str(position)+":C"+str(position)+"", "", dayCellFormat)#merge cells for excercise name            
                worksheet.write('A'+str(position)+"",selection, movementFormat)#inputs excercise name
                worksheet.write("D"+str(position)+"", ""+str(random.choice(setRange))+"x"+str(random.choice(repRange))+"", movementFormat) #inputs setxrep range
                position +=1#updates position
                #upLow.remove(0)#removes the selected entry to continue
                #upLow.remove(1)
                #upLow.remove(2)
                #upLow.remove(3)
                #upLow.remove(4)

            position += 2
    #Intermediate
    if(int(expLevel) == 2):
        worksheet.merge_range('A1:S3', "", cell_format)#-----WEEK Formatting (Static)
        for i in range(int(days)):
        
            temp = i #just to calculate
            dayNum = i+1 #gets the day number
            weekNum = dayNum - temp #gets the week number
            worksheet.write('A1', u'WEEK '+str(weekNum), weekCellFormat)#----Week Number

            worksheet.merge_range('A'+str(position)+":B"+str(position)+"", "", cell_format)#-----Format cells for day
            worksheet.write('A'+str(position)+"", u'DAY '+str(dayNum)+"",dayCellFormat)#----Day number

            position+=2 #update position for excercises

            for x in range(5):#picks and writes the 5 excercises
                selection = "NULL" #Holds the selection
                
                #picks a random excercise from the muscle group obtained from upLow
                for exercise in Accessories.query.filter_by(muscle = ppl[x]).order_by(Accessories.name):
                    selection = exercise.name

                worksheet.merge_range("A"+str(position)+":C"+str(position)+"", "", dayCellFormat)#merge cells for excercise name            
                worksheet.write('A'+str(position)+"",selection, movementFormat)#inputs excercise name
                worksheet.write("D"+str(position)+"", ""+str(random.choice(setRange))+"x"+str(random.choice(repRange))+"", movementFormat) #inputs setxrep range
                position +=1#updates position
            x+=5

            position += 2
    #Advanced 
    if(int(expLevel) == 3):
        worksheet.merge_range('A1:S3', "", cell_format)#-----WEEK Formatting (Static)
        for i in range(int(days)):
        
            temp = i #just to calculate
            dayNum = i+1 #gets the day number
            weekNum = dayNum - temp #gets the week number
            worksheet.write('A1', u'WEEK '+str(weekNum), weekCellFormat)#----Week Number

            worksheet.merge_range('A'+str(position)+":B"+str(position)+"", "", cell_format)#-----Format cells for day
            worksheet.write('A'+str(position)+"", u'DAY '+str(dayNum)+"",dayCellFormat)#----Day number

            position+=2 #update position for excercises

            for x in range(eRange):#picks and writes the 5 excercises
                selection = "NULL" #Holds the selection
                
                #picks a random excercise from the muscle group obtained from upLow
                for excercise in Accessories.query.filter_by(muscle = muscleSplit[x]).order_by(Accessories.name):
                    selection = random.choice(excercise.name)
                worksheet.merge_range("A"+str(position)+":C"+str(position)+"", "", dayCellFormat)#merge cells for excercise name            
                worksheet.write('A'+str(position)+"",selection, movementFormat)#inputs excercise name
                worksheet.write("D"+str(position)+"", ""+str(random.choice(setRange))+"x"+str(random.choice(repRange))+"", movementFormat) #inputs setxrep range
                position +=1#updates position
                #muscleSplit.remove(0)#removes the selected entry to continue
                #muscleSplit.remove(1)#removes the selected entry to continue
                #muscleSplit.remove(2)#removes the selected entry to continue
                #muscleSplit.remove(3)#removes the selected entry to continue
                #muscleSplit.remove(4)#removes the selected entry to continue

            position += 2









    ################################### END CHOOSING SPLIT/EXP LEVEL ###############################################

    #close the worksheet
    workbook.close()

    if (__name__ == "__main__"):
        app.run(debug=True)
