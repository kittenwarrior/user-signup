import webapp2
import cgi
import re

page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>User Signup</title>
    <style type="text/css">
        .error {
            color: red;
        }
    </style>
</head>
<body>
    <h1>Signup</h1>
"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")


def validate_username(username):
    return USER_RE.match(username)


def validate_password(password):
    return PASS_RE.match(password)


def validate_email(email):
    return EMAIL_RE.match(email)


def validate_passmatch(password, passwordverify):
    return password == passwordverify


def signup_form(valid_username=True, valid_password=True,
                password_match = True, valid_email=True, username="", email=""):
    user_valid_error = ""
    pass_match_error = ""
    pass_valid_error = ""
    email_valid_error = ""


    if not valid_username:
        user_valid_error = "That's not a valid username."

    if valid_password and not password_match:
        pass_match_error = "Your passwords didn't match."

    if not valid_password:
        pass_valid_error = "That wasn't a valid password."

    if not valid_email:
        email_valid_error = "That's not a valid email."

    form_content = """
    <form action="/" method="post">
        <label>
            Username
            <input type="text" name="username" value="%s"/>
            <span class="error">%s</span>
            <br>
            Password
            <input type="password" name="password"/>
            <span class="error">%s</span>
            <br>
            Verify Password
            <input type="password" name="passwordv"/>
            <span class="error">%s</span>
            <br>
            Email (Optional)
            <input name='emailaddress' type='text' value="%s">
            <span class="error">%s</span>
            <br>
        </label>
        <input type="submit" value="Submit"/>
    </form>
    """ % (username, user_valid_error, pass_valid_error, pass_match_error, email, email_valid_error)

    return form_content



class MainHandler(webapp2.RequestHandler):
    def get(self):

        self.response.write(page_header + signup_form())


    def post(self):

        username = self.request.get("username")
        password = self.request.get("password")
        passwordverify = self.request.get("passwordv")
        email = self.request.get("emailaddress")

        if all([
            validate_username(username),
            validate_password(password),
            validate_passmatch(password, passwordverify),
            validate_email(email)
        ]):
            self.redirect("/welcome?username=" + username)
        else:
            form_content = signup_form(
                validate_username(username),
                validate_password(password),
                validate_passmatch(password, passwordverify),
                validate_email(email),
                username,
                email
            )
            self.response.write(page_header + form_content)

class WelcomeHandler(webapp2.RequestHandler):

    def get(self):
        username = self.request.get("username")

        # validating username


        self.response.write("<h1>Welcome, " + username + "!</h1>")


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', WelcomeHandler)
], debug=True)
