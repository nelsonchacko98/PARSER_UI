import tkinter as tk
from tkinter import Listbox, ttk
import os
from download_attachments import  download_resumes
from dcube_resume_parser import parser
import glob
import pickle
import json
import csv
import tkentrycomplete

""" PHASE-1 PART THIS IS NOT THE COMPLETE PRODUCT
    WORKING IN A BRANCH """

__version__ = "3.1"

"""
BETTER COMMENT
--------------------
!deprecated
*important
?doubt
TODO - somthing to be done
--------------------
"""

# TODO: Check for credentials file. If not available handle it somehow


# Functions 

def download_attachments() : 

    # ! The app is requesting for complete access of the gmail inbox, when it only requires inbox email view and download rights
    # TODO : Change scope for email access. Need on read rights
    resumes = download_resumes()

    if not resumes : 
        # !USE ``download_resumes_gui(textLabel)``` to display and not this function
        textLabel.insert('1.0','NO EMAILS TO DOWNLOAD')
        return None

    files = glob.glob('downloads/confirm_resume_folder/*.pdf')

    display_list(files)
    return None


# ! Double click can be only bind to one function, make sure all file types and every single way of opening is handled
# ! eg. tried to double click a pdf resume. Since it is not handled by the following function it returned an error
def print_selected_item(event=None) : 
    selectedDesig = desig.get()
    print(selectedDesig)
    return None

def delete_designation() : 
    global desigDict
    selectedDesig = desig.get()
    if selectedDesig : 
        del desigDict[selectedDesig]
    return None


def show_matching_files() : 
    selectedDesig = desig.get()
    skillsNeeded = desigDict[selectedDesig]
    filesMatched = []

    files = glob.glob("json_out\*.json")

    for file in files:
        file_name = file.split("\\")[-1]
        with open(file, 'r') as j:
            contents = json.loads(j.read())

        skillsFromResume = contents['skills']
        commonSkills = list(set(skillsNeeded).intersection(skillsFromResume))

        if len(commonSkills)>2 :
            filesMatched.append(file)

    display_list(filesMatched)
    return None


def clear_data():
    listBoxView.delete(0,'end')
    return None

def clear_text_widget() : 
    textLabel.delete(1.0,'end')
    return None


# This fucntion only displays all the *.pdf files in the confirm_resume folder and not the downloaded files.
# TODO : Need to change this function to display the downloaded files

def display_list(files):
    clear_data()
    [listBoxView.insert('end',file) for file in files]
    return None


def double_click_handler(event=None):
    """
    Since listBoxView is used to display all the lists, it is necessary to handle all file cases that it can contain.
    """
    curItem = listBoxView.get( listBoxView.curselection())
    root,ext = os.path.splitext(curItem)

    if ext == '.json' : 

        """
        listBoxView.curselection() will return the index of the selected item in the listBox
        The variable filePath was created, just in case that if in the future, the 
        list-item is not the same as the file-path. 
        """
        with open(curItem, 'r') as j:
                contents = j.readlines()

        textLabel.insert('1.0',contents)

    elif ext=='.pdf' : 
        os.startfile(curItem)

    else : 
        clear_text_widget()
        textLabel.insert('end',"Filetype can't be handled")

    return None

def change_desig(event=None) :
    global n
    keys = desigDict.keys()
    n = keys

    

# *NEW WINDOW FUNCTION
def new_window() : 
    def add_skills_to_listbox(event=None) : 
        global skills
        value = combo.get()
        if value : 
            sublist = get_sublist()

            if sublist : 
                listBox.insert(tk.END,value)

    def get_sublist() : 

        '''    
        The following loop creates a sublist
        This sublist will contain all the mainlist elements that 
        are substring of the entry in entrybox. 
        This ensure only elements in the mainlist are being added to the listBox
        '''
        global skills
        value = combo.get()
        if value :
            sublist = []
            for item in skills :
                if value.lower() in item.lower() :
                    sublist.append(item)
            return sublist
        return skills

    def display_sublist(event=None) :  
        combo.configure(values=get_sublist())

    def delete_skills_from_list(event=None):
        cursel = listBox.curselection()
        if cursel : 
            listBox.delete(cursel)

    def submit_window() :
        global desigDict
        key = entryWidget.get()
        value_list = list(listBox.get(0,tk.END))

        desigDict[key] = value_list
        print(desigDict)
        new_window.destroy()

    new_window = tk.Toplevel(root)
    new_window.geometry('500x500+700+200')
    new_window.title('Add New Designation')
    new_window.resizable(False,False)


    newDesigLabel = tk.Label(new_window,text='Enter new designation : ')
    newDesigLabel.pack(fill=tk.X,ipadx=10,ipady=10)

    entryWidget = tk.Entry(new_window,font='helvetica',justify=tk.CENTER)
    entryWidget.pack(fill=tk.X,ipadx=10,ipady=10)


    comboBoxLabel = tk.Label(new_window, text='Select skills :',font=("Times", "14", "bold"))
    comboBoxLabel.pack(fill=tk.X,ipadx=10,ipady=10)

    tk.Label(new_window,text='- Press enter to add skills-',font=("Times", "14", "bold italic")).pack()

    combo = tkentrycomplete.AutocompleteCombobox(new_window,postcommand=display_sublist)
    combo.set_completion_list(skills)
    combo.pack(fill=tk.X,padx=10,pady=10)

    listBox = tk.Listbox(new_window)
    listBox.pack(fill=tk.X,ipadx=10,ipady=10)

    deleteButton = tk.Button(new_window,text='Delete skill', command=delete_skills_from_list)
    deleteButton.pack(ipadx=5)

    submitButton = tk.Button(new_window, text='Submit', command=submit_window)
    submitButton.pack(side=tk.BOTTOM, padx=10, pady=10, ipadx=10, ipady=10)

    # Bindings for the new window
    combo.bind('<Return>',add_skills_to_listbox)
    entryWidget.focus_set()



# TODO : need to show status on screen 
# !right now no way to know if the process was success or not
def parse_resumes() : 
    parser()



###########################################################################
"""
Right now desigDict is stored as a pickle file. The file will be read
at the start of the program and will be written at the end.

Sample desigDict : 
    desigDict = {  'ux_designer' : ['Html','Css','Website'] ,  
                    'php_developer' : ['Php','Website','Coding','Programming'] }
"""
# ! Need to check if ``job_description.pkl`` exists or not 
with open('job_description.pkl','rb') as fopen : 
    desigDict = pickle.load(fopen)


skills = []
f = open('skills_new.csv','r')
reader = csv.reader(f)

for row in reader : 
    skills.extend(row)
f.close()

###########################################################################


root = tk.Tk()
root.geometry("1000x1000")
root.pack_propagate(False)
root.resizable(0, 0)

#Frame for listBoxView
topFrame = tk.LabelFrame(root, text = 'Parser Data')
topFrame.place(height = 250, width= 1000)


# Frame for open file dialogue
bottomFrame = tk.LabelFrame(root, text = 'Open File')
bottomFrame.place(height = 300, width = 1000, rely=0.65, relx=0)

# Text editor
textLabel = tk.Text(root, height=12)
textLabel.place(height = 200, width = 1000, rely=0.25, relx=0)


#Buttons
# TODO : Disable all other buttons if download is not used once
DownloadButton = tk.Button(bottomFrame, text= "Download", command = download_attachments)
DownloadButton.place(rely = 0.35, relx = 0.0)

ParseButton = tk.Button(bottomFrame, text = "Parse Resumes", command = parse_resumes)
ParseButton.place(rely = 0.35, relx = 0.40)

AddDesigButton = tk.Button(bottomFrame, text='Add New Designation', command= new_window)
AddDesigButton.place(rely=0.75, relx=0.20 )

DeleteDesigButton = tk.Button(bottomFrame, text='Delete Designation', command=delete_designation)
DeleteDesigButton.place(rely=0.75,relx=0.40)




# listBox Widget
listBoxView  = tk.Listbox(topFrame, font=('TkMenuFont, 20'))
listBoxView.place(relheight=1, relwidth=1)


#Scrollbar
listBoxScroll_y = ttk.Scrollbar(topFrame, orient='vertical', command=listBoxView.yview)
listBoxScroll_x= ttk.Scrollbar(topFrame, orient='horizontal', command=listBoxView.xview)
listBoxView.configure(xscrollcommand=listBoxScroll_x.set, yscrollcommand=listBoxScroll_y.set)
listBoxScroll_x.pack(side='bottom', fill='x')
listBoxScroll_y.pack(side='right', fill='y')

listBoxView.bind('<Double-1>', double_click_handler)

# Set label 
ttk.Label( bottomFrame, text = "Select the Designation :", 
                      font = ("Times New Roman", 12)).place(rely=0.55, relx=0 )


# Create Combobox
n = tk.StringVar() 


desig = ttk.Combobox(bottomFrame, width = 27, textvariable = n,
                     postcommand=lambda : desig.configure(values=list(desigDict.keys())),
                     state='readonly')

desig.place(rely=0.55, relx=0.20)
desig.bind("<<ComboboxSelected>>", print_selected_item)  

SearchButton = tk.Button(bottomFrame, text = "Search", command = show_matching_files)
SearchButton.place(rely = 0.55, relx = 0.40)



root.mainloop()


# The job_description.pkl file is updated at the end
# This is to ensure all the newly added items are stored.

with open('job_description.pkl','wb') as fwrite : 
            pickle.dump(desigDict,fwrite)