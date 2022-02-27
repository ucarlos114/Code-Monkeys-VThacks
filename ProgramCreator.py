from questionnaire import *
import xlsxwriter
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy import desc

questionnaire()
############################## CONNECT TO DATABASE #####################################333

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

chestExcercise = Accessories.query.filter_by(muscle = 'chest').order_by(Accessories.name).all()


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
                                   'valign': 'vcenter','bold': True})

######################################### END FORMATS FOR WORKBOOK #############################################

######################################### Writing to Cells #####################################################
worksheet.merge_range('A1:K3', "", cell_format)#-----WEEK X
worksheet.write('A1', u'WEEK 1',weekCellFormat)


worksheet.merge_range('A5:B5', "", cell_format)#-----DAY X
worksheet.write('A5', u'DAY 1',dayCellFormat)
worksheet.write(chestExcercise, movementFormat)


worksheet.merge_range('D5:E5', "", cell_format)#-----DAY X
worksheet.write('D5', u'DAY 2',dayCellFormat)

worksheet.merge_range('G5:H5', "", cell_format)#-----DAY X
worksheet.write('G5', u'DAY 3',dayCellFormat)

worksheet.merge_range('J5:K5', "", cell_format)#-----DAY X
worksheet.write('J5', u'DAY 4',dayCellFormat)
##################################### END WRITING TO CELLS ###########################################################
#close the worksheet
workbook.close()

if (__name__ == "__main__"):
    app.run(debug=True)
