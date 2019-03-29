from flask import Flask,\
                  render_template, \
                  flash, \
                  request, \
                  session, \
                  redirect, \
                  url_for

from flask_recaptcha import ReCaptcha
from functools import wraps
 

import gc
import os
import datetime

# -------- app initialization ----------------
app = Flask(__name__)
app.config.update(
    dict(
        SECRET_KEY=b'samplekey2019',
        SECURITY_PASSWORD_SALT='samplekey2019'
    )
)

# Login
@app.route('/', methods = ['GET','POST'])
def main():
    try:

        return render_template("form.html")
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    app.run(debug=False)