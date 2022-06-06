import string
import random

def generate(password_length= 8, have_uppercase= True, have_lowercase= True, have_symbol= True, have_number= True):
    """Generates a password"""
    counter = 0
    password = ''
    
    while counter != password_length:
        random_item = random.choice(list(range(4)))

        match random_item:
            case 0:
                if have_uppercase == True:
                    password += random.choice(string.ascii_uppercase)
                    counter += 1
                    continue
            case 1:
                if have_lowercase == True:
                    password += random.choice(string.ascii_lowercase)
                    counter += 1
                    continue
            case 2:
                if have_symbol == True:
                    password += random.choice(string.punctuation)
                    counter += 1
                    continue
            case 3:
                if have_number == True:
                    password += random.choice(string.digits)
                    counter += 1
                    continue

    return password
