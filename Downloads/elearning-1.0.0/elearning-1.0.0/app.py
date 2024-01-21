from __future__ import division, print_function

# coding=utf-8
import os
import tensorflow as tf
from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField

import numpy as np
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession

config = ConfigProto()
config.gpu_options.per_process_gpu_memory_fraction = 0.2
config.gpu_options.allow_growth = True
session = InteractiveSession(config=config)

# Keras
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

print("tensorflow ver")
print(tf.__version__)
# Flask utils
from flask import request, render_template
from flask import Flask
from werkzeug.utils import secure_filename
#from gevent.pywsgi import WSGIServer
# Define a flask app
app = Flask(__name__)
app = Flask(__name__, template_folder='templates')
app = Flask(__name__, static_folder='static')
@app.route("/")
def Index():
    return render_template('index.html')

@app.route("/Home")
def Home():
    return render_template('index.html')

@app.route("/About")
def About():
    return render_template('form.html')


@app.route("/Blog")
def Blog():
    return render_template('form.html')

@app.route("/Login")
def Login():
    return render_template('login.html')


@app.route("/Predict")
def Predict():
    return render_template('predict.html')


class StudentForm(FlaskForm):
    maritalStatus = SelectField('Marital Status', choices=[('1', 'Single'), ('2', 'Married'), ('3', 'Widower'), ('4', 'Divorced'), ('5', 'Facto union'), ('6', 'Legally separated')], coerce=int)
    course = SelectField('Course', choices=[('1', 'Biofuel Production Technologies'), ('2', 'Animation and Multimedia Design'), ('3', 'Social Service (evening attendance)'), ('4', 'Agronomy'), ('5', 'Communication Design'), ('6', 'Veterinary Nursing'), ('7', 'Informatics Engineering'), ('8', 'Equiniculture'), ('9', 'Management'), ('10', 'Social Service'), ('11', 'Tourism'), ('12', 'Nursing'), ('13', 'Oral Hygiene'), ('14', 'Advertising and Marketing Management'), ('15', 'Journalism and Communication'), ('16', 'Basic Education'), ('17', 'Management (evening attendance)')], coerce=int)
    prevQualification = SelectField('Previous Qualification', choices=[('1', 'Secondary education'), ('2', 'Higher education—bachelor’s degree'), ('3', 'Higher education—degree'), ('4', 'Higher education—master’s degree'), ('5', 'Higher education—doctorate'), ('6', 'Frequency of higher education'), ('7', '12th year of schooling—not completed'), ('8', '11th year of schooling—not completed'), ('9', 'Other—11th year of schooling'), ('10', '10th year of schooling'), ('11', '10th year of schooling—not completed'), ('12', 'Basic education 3rd cycle (9th/10th/11th year) or equivalent'), ('13', 'Basic education 2nd cycle (6th/7th/8th year) or equivalent'), ('14', 'Technological specialization course'), ('15', 'Higher education—degree (1st cycle)'), ('16', 'Professional higher technical course'), ('17', 'Higher education—master’s degree (2nd cycle)')], coerce=int)
    motherOccupation = SelectField("Mother's Occupation", choices=[('1', 'Student'), ('2', 'Representatives of the Legislative Power and Executive Bodies, Directors, Directors and Executive Managers'), ('3', 'Specialists in Intellectual and Scientific Activities'), ('4', 'Intermediate Level Technicians and Professions'), ('5', 'Administrative staff'), ('6', 'Personal Services, Security and Safety Workers, and Sellers'), ('7', 'Farmers and Skilled Workers in Agriculture, Fisheries, and Forestry'), ('8', 'Skilled Workers in Industry, Construction, and Craftsmen'), ('9', 'Installation and Machine Operators and Assembly Workers'), ('10', 'Unskilled Workers'), ('11', 'Armed Forces Professions'), ('12', 'Other Situation'), ('13', '(blank)'), ('14', 'Armed Forces Officers'), ('15', 'Armed Forces Sergeants'), ('16', 'Other Armed Forces personnel'), ('17', 'Directors of administrative and commercial services'), ('18', 'Hotel, catering, trade, and other services directors'), ('19', 'Specialists in the physical sciences, mathematics, engineering, and related techniques'), ('20', 'Health professionals'), ('21', 'Teachers'), ('22', 'Specialists in finance, accounting, administrative organization, and public and commercial relations'), ('23', 'Intermediate level science and engineering technicians and professions'), ('24', 'Technicians and professionals of intermediate level of health'), ('25', 'Intermediate level technicians from legal, social, sports, cultural, and similar services'), ('26', 'Information and communication technology technicians'), ('27', 'Office workers, secretaries in general, and data processing operators'), ('28', 'Data, accounting, statistical, financial services, and registry-related operators'), ('29', 'Other administrative support staff'), ('30', 'Personal service workers'), ('31', 'Sellers'), ('32', 'Personal care workers and the like'), ('33', 'Protection and security services personnel'), ('34', 'Market-oriented farmers and skilled agricultural and animal production workers'), ('35', 'Farmers, livestock keepers, fishermen, hunters and gatherers, and subsistence'), ('36', 'Skilled construction workers and the like, except electricians'), ('37', 'Skilled workers in metallurgy, metalworking, and similar'), ('38', 'Skilled workers in electricity and electronics'), ('39', 'Workers in food processing, woodworking, and clothing and other industries and crafts'), ('40', 'Fixed plant and machine operators'), ('41', 'Assembly workers'), ('42', 'Vehicle drivers and mobile equipment operators'), ('43', 'Unskilled workers in agriculture, animal production, and fisheries and forestry'), ('44', 'Unskilled workers in extractive industry, construction, manufacturing, and transport'), ('45', 'Meal preparation assistants'), ('46', 'Street vendors (except food) and street service providers')], coerce=int)
    fatherOccupation = SelectField("Father's Occupation", choices=[('1', 'Student'), ('2', 'Representatives of the Legislative Power and Executive Bodies, Directors, Directors and Executive Managers'), ('3', 'Specialists in Intellectual and Scientific Activities'), ('4', 'Intermediate Level Technicians and Professions'), ('5', 'Administrative staff'), ('6', 'Personal Services, Security and Safety Workers, and Sellers'), ('7', 'Farmers and Skilled Workers in Agriculture, Fisheries, and Forestry'), ('8', 'Skilled Workers in Industry, Construction, and Craftsmen'), ('9', 'Installation and Machine Operators and Assembly Workers'), ('10', 'Unskilled Workers'), ('11', 'Armed Forces Professions'), ('12', 'Other Situation'), ('13', '(blank)'), ('14', 'Armed Forces Officers'), ('15', 'Armed Forces Sergeants'), ('16', 'Other Armed Forces personnel'), ('17', 'Directors of administrative and commercial services'), ('18', 'Hotel, catering, trade, and other services directors'), ('19', 'Specialists in the physical sciences, mathematics, engineering, and related techniques'), ('20', 'Health professionals'), ('21', 'Teachers'), ('22', 'Specialists in finance, accounting, administrative organization, and public and commercial relations'), ('23', 'Intermediate level science and engineering technicians and professions'), ('24', 'Technicians and professionals of intermediate level of health'), ('25', 'Intermediate level technicians from legal, social, sports, cultural, and similar services'), ('26', 'Information and communication technology technicians'), ('27', 'Office workers, secretaries in general, and data processing operators'), ('28', 'Data, accounting, statistical, financial services, and registry-related operators'), ('29', 'Other administrative support staff'), ('30', 'Personal service workers'), ('31', 'Sellers'), ('32', 'Personal care workers and the like'), ('33', 'Protection and security services personnel'), ('34', 'Market-oriented farmers and skilled agricultural and animal production workers'), ('35', 'Farmers, livestock keepers, fishermen, hunters and gatherers, and subsistence'), ('36', 'Skilled construction workers and the like, except electricians'), ('37', 'Skilled workers in metallurgy, metalworking, and similar'), ('38', 'Skilled workers in electricity and electronics'), ('39', 'Workers in food processing, woodworking, and clothing and other industries and crafts'), ('40', 'Fixed plant and machine operators'), ('41', 'Assembly workers'), ('42', 'Vehicle drivers and mobile equipment operators'), ('43', 'Unskilled workers in agriculture, animal production, and fisheries and forestry'), ('44', 'Unskilled workers in extractive industry, construction, manufacturing, and transport'), ('45', 'Meal preparation assistants'), ('46', 'Street vendors (except food) and street service providers')], coerce=int)
    gender = SelectField('Gender', choices=[('1', 'Male'), ('0', 'Female')], coerce=int)
    displaced = SelectField('Displaced', choices=[('1', 'Yes'), ('0', 'No')], coerce=int)
    specialNeeds = SelectField('Educational Special Needs', choices=[('1', 'Yes'), ('0', 'No')], coerce=int)
    debtor = SelectField('Debtor', choices=[('1', 'Yes'), ('0', 'No')], coerce=int)
    tuitionUpToDate = SelectField('Tuition Fees Up to Date', choices=[('1', 'Yes'), ('0', 'No')], coerce=int)
    scholarshipHolder = SelectField('Scholarship Holder', choices=[('1', 'Yes'), ('0', 'No')], coerce=int)
    international = SelectField('International', choices=[('1', 'Yes'), ('0', 'No')], coerce=int)
    submit = SubmitField('Submit')

# Load the pre-trained model
# model = load_model('trained_model.h5')

# # Function to preprocess form data and make predictions
# def preprocess_and_predict(data):
#     # Convert form data to numpy array
#     input_data = np.array(list(data.values())).astype(float).reshape(1, -1)

#     # Make predictions
#     prediction = model.predict_classes(input_data)

#     # Map prediction values to corresponding labels
#     labels = {0: 'Dropped', 1: 'Enrolled', 2: 'Graduated'}
#     result = labels[prediction[0]]

#     return result

# @app.route('/About', methods=['GET', 'POST'])
# def index():
#     form = StudentForm()
#     if form.validate_on_submit():
#         result = preprocess_and_predict(request.form)
#         return render_template('result.html', result=result)
#     return render_template('index.html', form=form)

app.run(debug=True)
if __name__ == '_app_':
    app.run(port=5000,debug=True)