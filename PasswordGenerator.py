import string, random

letters = string.ascii_letters
symbols = string.punctuation
digits = string.digits

all_symbols = letters + symbols + digits

def Generate(length:int = 12, count:int = 1, use_all_symbols:bool = False, only_letters:bool = False, letters_and_digits:bool = False) -> str:
    password = ""
    for n in range(count):
        if use_all_symbols == True:
            password += ''.join(random.choice(all_symbols) for i in range(length))
        elif only_letters == True:
            password += ''.join(random.choice(letters) for i in range(length))
        elif letters_and_digits == True:
            extra = letters + str(digits)
            password += ''.join(random.choice(extra) for i in range(length))
        else:
            password += ''.join(random.choice(digits) for i in range(length))
    return str(password)