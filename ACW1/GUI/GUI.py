from tkinter import Tk, Label, OptionMenu, StringVar, Scrollbar, Text, END


def create():
    opt = variable.get()
    #If the selected option is "1", it assigns the string "option 1" to the variable b
    if opt == "1":
        b = "option 1"   
    elif opt == "2":
        b = "option 2"   
    elif opt == "3":
        b = "option 3"

    #clears the contents of the result Text widget using result.delete(0.0, END). The parameters 0.0 and END represent the start and end positions of the text to be deleted, respectively.
    result.delete("1.0", END)
    #inserts the value of b into the result Text widget using result.insert(END, b). This appends the value of b at the end of the widget's contents.
    result.insert(END, b)
    
window = Tk()
window.geometry("1500x900")
window.configure(bg="White")
window.title("Steganography")

select_label = Label(window, text="Encoding and Decoding", font=("Algerian", 18, "underline"), bg="white", fg="black")
# select_label.grid(column=0, row=0, padx=5)
select_label.place(x=5, y=5)


o = ["Image", "Document", "Audio Visual"]
options = sorted(o)
variable = StringVar()
variable.set("Choose file type")

def on_option_selected(*args):
    create()

variable.trace('w', on_option_selected)

drop = OptionMenu(window, variable, *options)
# drop.grid(column=1, row=0, padx=5, pady=10)
drop.place(x=100, y=30)

scroll = Scrollbar(window)
# scroll.grid(column=2, row=4, sticky='ns')
scroll.place(x=1000, y=150, relheight=0.5)

result = Text(window, height=30, width=90, font=('Candara', 12, "bold"), bg='white', fg='blue', yscrollcommand=scroll.set)
# result.grid(column=1, row=4, pady=5)
result.place(x=200, y=150)

scroll.config(command=result.yview)

window.mainloop()
