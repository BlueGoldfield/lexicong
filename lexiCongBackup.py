from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from RandomWordGenerator import RandomWord
import sqlite3

root = Tk()
root.title("Super Ultra Epic Dictionary")

conn = sqlite3.connect('lexicon.db')
c = conn.cursor()

def getData():
    table.delete(*table.get_children())
    c.execute("SELECT * FROM words")
    all = c.fetchall()
    count = 0
    for row in all:
        table.insert('', count, values=(row[1], row[2], row[3], row[4]))
        count += 1

def newWindow(vars, type):
    nw = Toplevel(root)
    nw.geometry("250x320+{}+{}".format(int((root.winfo_screenwidth()/2)-250), int((root.winfo_screenheight()/2)-320)))
    nw.focus()

    def closeThis():
        nw.destroy()

    if type == 4:
        def genWord(len, qty, vl):
            if vl == 0:
                cws = True
            else:
                cws = False
            for i in range(qty):
                wrdslist.insert(i, RandomWord(max_word_size=len, constant_word_size=cws).generate().title())
             
        nw.title("Generator")
        nw.geometry("400x300+{}+{}".format(int((root.winfo_screenwidth()/2)-400), int((root.winfo_screenheight()/2)-300)))
        frame1 = Frame(nw, padx=10, pady=5)
        frame1.grid(column=0, row=0, sticky=NSEW, in_=nw)
        frame2 = Frame(nw, padx=15, pady=5)
        frame2.grid(column=1, row=0, sticky=NSEW, in_=nw)
        frame3 = Frame(nw, padx=10, pady=10)
        frame3.grid(column=0, row=1, columnspan=2, sticky=NSEW, in_=nw)

        nw.grid_columnconfigure(0, weight=1)
        nw.grid_rowconfigure(0, weight=1)

        wllbl = Label(frame1, text="Word max length:")
        wllbl.grid(column=0, row=0, in_=frame1)
        wl = Entry(frame1, width=14)
        wl.grid(column=1, row=0, in_=frame1)
        nowlbl = Label(frame1, text="Number of words \nto generate:")
        nowlbl.grid(column=0, row=1, in_=frame1)
        now = Entry(frame1, width=14)
        now.grid(column=1, row=1, in_=frame1)

        gen = Button(frame2, text="Generate", padx=10, command=lambda:genWord(int(wl.get()), int(now.get()), vwl.get()))
        gen.grid(column=0, row=1, in_=frame2)
        vwl = IntVar()
        varlen = Checkbutton(frame2, text="Variable word length?", onvalue=1, offvalue=0, variable=vwl)
        varlen.grid(column=0, row=0, in_=frame2)

        wrds = Label(frame3, text="Words generated:")
        wrds.grid(column=0, row=0, sticky=W, in_=frame3)
        scroll = Scrollbar(frame3)
        scroll.grid(column=1, row=1, sticky=NS, in_=frame3)
        wrdslist = Listbox(frame3, yscrollcommand=scroll.set)
        wrdslist.delete(0, END)
        wrdslist.grid(column=0, row=1, sticky=NSEW, in_=frame3)
        scroll.config(command = wrdslist.yview)

        frame1.grid_columnconfigure(0, weight=1)
        frame1.grid_rowconfigure(0, weight=1)
        frame2.grid_columnconfigure(0, weight=1)
        frame2.grid_rowconfigure(0, weight=1)
        frame3.grid_columnconfigure(0, weight=1)
        frame3.grid_rowconfigure(0, weight=1)

        def onselect(event):
            w = event.widget
            try:
                val = w.get(w.curselection())
                c.execute("INSERT INTO words VALUES(:id, :word, :pron, :tran, :pos, :def)", {'id': None, 'word': val, 'pron': None, 'tran': None, 'pos': None, 'def': None})
                conn.commit()
                getData()
            except:
                return

        wrdslist.bind('<<ListboxSelect>>', onselect)

        return

    frame1 = Frame(nw, pady=5, padx=5)
    frame1.pack()
    frame2 = Frame(nw, pady=5, padx=5)
    frame2.pack()
    frame3 = Frame(nw, padx=10)
    frame3.pack()

    if vars != '':
        defined = vars[4]

    if type == 1:
        def delete():
            reply = messagebox.askyesno("Confirm", "Are you sure you want to delete {}?".format(word.get()), icon='warning')
            if reply == True:
                c.execute("DELETE FROM words WHERE id = :id", {'id': vars[5]})
                conn.commit()
                getData()
                nw.destroy()
            else: 
                nw.focus()

        nw.title("View")
        vmenu = Menu(nw)
        vmenu.add_command(label = "Edit", command=lambda:[newWindow(vars, 2), closeThis()])
        vmenu.add_command(label = "Delete", command=delete)
        vmenu.add_command(label = "New", command=lambda:[newWindow('', 3), closeThis()])
        nw.config(menu = vmenu)
        word = ttk.Entry(frame1, width=30)
        pos = Entry(frame1, width=10)
        word.insert(0, vars[0])
        pos.insert(0, vars[3])
        word.configure(state=DISABLED)
        pos.configure(state=DISABLED)
        lbl_word = Label(frame1, pady=3, text="Word")
        lbl_pos = Label(frame1, pady=3, text="PoS")
        lbl_word.grid(column=0, row=0, in_=frame1, sticky=W)
        lbl_pos.grid(column=1, row=0, in_=frame1, sticky=W)
        word.grid(column=0, row=1, in_=frame1, padx=2)
        pos.grid(column=1, row=1, in_=frame1, padx=2)
        pron = Entry(frame2, width=25)
        tran = Entry(frame2, width=15)
        pron.insert(0, vars[1])
        tran.insert(0, vars[2])
        pron.configure(state=DISABLED)
        tran.configure(state=DISABLED)
        lbl_pron = Label(frame2, pady=3, text="Pronunciation")
        lbl_tran = Label(frame2, pady=3, text="Translation")
        lbl_pron.grid(column=0, row=0, in_=frame2, sticky=W)
        lbl_tran.grid(column=1, row=0, in_=frame2, sticky=W)
        pron.grid(column=0, row=1, in_=frame2, padx=2)
        tran.grid(column=1, row=1, in_=frame2, padx=2)
        frame1.grid_columnconfigure(0, weight=1)
        frame1.grid_rowconfigure(0, weight=1)
        frame2.grid_columnconfigure(0, weight=1)
        frame2.grid_rowconfigure(0, weight=1)
        lbl_defi = Label(frame3, pady=3, text="Definition")
        lbl_defi.grid(column=0, row=0, in_=frame3, sticky=W)
        defi = Text(frame3, undo=True, width=25, height=10)
        defi.insert(1.0, defined)
        defi.configure(state=DISABLED)
        defi.grid(column=0, row=1, in_=frame3, sticky=NSEW)
        frame3.grid_columnconfigure(0, weight=1)
        frame3.grid_rowconfigure(0, weight=1)

    if type == 2:
        nw.title("Edit")
        def acceptChanges():
            c.execute("UPDATE words SET word = :word, pron = :pron, tran = :tran, pos = :pos, def = :def WHERE id = :id", {'word': word.get(), 'pron': pron.get(), 'tran': tran.get(), 'pos': pos.get(), 'def': defi.get("1.0", "end - 1 chars"), 'id': vars[5]})
            getData()
            editval = (word.get(), pron.get(), tran.get(), pos.get(), defi.get("1.0", "end - 1 chars"), vars[5])
            newWindow(editval, 1)
            nw.destroy()
        emenu = Menu(nw)
        emenu.add_command(label = "Confirm", command=acceptChanges)
        emenu.add_command(label = "Cancel", command=lambda:[newWindow(vars, 1), closeThis()])
        nw.config(menu = emenu)
        word = ttk.Entry(frame1, width=30)
        pos = Entry(frame1, width=10)
        word.insert(0, vars[0])
        pos.insert(0, vars[3])
        lbl_word = Label(frame1, pady=3, text="Word")
        lbl_pos = Label(frame1, pady=3, text="PoS")
        lbl_word.grid(column=0, row=0, in_=frame1, sticky=W)
        lbl_pos.grid(column=1, row=0, in_=frame1, sticky=W)
        word.grid(column=0, row=1, in_=frame1, padx=2)
        pos.grid(column=1, row=1, in_=frame1, padx=2)
        pron = Entry(frame2, width=25)
        tran = Entry(frame2, width=15)
        pron.insert(0, vars[1])
        tran.insert(0, vars[2])
        lbl_pron = Label(frame2, pady=3, text="Pronunciation")
        lbl_tran = Label(frame2, pady=3, text="Translation")
        lbl_pron.grid(column=0, row=0, in_=frame2, sticky=W)
        lbl_tran.grid(column=1, row=0, in_=frame2, sticky=W)
        pron.grid(column=0, row=1, in_=frame2, padx=2)
        tran.grid(column=1, row=1, in_=frame2, padx=2)
        frame1.grid_columnconfigure(0, weight=1)
        frame1.grid_rowconfigure(0, weight=1)
        frame2.grid_columnconfigure(0, weight=1)
        frame2.grid_rowconfigure(0, weight=1)
        lbl_defi = Label(frame3, pady=3, text="Definition")
        lbl_defi.grid(column=0, row=0, in_=frame3, sticky=W)
        defi = Text(frame3, undo=True, width=25, height=10)
        defi.insert(1.0, defined)
        defi.grid(column=0, row=1, in_=frame3, sticky=NSEW)
        frame3.grid_columnconfigure(0, weight=1)
        frame3.grid_rowconfigure(0, weight=1)
    
    if type == 3:
        nw.title("Add")
        def acceptChanges():
            c.execute("INSERT INTO words VALUES (:id, :word, :pron, :tran, :pos, :def)", {'id': None, 'word': word.get(), 'pron': pron.get(), 'tran': tran.get(), 'pos': pos.get(), 'def': defi.get("1.0", "end - 1 chars")})
            conn.commit()
            getData()
            c.execute("SELECT id FROM words WHERE word = ?", (word.get(),))
            newval = (word.get(), pron.get(), tran.get(), pos.get(), defi.get("1.0", "end - 1 chars"), c.fetchone()[0],)
            newWindow(newval, 1)
            nw.destroy()
        amenu = Menu(nw)
        amenu.add_command(label = "Confirm", command=acceptChanges)
        amenu.add_command(label = "Cancel", command=nw.destroy)
        nw.config(menu = amenu)
        word = ttk.Entry(frame1, width=30)
        pos = Entry(frame1, width=10)
        lbl_word = Label(frame1, pady=3, text="Word")
        lbl_pos = Label(frame1, pady=3, text="PoS")
        lbl_word.grid(column=0, row=0, in_=frame1, sticky=W)
        lbl_pos.grid(column=1, row=0, in_=frame1, sticky=W)
        word.grid(column=0, row=1, in_=frame1, padx=2)
        pos.grid(column=1, row=1, in_=frame1, padx=2)
        pron = Entry(frame2, width=25)
        tran = Entry(frame2, width=15)
        lbl_pron = Label(frame2, pady=3, text="Pronunciation")
        lbl_tran = Label(frame2, pady=3, text="Translation")
        lbl_pron.grid(column=0, row=0, in_=frame2, sticky=W)
        lbl_tran.grid(column=1, row=0, in_=frame2, sticky=W)
        pron.grid(column=0, row=1, in_=frame2, padx=2)
        tran.grid(column=1, row=1, in_=frame2, padx=2)
        frame1.grid_columnconfigure(0, weight=1)
        frame1.grid_rowconfigure(0, weight=1)
        frame2.grid_columnconfigure(0, weight=1)
        frame2.grid_rowconfigure(0, weight=1)
        lbl_defi = Label(frame3, pady=3, text="Definition")
        lbl_defi.grid(column=0, row=0, in_=frame3, sticky=W)
        defi = Text(frame3, undo=True, width=25, height=10)
        defi.grid(column=0, row=1, in_=frame3, sticky=NSEW)
        frame3.grid_columnconfigure(0, weight=1)
        frame3.grid_rowconfigure(0, weight=1)


mainmenu = Menu(root)
pmenu = Menu(mainmenu, tearoff=0)
pmenu.add_command(label="Add", command=lambda:newWindow("", 3))
pmenu.add_command(label="Generator", command=lambda:newWindow("", 4))
mainmenu.add_cascade(label="Menu", menu=pmenu)
root.config(menu = mainmenu)

topframe = Frame(root)
topframe.pack(pady=9)
label = Label(topframe, text="Dictionary")
label.pack()

container = Frame(root)
container.pack(padx=10, fill=BOTH, expand=True)
table = ttk.Treeview(container, columns=(1, 2, 3, 4), show = 'headings')
hsb = ttk.Scrollbar(orient="horizontal", command=table.xview)
vsb = ttk.Scrollbar(orient="vertical", command=table.yview)
table.configure(yscrollcommand=vsb.set,xscrollcommand=hsb.set)
table.grid(column=0, row=0, sticky='nsew', in_=container)
vsb.grid(column=1, row=0, sticky='ns', in_=container)
hsb.grid(column=0, row=1, sticky='ew', in_=container)

container.grid_columnconfigure(0, weight=1)
container.grid_rowconfigure(0, weight=1)

table.heading(1, text='word', command=lambda c=1: sortby(table, c, 0))
table.column(1, minwidth=0, width=100)
table.heading(2, text='pronunciation', command=lambda c=2: sortby(table, c, 0))
table.column(2, minwidth=0, width=100)
table.heading(3, text='translation', command=lambda c=3: sortby(table, c, 0))
table.column(3, minwidth=0, width=100)
table.heading(4, text='part of speech', command=lambda c=4: sortby(table, c, 0))
table.column(4, minwidth=0, width=100)
getData()

def onSelect(e):
    selected = table.focus()
    values = table.item(selected, 'values')
    c.execute("SELECT def FROM words WHERE word = ?", (values[0],))
    values = values + c.fetchone()
    c.execute("SELECT id FROM words WHERE word = ?", (values[0],))
    values = values + c.fetchone()
    newWindow(values, 1)

def sortby(tree, col, descending):
    """sort tree contents when a column header is clicked on"""
    # grab values to sort
    data = [(tree.set(child, col), child) \
        for child in tree.get_children('')]
    # if the data to be sorted is numeric change to float
    #data =  change_numeric(data)
    # now sort the data in place
    data.sort(reverse=descending)
    for ix, item in enumerate(data):
        tree.move(item[1], '', ix)
    # switch the heading so it will sort in the opposite direction
    tree.heading(col, command=lambda col=col: sortby(tree, col, \
        int(not descending)))

table.bind('<Double-1>', onSelect)

root.mainloop()