import toml
from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename
import subprocess

file_path = ''

config = {
    'file_path': '',
    'window_title': 'Python Editor',
    'output_height': 10,
}
toml_string = toml.dumps(config)

with open('config.toml', 'w') as file:
    file.write(toml_string)



compiler = Tk()
compiler.title("Python Editor")
editor = Text()
editor.pack()
code_output = Text(height=10)
code_output.pack()


def set_file_path(path):
    global file_path
    file_path = path


def open_file():
    path = askopenfilename(filetypes=[('Python File', '*.py')])
    with open(path, 'r') as file:
        code = file.read()
        editor.delete('1.0', END)
        editor.insert('1.0', code)
        set_file_path(path)


def save_as():
    if file_path == '':
        path = asksaveasfilename(filetypes=[('Python File', '*.py')])
    else:
        path = file_path
    with open(path, 'w') as file:
        code = editor.get('1.0', END)
        file.write(code)
        set_file_path(path)


def run():
    if file_path == '':
        save_prompt = Toplevel()
        text = Label(save_prompt, text="Save your code!")
        text.pack()
        return
    command = f'python {file_path}'
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    code_output.insert('1.0', output)
    code_output.insert('1.0', error)


# create menu
try:
    menu_bar = Menu(compiler)
    File_menu = Menu(menu_bar, tearoff=0)
    File_menu.add_command(label='Open', command=open_file)
    File_menu.add_command(label='Save', command=save_as)
    File_menu.add_command(label='Save As', command=save_as)
    menu_bar.add_cascade(label='File', menu=File_menu)

    run_bar = Menu(menu_bar, tearoff=0)
    run_bar.add_command(label='Run', command=run)
    menu_bar.add_cascade(label='Run', menu=run_bar)
    compiler.config(menu=menu_bar)

    compiler.mainloop()
except Exception as e:
    print("Error is:", e)




