import os
from random import randint

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '&PkGWqfp?kFE9TDLw-URW=-P2tVou4QyMH4tJz2LP~BNGA!B7-siyfT.&inE:@*@' # Prevents CSRF attacks                                                                       # random key to prevent access through guessing port (for upload)
    PORT = 8787                                                                                                     # port to run server on