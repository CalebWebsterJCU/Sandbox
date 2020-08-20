"""This program gets a password from the user and prints asterisks as long as the password."""
MINIMUM_LENGTH = 5
password = input("Enter password: ")
length = len(password)
while length < 5:
    print("Invalid password")
    password = input("Enter password: ")
    length = len(password)

print("*" * length)
