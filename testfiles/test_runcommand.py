import subprocess

def run_command(filename, language, location = '' ):
    if(language == 'python'):
        return 'python '+ location + filename + '.py'

command = run_command('ide4','python', 'E:/tranfer/MainProject/MainProject/')
print(command)

result = subprocess.run(['cmd.exe', '/c', command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
print (result)