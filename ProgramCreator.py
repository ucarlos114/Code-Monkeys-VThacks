from questionnaire import *
import xlsxwriter
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy import desc

questionnaire()

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
    

#takes one arguement which is the file name
workbook = xlsxwriter.Workbook(name+'.xlsx')

#adds new worksheet
worksheet = workbook.add_worksheet()

# Use the worksheet object to write
# data via the write() method.
worksheet.write('A1', 'Hello..')
worksheet.write('B1', 'Geeks')
worksheet.write('C1', 'For')
worksheet.write('D1', 'Geeks')

#close the worksheet
workbook.close()
