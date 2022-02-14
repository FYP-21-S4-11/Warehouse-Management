from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, TextAreaField, SearchField, IntegerField, DateField, SelectField
from wtforms.validators import DataRequired, EqualTo, Length
from flask.views import View

# Create Login Form
class LoginForm(FlaskForm):
	username = StringField("Username:", validators=[DataRequired()], render_kw={"placeholder": "Enter Username"})
	password = PasswordField("Password:", validators=[DataRequired()], render_kw={"placeholder": "Enter Password"})
	type = SelectField("Log In As:", render_kw={"placeholder": "Enter User Type"}, choices=["Admin", "Supervisor"])
	submit = SubmitField("Login")

# ==================================
# Product Add Form
class ProductAddForm(FlaskForm):
	sku = StringField("Product SKU:", validators=[DataRequired()], render_kw={"placeholder": "Enter Product SKU..."})
	name = StringField("Product Name:", validators=[DataRequired()], render_kw={"placeholder": "Enter Product Name..."})
	description = StringField("Description:", validators=[DataRequired()], render_kw={"placeholder": "Enter Description..."})
	producttype = StringField("Product Type:", validators=[DataRequired()], render_kw={"placeholder": "Enter Product Type..."})

# Product Update Form
class ProductUpdateForm(FlaskForm):
	sku = StringField("Product SKU:", validators=[DataRequired()], render_kw={"placeholder": "Enter Product SKU..."})
	name = StringField("Product Name:", validators=[DataRequired()], render_kw={"placeholder": "Enter Product Name..."})
	description = StringField("Description:", validators=[DataRequired()], render_kw={"placeholder": "Enter Description..."})
	producttype = StringField("Product Type:", validators=[DataRequired()], render_kw={"placeholder": "Enter Product Type..."})

# Product Delete Form
class ProductDeleteForm(FlaskForm):
	sku = StringField("Product SKU:", validators=[DataRequired()], render_kw={"placeholder": "Enter Product SKU..."})

# ==================================
# Supplier Add Form
class SupplierAddForm(FlaskForm):
	code = StringField("Supplier Code:", validators=[DataRequired()], render_kw={"placeholder": "Enter Supplier Code..."})
	name = StringField("Supplier Name:", validators=[DataRequired()], render_kw={"placeholder": "Enter Supplier Name..."})
	password = StringField("Supplier Password:", validators=[DataRequired()], render_kw={"placeholder": "Enter Supplier Password..."})
	phone = StringField("Supplier Phone:", validators=[DataRequired()], render_kw={"placeholder": "Enter Supplier Phone..."})
	address = StringField("Supplier Address:", validators=[DataRequired()], render_kw={"placeholder": "Enter Supplier Address..."})

# Supplier Update Form
class SupplierUpdateForm(FlaskForm):
	code = StringField("Supplier Code:", validators=[DataRequired()], render_kw={"placeholder": "Enter Supplier Code..."})
	name = StringField("Supplier Name:", validators=[DataRequired()], render_kw={"placeholder": "Enter Supplier Name..."})
	password = StringField("Supplier Password:", validators=[DataRequired()], render_kw={"placeholder": "Enter Supplier Password..."})
	phone = StringField("Supplier Phone:", validators=[DataRequired()], render_kw={"placeholder": "Enter Supplier Phone..."})
	address = StringField("Supplier Address:", validators=[DataRequired()], render_kw={"placeholder": "Enter Supplier Address..."})

# Supplier Delete Form
class SupplierDeleteForm(FlaskForm):
	code = StringField("Supplier Code:", validators=[DataRequired()], render_kw={"placeholder": "Enter Supplier Code..."})

# ==================================
# Store Add Form
class StoreAddForm(FlaskForm):
	code = StringField("Store Code:", validators=[DataRequired()], render_kw={"placeholder": "Enter Store Code..."})
	location = StringField("Location:" , validators=[DataRequired()], render_kw={"placeholder": "Enter Location..."})
	address = StringField("Address:", validators=[DataRequired()], render_kw={"placeholder": "Enter Address..."})

# Store Update Form
class StoreUpdateForm(FlaskForm):
	code = StringField("Store Code:", validators=[DataRequired()], render_kw={"placeholder": "Enter Store Code..."})
	location = StringField("Location:" , validators=[DataRequired()], render_kw={"placeholder": "Enter Location..."})
	address = StringField("Address:", validators=[DataRequired()], render_kw={"placeholder": "Enter Address..."})

# Store Delete Form
class StoreDeleteForm(FlaskForm):
	code = StringField("Store Code:", validators=[DataRequired()], render_kw={"placeholder": "Enter Store Code..."})

# ==================================
# Admin Add Form
class AdminAddForm(FlaskForm):
	name = StringField("Name:", validators=[DataRequired()], render_kw={"placeholder": "Enter Name..."})
	username = StringField("Username:", validators=[DataRequired()], render_kw={"placeholder": "Enter Username..."})
	password = StringField("Admin Password:", validators=[DataRequired()], render_kw={"placeholder": "Enter Password..."})
	phone = StringField("Admin Phone:", validators=[DataRequired()], render_kw={"placeholder": "Enter Phone..."})
	address = StringField("Admin Address:", validators=[DataRequired()], render_kw={"placeholder": "Enter Address..."})
	email = StringField("Admin Email:", validators=[DataRequired()], render_kw={"placeholder": "Enter Email..."})

# Admin Update Form
class AdminUpdateForm(FlaskForm):
	name = StringField("Name:", validators=[DataRequired()], render_kw={"placeholder": "Enter Name..."})
	username = StringField("Username:", validators=[DataRequired()], render_kw={"placeholder": "Enter Username..."})
	password = StringField("Admin Password:", validators=[DataRequired()], render_kw={"placeholder": "Enter Password..."})
	phone = StringField("Admin Phone:", validators=[DataRequired()], render_kw={"placeholder": "Enter Phone..."})
	address = StringField("Admin Address:", validators=[DataRequired()], render_kw={"placeholder": "Enter Address..."})
	email = StringField("Admin Email:", validators=[DataRequired()], render_kw={"placeholder": "Enter Email..."})

# Admin Delete Form
class AdminDeleteForm(FlaskForm):
	username = StringField("Username", validators=[DataRequired()], render_kw={"placeholder": "Enter Username..."})

# ==================================
