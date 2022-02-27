from questionnaire import *
import xlsxwriter
from flask import Flask
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
workbook = xlsxwriter.Workbook('moeed.xlsx')

#adds new worksheet
worksheet = workbook.add_worksheet()

# Use the worksheet object to write
# data via the write() method.
#worksheet.write('A1', 'Hello..')
#worksheet.write('B1', 'Geeks')
#worksheet.write('C1', 'For')
#worksheet.write('D1', 'Geeks')

# Set up some formats to use.
red = workbook.add_format({'color': 'red'})
blue = workbook.add_format({'color': 'blue'})
cell_format = workbook.add_format({'align': 'center',
                                   'valign': 'vcenter',
                                   'border': 2, 'bold': True})
weekCellFormat = workbook.add_format({'align': 'center',
                                   'valign': 'vcenter','bold': True, })
weekCellFormat.set_font_size(10)

# We can only write simple types to merged ranges so we write a blank string.
worksheet.merge_range('A1:K3', "", cell_format)#-----WEEK X
worksheet.write('A1', u'DAY 1',cell_format)


worksheet.merge_range('A5:B5', "", cell_format)#-----DAY X
worksheet.merge_range('D5:E5', "", cell_format)#-----DAY X
worksheet.merge_range('G5:H5', "", cell_format)#-----DAY X
worksheet.merge_range('J5:K5', "", cell_format)#-----DAY X

# We then overwrite the first merged cell with a rich string. Note that we
# must also pass the cell format used in the merged cells format at the end.
worksheet.write_rich_string('B2',
                            'This is ',
                            red, 'red',
                            ' and this is ',
                            blue, 'blue',
                            cell_format)
#close the worksheet
workbook.close()

if (__name__ == "__main__"):
    app.run(debug=True)
