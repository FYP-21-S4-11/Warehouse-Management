from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, TextAreaField, SearchField
from wtforms.validators import DataRequired, EqualTo, Length
from flask.views import View

# Create Login Form
class LoginForm(FlaskForm):
	username = StringField("Username:", validators=[DataRequired()], render_kw={"placeholder": "Enter Username"})
	password = PasswordField("Password:", validators=[DataRequired()], render_kw={"placeholder": "Enter Password"})
	submit = SubmitField("Login")

# ==================================
# Product Add Form
class ProductAddForm(FlaskForm):
	sku = StringField("SKU:", validators=[DataRequired()])
	name = StringField("Product Name:", validators=[DataRequired()])
	description = StringField("Description:", validators=[DataRequired()])
	producttype = StringField("Product Type:", validators=[DataRequired()])

# Product Update Form
class ProductUpdateForm(FlaskForm):
	sku = StringField("SKU:", validators=[DataRequired()])
	name = StringField("Product Name:", validators=[DataRequired()])
	description = StringField("Description:", validators=[DataRequired()])
	producttype = StringField("Product Type:", validators=[DataRequired()])

# Product Delete Form
class ProductDeleteForm(FlaskForm):
	sku = StringField("SKU:", validators=[DataRequired()], render_kw={"placeholder": "Enter SKU..."})

# Product Search Form
class ProductSearchForm(FlaskForm):
	sku = StringField("SKU:", validators=[DataRequired()], render_kw={"placeholder": "Enter SKU..."})

# ==================================
# Supplier Add Form
class SupplierAddForm(FlaskForm):
	code = StringField("Code:", validators=[DataRequired()])
	name = StringField("Supplier Name:", validators=[DataRequired()])
	phone = StringField("Supplier Phone:", validators=[DataRequired()])
	address = StringField("Supplier Address:", validators=[DataRequired()])

# Supplier Update Form
class SupplierUpdateForm(FlaskForm):
	code = StringField("Code:", validators=[DataRequired()])
	name = StringField("Supplier Name:", validators=[DataRequired()])
	phone = StringField("Supplier Phone:", validators=[DataRequired()])
	address = StringField("Supplier Address:", validators=[DataRequired()])

# Supplier Delete Form
class SupplierDeleteForm(FlaskForm):
	code = StringField("Code:", validators=[DataRequired()], render_kw={"placeholder": "Enter Code..."})

# Supplier Search Form
class SupplierSearchForm(FlaskForm):
	code = StringField("Code:", validators=[DataRequired()], render_kw={"placeholder": "Enter Code..."})

# ==================================
# Store Add Form
class StoreAddForm(FlaskForm):
	code = StringField("Code:", validators=[DataRequired()])
	location = StringField("Location:" , validators=[DataRequired()])
	address = StringField("Address:", validators=[DataRequired()])

# Store Update Form
class StoreUpdateForm(FlaskForm):
	code = StringField("Code:", validators=[DataRequired()])
	location = StringField("Location:" , validators=[DataRequired()])
	address = StringField("Address:", validators=[DataRequired()])

# Store Delete Form
class StoreDeleteForm(FlaskForm):
	code = StringField("Code:", validators=[DataRequired()], render_kw={"placeholder": "Enter Code..."})

# Store Search Form
class StoreSearchForm(FlaskForm):
	code = StringField("Code:", validators=[DataRequired()], render_kw={"placeholder": "Enter Code..."})


# ==================================
# Admin Add Form
class AdminAddForm(FlaskForm):
	name = StringField("Name:", validators=[DataRequired()])
	username = StringField("Username:", validators=[DataRequired()])
	password = PasswordField("Admin Password:", validators=[DataRequired()])
	phone = StringField("Admin Phone:", validators=[DataRequired()])
	address = StringField("Admin Address:", validators=[DataRequired()])
	email = StringField("Admin Email:", validators=[DataRequired()])

# Admin Update Form
class AdminUpdateForm(FlaskForm):
	name = StringField("Name:", validators=[DataRequired()])
	username = StringField("Username:", validators=[DataRequired()])
	password = PasswordField("Admin Password:", validators=[DataRequired()])
	phone = StringField("Admin Phone:", validators=[DataRequired()])
	address = StringField("Admin Address:", validators=[DataRequired()])
	email = StringField("Admin Email:", validators=[DataRequired()])

# Admin Delete Form
class AdminDeleteForm(FlaskForm):
	username = StringField("Username", validators=[DataRequired()], render_kw={"placeholder": "Enter Username..."})

# Admin Search Form
class AdminSearchForm(FlaskForm):
	username = StringField("Username", validators=[DataRequired()], render_kw={"placeholder": "Enter Username..."})

# ==================================
# Inventory In

# Inventory Out