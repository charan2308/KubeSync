import yaml
from tkinter import filedialog,Tk
import os
with open("docker-compose.yaml") as f:
     list_doc = yaml.safe_load(f)

root = Tk()
root.withdraw()

file_path = filedialog.askdirectory()
base = os.path.basename(file_path)
newpath = file_path+':/app/files/'+base
print(newpath)
list_doc["services"]["back_me_up"]["volumes"][0] = newpath


with open("docker-compose.yaml", "w") as f:
    yaml.dump(list_doc, f)
os.system("docker compose up")  
