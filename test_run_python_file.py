from functions.run_python_file import run_python_file

test_1 = run_python_file("calculator", "main.py")
print("Running test_1")
print(test_1)

test_2 = run_python_file("calculator", "main.py", ["3 + 5"])
print("Running test_2")
print(test_2)

test_3 = run_python_file("calculator", "tests.py")
print("Running test_3")
print(test_3)

test_4 = run_python_file("calculator", "../main.py")
print("Running test_4") 
print(test_4)

test_5 = run_python_file("calculator", "nonexistent.py")
print("Running test_5")
print(test_5)

test_6 = run_python_file("calculator", "lorem.txt")
print("Running test_6")
print(test_6)