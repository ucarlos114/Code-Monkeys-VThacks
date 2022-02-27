import xlsxwriter
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import random



############################## DECLARING VARIABLES #########################################

setRange = [3, 4]#used to get a set range 
repRange = [6, 8, 10, 12]#used to get a rep range

name = "Carlos" #users name
days = 4 #how many days they wanna lift
expLevel = 1 #experience level (1 - beginner, 2 - intermediate, 3 - advanced)

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
chestCount = 0

#takes one arguement which is the file name
workbook = xlsxwriter.Workbook('moeed.xlsx')

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

######################################### Writing to Cells #####################################################

worksheet.merge_range('A1:S3', "", cell_format)#-----WEEK Formatting (Static)
for i in range(days):
    temp = i #just to calculate
    dayNum = i+1 #gets the day number
    weekNum = dayNum - temp #gets the week number
    worksheet.write('A1', u'WEEK '+str(weekNum), weekCellFormat)#----Week Number

    worksheet.merge_range('A'+str(position)+":B"+str(position)+"", "", cell_format)#-----Format cells for day
    worksheet.write('A'+str(position)+"", u'DAY '+str(dayNum)+"",dayCellFormat)#----Day number

    position+=2 #update position for excercises

    for chest in chestQuery:
        worksheet.merge_range("A"+str(position)+":C"+str(position)+"", "", dayCellFormat)
        worksheet.write('A'+str(position)+"",chest.name, movementFormat)
        worksheet.write("D"+str(position)+"", ""+str(random.choice(setRange))+"x"+str(random.choice(repRange))+"", movementFormat)
        chestCount+=1#remember to change var name
        position +=1
    position += 2



##################################### END WRITING TO CELLS ###########################################################
#close the worksheet
workbook.close()

if (__name__ == "__main__"):
    app.run(debug=True)
