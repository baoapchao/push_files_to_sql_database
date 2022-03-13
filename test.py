import os

path = r'C:\Users\ADMIN\OneDrive\Study\Jupyter Notebook'
# print(os.path.basename(os.path.dirname(path)))
# print(os.path.basename(path))

dirs = path.split(sep='\\')
# print('\\'.join(dirs[:-1]))
# print(dirs[-1])
# print(os.sep)

path = r'C:\Users\ADMIN\OneDrive\Study\Jupyter Notebook'

dirs = path.split(sep='\\')
# print(dirs)

path = os.getcwd()

print(os.path.join(path, 'ABC', 'DEF'))