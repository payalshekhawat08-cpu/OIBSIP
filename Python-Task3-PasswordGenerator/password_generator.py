import random
import string

print("------RANDOM PASSWORD GENERATOR------")

while True:

    try:
        length = int(input("Enter password length (min 8): "))

        if length < 8:
            print("Error! Password must be 8 or more.")
            continue

    except ValueError:
        print("Error! Please enter a valid number.")
        continue

    print("Choose character type to include (y/n)")

    use_upper = input("Upper case letters (A-Z)? ").strip().lower() == "y"
    use_lower = input("Lower case letters (a-z)? ").strip().lower() == "y"
    use_numbers = input("Numbers (0-9)? ").strip().lower() == "y"
    use_symbols = input("Symbols (!,@,#,$,%,^,&,*)? ").strip().lower() == "y"

    selected_types = sum([
        use_upper,
        use_lower,
        use_numbers,
        use_symbols
    ])

    if selected_types < 2:
        print("\nERROR! You must select at least two character types")
        continue

    characters = ""
    password = []

    if use_upper:
        characters += string.ascii_uppercase
        password.append(random.choice(string.ascii_uppercase))

    if use_lower:
        characters += string.ascii_lowercase
        password.append(random.choice(string.ascii_lowercase))

    if use_numbers:
        characters += string.digits
        password.append(random.choice(string.digits))

    if use_symbols:
        symbols = "!@#$%^&*"
        characters += symbols
        password.append(random.choice(symbols))

    while len(password) < length:
        password.append(random.choice(characters))

    random.shuffle(password)

    print("\nGenerated password")
    print("".join(password))

    again = input("\nGenerate another password? (y/n): ").strip().lower()

    if again != "y":
        print("Thank you for using password generator!")
        break