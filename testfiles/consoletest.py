import subprocess

# Run a command and capture its output
# :\tranfer\Main Project260324\Main Project\mainproj
result = subprocess.run(['cmd.exe', '/c', 'E:'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
print(result)
result = subprocess.run(['cmd.exe', '/c', 'cd', '/tranfer/MainProject/MainProject/mainproj'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
print(result)
result = subprocess.run(['cmd.exe', '/c', 'python', 'test.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# Print the output
print(result.stdout)

# Print any errors
if result.stderr:
    print("Error:", result.stderr)
