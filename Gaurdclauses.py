def Valid(email,password):
    if "@" not in email or type(email) != str:
        return "is not email"
    if type(password) != str: return "not a string"
    if len(password) < 8: return "password is not long enough"
    digit = 0
    upper = 0
    for char in password:
        if char == char.isupper():
            upper += 1
        if char == char.isdigit():
            digit += 1
        if upper > 0:
            return "your password needs at least 1 upper case letter"
        if digit > 0:
            return "your password requires at least 1 digit"

print(Valid("grfeweheoihgkh@gmail.com", "EefytErger4f3"))
