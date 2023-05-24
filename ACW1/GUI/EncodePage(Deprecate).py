import tkinter as tk
import tkinterDnD as dnd

uiWidth = 750
uiHeight = 750
uiPositionX = 10
uiPositionY = 10

root = tk.Tk()
root.geometry(f"{uiWidth}x{uiHeight}+{uiPositionX}+{uiPositionY}")
root.resizable(False, False)

frm = tk.Frame(root, bg="red")
frm.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

colfrm1 = tk.Frame(frm, width=uiWidth * 0.2, bg="grey")
colfrm1.pack(fill=tk.Y, side=tk.LEFT, anchor=tk.W)

colfrm2 = tk.Frame(frm, width=uiWidth * 0.3, bg="green")
colfrm2.pack(fill=tk.Y, side=tk.LEFT, anchor=tk.W)

colfrm3 = tk.Frame(frm, width=uiWidth * 0.45, bg="yellow")
colfrm3.pack(fill=tk.Y, side=tk.LEFT, anchor=tk.W)

draggable1 = tk.Frame(colfrm1, width=100, height=100)
draggable1.place(x=50, y=50)
dnd.make_draggable(draggable1)

frm2 = tk.Frame(root, bg="blue")
frm2.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

root.mainloop()