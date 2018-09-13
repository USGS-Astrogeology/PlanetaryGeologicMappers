from wtforms import TextField, StringField, Form, PasswordField
from wtforms.validators import AnyOf, DataRequired, required
from wtforms.widgets import TextArea

class PageForm(Form):
    page_title = StringField(u"Title",
                             [DataRequired(message = "No webpage title given.")],
                             widget = TextArea())

    page_name = StringField(u"Name",
                            [DataRequired(message = "No webpage name given.")],
                            widget = TextArea())

    page_content = StringField(u"Content",
                               [DataRequired(message = "No webpage content given.")],
                               widget = TextArea())

class LoginForm(Form):
    admin_name = TextField(u'Admin Name', [required()])
    admin_password = PasswordField(u'Admin Password', [required()])
