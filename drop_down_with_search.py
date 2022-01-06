import tkinter as tk
import tkentrycomplete

root = tk.Tk()
box_value = tk.StringVar()

def fun():
    print(box_value.get())
combo = tkentrycomplete.AutocompleteCombobox(textvariable=box_value)
test_list = ['apple', 'banana', 'cherry', 'grapes']
combo.set_completion_list(test_list)
combo.place(x=140, y=50)
button = tk.Button(text='but', command=fun)
button.place(x=140,y=70)

root.mainloop()