from flask_wtf import Form
from wtforms import SubmitField,PasswordField,StringField,validators
from wtforms.fields.html5 import DateTimeLocalField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_uploads import UploadSet, IMAGES


images = UploadSet('images', IMAGES)

class PwdForm(Form):

    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField("Password", [validators.Length(min=4, max=25)])
    submit = SubmitField("Login")


class PostForm(Form):

    title = StringField("Title")
    body = StringField("Body")
    post_image = FileField('image', validators=[FileAllowed(images, 'Images only!')])
    submit = SubmitField("Post")




class UserRegistration(Form):

    username = StringField("Username", [validators.required(True)])
    password = PasswordField("Password", [validators.required(True)])
    first_name = StringField("Name", [validators.required(True)])
    last_name = StringField("Last Name", [validators.required(True)])


    profile_pic = FileField('image', validators=[FileAllowed(images, 'Images only!')])


    email = StringField("Email", [validators.required(True)])
    submit = SubmitField("register", [validators.required(True)])

class DeleteButton(Form):
    id_hidden = StringField("Hidden Field")
    delete = SubmitField("delete")

class RegisterWeights(Form):

    time_date = DateTimeLocalField("Date And Time", [validators.required(True)], format='%Y-%m-%dT%H:%M')
    video = FileField("Video Proof", )
    weight = StringField("Weight", [validators.required(True)])
    submit = SubmitField("submit")