import re

emailRegex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
passRegex = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{4,}$') 
nameRegex = re.compile(r'^[A-Za-z][A-Za-z0-9_]{3,19}$')

def emailValidator(email: str):
    """Check Valid email"""
    if re.fullmatch(emailRegex, email):
      return True
    else:
      return False

def passValidator(password: str):
    """
        Minimum 4 characters \n
        At least one letter \n
        At least one number \n
        At least one special character
    """
    if re.fullmatch(passRegex, password):
        return True
    else:
        return False

def nameValidator(name: str):
    """
        Minimum 4 characters \n
        First letter alpha \n
        Rest alphanumeric
    """
    if re.fullmatch(nameRegex, name):
        return True
    else:
        return False