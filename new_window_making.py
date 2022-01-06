
import tkinter as tk
import csv
from tkinter import font

import tkentrycomplete

def show() : 
    value = entryWidget.get()
    tk.Label(new_window, text=value).pack()
    value_list.append(value)

def func(event=None) :
    value = entryWidget.get()

    tk.Label(new_window, text= value).pack(fill=tk.BOTH)

def sample_func(event=None) : 
    value = combo.get()
    listBox.insert(tk.END,value)


def delete_from_list(event=None):
    # import pdb; pdb.set_trace()
    cursel = listBox.curselection()
    if cursel : 
        listBox.delete(cursel)

def submit_window() :
    key = entryWidget.get()
    value_list = list(listBox.get(0,tk.END))

    desigDict[key] = value_list
    print(desigDict)
    new_window.destroy()



###########################################################################

skills = []
f = open('skills.csv','r')
reader = csv.reader(f)

for row in reader : 
    skills.extend(row)
# print(skills)
f.close()

# !need to change desigDict = {}
desigDict = {}
value_list = []


###########################################################################

new_window = tk.Tk()
new_window.geometry('500x500+700+200')
new_window.title('Add New Designation')
# new_window.resizable(False,False)


newDesigLabel = tk.Label(new_window,text='Enter new designation : ')
newDesigLabel.pack(fill=tk.X,ipadx=10,ipady=10)

entryWidget = tk.Entry(new_window,font='helvetica',justify=tk.CENTER)
entryWidget.pack(fill=tk.X,ipadx=10,ipady=10)



comboBoxLabel = tk.Label(new_window, text='Select skills :',font=("Times", "14", "bold"))
comboBoxLabel.pack(fill=tk.X,ipadx=10,ipady=10)

tk.Label(new_window,text='- Press enter to add skills-',font=("Times", "14", "bold italic")).pack()

# ! using this autoomplete have a problem
# ! we are able to type into the box even if the string is not present in the list 
# ! Need to change it such that only elements that are available are considered
combo = tkentrycomplete.AutocompleteCombobox(new_window)
combo.set_completion_list(skills)
combo.pack(fill=tk.X,padx=10,pady=10)

listBox = tk.Listbox(new_window)
listBox.pack(fill=tk.X,ipadx=10,ipady=10)

deleteButton = tk.Button(new_window,text='Delete skill', command=delete_from_list)
deleteButton.pack(ipadx=5)

submitButton = tk.Button(new_window, text='Submit', command=submit_window)
submitButton.pack(side=tk.BOTTOM, padx=10, pady=10, ipadx=10, ipady=10)
# Set  the focus on entryWidget when code is run
# entryWidget.focus_set()


# tk.Label(new_window, text='Enter primary skills : ')

# box_value = tk.StringVar()
# combo = ttk.Combobox(new_window)

# # ! Need to add command to this button
# addSkillsButton = tk.Button(new_window,text='Add Skill')

# skillsSelected = tk.Listbox(new_window, height = 10, 
#                             width = 15, 
#                             bg = "grey",
#                             activestyle = 'dotbox', 
#                             font = "Helvetica",
#                             fg = "yellow")

# submitButton = tk.Button(new_window,text='Submit',command=show)




#############################################################################

entryWidget.bind('<Return>',func)
combo.bind('<Return>',sample_func)

new_window.bind('<Control-Q>', lambda event=None: new_window.destroy())
new_window.bind('<Control-q>', lambda event=None: new_window.destroy())

entryWidget.focus_set()

new_window.mainloop()
