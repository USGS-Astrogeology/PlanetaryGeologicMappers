from wtforms import StringField, Form
from wtforms.validators import AnyOf, DataRequired
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
