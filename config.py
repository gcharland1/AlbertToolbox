import os

# Statement for enabling the development environment
DEBUG = False

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SERVER_NAME = "albert-toolbox.com"
# Define the database - we are working with
# SQLite for this example
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection against *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "secret"

# Mail service config
MAIL_SERVER = 'smtp.googlemail.com'

# If using SSL/TLS
#MAIL_PORT = 465
#MAIL_USE_SSL = True

# If using STARTTLS
MAIL_PORT = 587
MAIL_USE_TLS = True

MAIL_USERNAME = 'albert.toolbox@gmail.com'  # enter your email here
MAIL_DEFAULT_SENDER = 'albert.toolbox@gmail.com' # enter your email here
MAIL_PASSWORD = 'nrkjfggiucocwbxw' # enter your password here
