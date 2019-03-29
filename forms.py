from wtforms import Form, \
					TextField, \
					SelectField, \
                    SelectMultipleField, \
					BooleanField, \
					TextAreaField, \
					SubmitField, \
					FormField, \
					validators

# for custom multiselect checkbox
from wtforms.widgets import ListWidget, CheckboxInput

# for file upload
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed

# regular expression
import re

# list declaration
list_of_affiliation = [
    ('None', '----- Select Affiliation -----'),
	('S1', 'School A'),
	('S2', 'School B'),
	('S3', 'School C'),
	('S4', 'School D')
]

valid_affiliation = ['S1','S2','S3','S4']

list_of_categories = [
    ('C1', 'Cat 1'),
	('C2', 'Cat 2'), 
	('C3', 'Cat 3'), 
	('C4', 'Cat 4'), 
	('C5', 'Cat 5')
]


class MultiCheckboxField(SelectMultipleField):
	widget = ListWidget(prefix_label=False)
	option_widget = CheckboxInput()


class CatSubForm(Form):

	select_section = MultiCheckboxField("One or More: ", 
									   [validators.Required()], 
									   choices=list_of_categories)

	others_section = TextField("Others: ", 
							 [], 
							 render_kw={"placeholder":"Enter up to three keywords (format example: keyword1;keyword2;keyword3)","class":"form-control"})

    # custom validator
	def validate(self):

		isValidated = True

		rv = FlaskForm.validate(self)

		if not rv:
			isValidated = False

		if self.secondsection.data:

			pattern = re.compile('^[a-z\s]+(?:;[a-z\s]+)*$')
            
            # check if user entered one more ;
			if self.secondsection.data.endswith(';'):
				self.secondsection.data = self.secondsection.data[:-1]
			
			if pattern.match(self.secondsection.data):
				keywords_str = self.secondsection.data
				keywords_list = keywords_str.split(';')
				keywords_list = [x.strip() for x in keywords_list if x]

                # if user entered more than 3 keywords
				if len(keywords_list) > 3:
					self.secondsection.errors.append('You have entered more than 3 keyphrases!')
					isValidated = False
			else:
                # if format is wrong
				self.secondsection.errors.append('Please use only small letters, semicolon and space for this field')
				isValidated = False

		return isValidated


class MainForm(Form):

    _title = TextField('Team Name', 
                       [validators.Required(), validators.Length(max=100, message="Keep length under 100 characters!")], 
                       render_kw={"placeholder":"Enter a title", "class":"form-control"})

    _description = TextAreaField('Description',
								  [validators.Required(), validators.Length(max=3000, message="Keep length under 3000 characters!")], 
								  render_kw={"placeholder":"Tell us more about your project", "class":"form-control"})

    _affiliation = SelectField('Affiliation',
                               choices=list_of_affiliation,
                               validators=[validators.AnyOf(valid_affiliation, message="Please use a valid choice!")],
                               render_kw={"class":"form-control"})

    _categories = FormField(CatSubForm, label='Category')

    _terms = BooleanField('Agree to terms and conditions', 
								  [validators.Required()], 
								  render_kw={"class":"form-control"})

    _submit = SubmitField(label="Submit", 
						  render_kw={"class":"btn btn-primary btn-sm"})






