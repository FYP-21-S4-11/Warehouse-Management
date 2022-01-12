from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError, TextAreaField, SearchField
from wtforms.validators import DataRequired, EqualTo, Length

# Create Login Form
class LoginForm(FlaskForm):
	username = StringField("Username:", validators=[DataRequired()], render_kw={"placeholder": "Enter Username"})
	password = PasswordField("Password:", validators=[DataRequired()], render_kw={"placeholder": "Enter Password"})
	submit = SubmitField("Login")

# ==================================
# Product Add Form
class ProductAddForm(FlaskForm):
	sku = StringField("SKU:", validators=[DataRequired()])
	name = StringField("Name:", validators=[DataRequired()])
	description = StringField("Description:", validators=[DataRequired()])
	producttype = StringField("Product Type:", validators=[DataRequired()])
	submit = SubmitField("Add Product")

# Product Update Form
class ProductUpdateForm(FlaskForm):
	sku = StringField("SKU:", validators=[DataRequired()])
	search = SubmitField("Search")
	name = StringField("Name:", validators=[DataRequired()])
	description = StringField("Description:", validators=[DataRequired()])
	producttype = StringField("Product Type:", validators=[DataRequired()])
	submit = SubmitField("Update Product")

# Product Delete Form
class ProductDeleteForm(FlaskForm):
	sku = StringField("SKU:", validators=[DataRequired()])
	submit = SubmitField("Delete Product")

# Product View Form
class ProductViewForm(FlaskForm):
	sku = StringField("SKU:", validators=[DataRequired()])
	submit = SubmitField("View Product")

# ==================================
# Supplier Add Form
class SupplierAddForm(FlaskForm):
	code = StringField("Code:", validators=[DataRequired()])
	name = StringField("Name:", validators=[DataRequired()])
	phone = StringField("Phone:", validators=[DataRequired()])
	address = StringField("Address:", validators=[DataRequired()])
	submit = SubmitField("Add Supplier")

# Supplier Update Form
class SupplierUpdateForm(FlaskForm):
	code = StringField("Code:", validators=[DataRequired()])
	search = SubmitField("Search")
	name = StringField("Name:", validators=[DataRequired()])
	phone = StringField("Phone:", validators=[DataRequired()])
	address = StringField("Address:", validators=[DataRequired()])
	submit = SubmitField("Update Supplier")

# Supplier Delete Form
class SupplierDeleteForm(FlaskForm):
	code = StringField("Code:", validators=[DataRequired()])
	submit = SubmitField("Delete Supplier")

# Supplier View Form
class SupplierViewForm(FlaskForm):
	code = StringField("Code:", validators=[DataRequired()])
	submit = SubmitField("View Supplier")

# ==================================
# Store Add Form
class StoreAdddForm(FlaskForm):
	code = StringField("Code:", validators=[DataRequired()])
	location = StringField("Location:" , validators=[DataRequired()])
	address = StringField("Address:", validators=[DataRequired()])
	submit = SubmitField("Add Store")

# Store Update Form
class StoreUpdateForm(FlaskForm):
	code = StringField("Code:", validators=[DataRequired()])
	location = StringField("Location:" , validators=[DataRequired()])
	address = StringField("Address:", validators=[DataRequired()])
	submit = SubmitField("Update Store")

# Store Delete Form
class StoreDeleteForm(FlaskForm):
	code = StringField("Code:", validators=[DataRequired()])
	submit = SubmitField("Delete Store")

# Store View Form
class StoreViewForm(FlaskForm):
	code = StringField("Code:", validators=[DataRequired()])
	submit = SubmitField("View Store")
