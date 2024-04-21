import cv2

def calculate(first_number,operator,second_number):
	a = int(first_number)
	b = int(second_number)
	if operator == "*":
		res = a * b
	elif operator == "/":
		res = a/b
	elif operator == "+":
		res = a + b
	elif operator == "%":
		res = a % b
	elif operator == "-":
		res = a - b
	elif operator == "**":
		res = a**b
	else:
		print("Not a valid operator")
	return res


