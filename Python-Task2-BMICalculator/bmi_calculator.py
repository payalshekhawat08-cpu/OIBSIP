print("-------- Body Mass Index Calculator --------")

while True:
    try:
        weight = float(input("Enter weight in kg: "))
        height = float(input("Enter height in meters: "))
    except ValueError:
        print("Invalid input. Please enter numbers only (e.g., 70 or 1.75).\n")
        continue

    if weight <= 0 or height <= 0:
        print("Weight and height must be positive values.\n")
        continue

    break

bmi = weight / (height ** 2)

if bmi < 18.5:
    category = "Underweight"
elif bmi < 25:
    category = "Normal"
elif bmi < 30:
    category = "Overweight"
else:
    category = "Obese"

print("YOUR BMI IS:", round(bmi, 2))
print("CATEGORY:", category) 