import os
import traceback
from tkinter import *
from tkinter import ttk, filedialog as fd
from tkinter import messagebox
from Parser import *
import Translate
from Codegen import Converter


def choose_input():
    infile.set(fd.askopenfilename())


def choose_output():
    outfile.set(fd.asksaveasfilename(initialfile='out.ref', defaultextension='.ref'))


def convert():
    with open(infile.get(), 'r') as input_file:
        data = input_file.read()

    result = parser.parse(data)
    if not result:
        raise GenericError('Parsing failed!')
    result, preds = Translate.translateToCNF(list(result))

    result = collapse_asserts(result)

    converter = Converter(result, preds)

    converter.codegen()

    with open(outfile.get(), 'w') as output_file:
        for i in converter.decls:
            output_file.write(i)
            output_file.write('\n')
        output_file.write(converter.entry)

    os.startfile(outfile.get())


def show_error(*args):
    err = traceback.format_exception(*args)
    messagebox.showerror('Exception', err)


if __name__ == '__main__':

    root = Tk()
    root.report_callback_exception = show_error
    root.title('SMT to REF')

    mainframe = ttk.Frame(root, padding='3 3 12 12')
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

    infile = StringVar()
    outfile = StringVar()

    infile_entry = ttk.Entry(mainframe, width=100, textvariable=infile)
    infile_entry.grid(column=2, row=1, sticky=(W, E), padx=(10, 10))
    open_ = ttk.Button(mainframe, text='Browse', command=choose_input)
    open_.grid(column=3, row=1, sticky=E)

    outfile_entry = ttk.Entry(mainframe, width=100, textvariable=outfile)
    outfile_entry.grid(column=2, row=2, sticky=(W, E), padx=(10, 10))
    save = ttk.Button(mainframe, text='Browse', command=choose_output)
    save.grid(column=3, row=2, sticky=E)

    ttk.Label(mainframe, text='Input:').grid(column=1, row=1, sticky=E)
    ttk.Label(mainframe, text='Output:').grid(column=1, row=2, sticky=E)

    make = ttk.Button(mainframe, text='Convert', command=convert)
    make.grid(column=4, row=2, sticky=E, padx=(10, 0))

    root.mainloop()
