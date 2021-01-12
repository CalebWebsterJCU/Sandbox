from tkinter import *
from tkinter import ttk

root = Tk()
# root.geometry('1000x1000')

outer_frame = LabelFrame(root, text='Outer', bg='black')
outer_frame.grid(row=0, column=0, padx=10, pady=10)

inner_frame = LabelFrame(outer_frame, text='Inner', bg='black')
inner_frame.pack(fill=BOTH, expand=True)

canvas = Canvas(inner_frame, width=500, height=500, bg='black')
canvas.pack(side='left', fill=BOTH, expand=True)

scrollbar = ttk.Scrollbar(inner_frame, orient='vertical', command=canvas.yview)
scrollbar.pack(side='right', fill='y')

scrollable_frame = ttk.Frame(canvas)
scrollable_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))


def on_mouse_wheel(event):
    canvas.yview_scroll(-1 * (event.delta // 30), 'units')


canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
canvas.configure(yscrollcommand=scrollbar.set)

root.bind_all('<MouseWheel>', on_mouse_wheel)

for x in range(100):
    Button(scrollable_frame, text=f'Button {x} Yo!', bd=6, bg='black', width=20, height=10).pack()

mainloop()
