from tkinter import*

def create():
    opt = variable.get()
    if opt == "1":
        b = "option 1"   
    elif opt == "2":
        b = "option 2"   
    elif opt == "3":
        b = "option 3"
    elif opt == "4":
        b = "option 4"
        
    result.delete(0.0, END)
    result.insert(END, b)
    
window = Tk()
window.geometry("1500x900")
window.configure(bg="White")
window.title("Steganography")

select_label = Label(window, text="Encoding and Decoding", font=("Algerian", 18, "underline"), bg="white", fg="black")
select_label.grid(column=0, row=0, padx=5)

o = ["Image", "Document", "Audio Visual"]
options = sorted(o)
variable = StringVar()
variable.set("Choose file type")

def on_option_selected(*args):
    create()

variable.trace('w', on_option_selected)

drop = OptionMenu(window, variable, *options)
drop.grid(column=1, row=0, padx=5, pady=10)

scroll = Scrollbar(window)
scroll.grid(column=2, row=4, sticky='ns')

result = Text(window, height=30, width=90, font=('Candara', 12, "bold"), bg='white', fg='blue', yscrollcommand=scroll.set)
result.grid(column=1, row=4, pady=5)

scroll.config(command=result.yview)

window.mainloop()
