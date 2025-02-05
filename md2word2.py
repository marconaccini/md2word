#!/usr/bin/python3
import pathlib
import tkinter as tk
import pygubu
from tkinter import filedialog
import json
import os
import subprocess
from pathlib import Path

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "ui2.ui"


class md2word:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow: tk.Toplevel = builder.get_object("Toplevel1", master)

        self.md_file_name: tk.StringVar = None
        self.template_file: tk.StringVar = None
        self.output_word_file: tk.StringVar = None
        #self.overwrite_option: tk.StringVar = None

        builder.import_variables(self)

        builder.connect_callbacks(self)

        self.md_file_selector = builder.get_object("md_file_selector")
        self.execute_button = builder.get_object("execute_button")
        self.debug = builder.get_object("debug")


        self.settings_file = "m2w_settings.json"
        self.settings = self.load_settings()

        self.md_file_name.set(self.settings['md_file_name'])
        self.template_file.set(self.settings['template_file'])
        self.output_word_file.set(self.settings['output_word_file'])
        self.pandoc_file = self.settings['pandoc_file']
        md_file_name_history = self.settings.get('md_file_name_history', [])
        self.md_file_selector['values'] = md_file_name_history

        self.debug.delete('1.0', 'end')

        self.mainwindow.geometry(self.settings.get('geometry', '600x420'))

        if self.pandoc_file:
            self.execute_button.config(state='normal')
        else:
            self.execute_button.config(state='disable')
            self.debug.insert('pandoc.exe not defined. Install and select .exe file\n')



    def load_settings(self):
        if os.path.exists(self.settings_file):
            with open(self.settings_file, 'r') as f:
                self.debug.insert('insert','previous settings loaded\n')
                return json.load(f)
        return {"md_file_name": "", "md_file_name_history": "", "template_file": "", "output_word_file": "", "pandoc_file": "", "geometry":""}

    def save_settings(self):
        with open(self.settings_file, 'w') as f:
            json.dump(self.settings, f, indent=4)
            self.debug.insert('insert','settings saved\n')

    def run(self):
        self.mainwindow.protocol("WM_DELETE_WINDOW", self.quit)
        self.mainwindow.mainloop()

    def ms_file_select(self, event=None):
        file = filedialog.askopenfilename(filetypes=[("Markdown Files", "*.md")])
        if file:
            self.base_dir_path = Path(file).parent
            self.md_file_name.set(file)
            to_add_to_list = self.md_file_name.get()
            ms_list = list(self.md_file_selector['values'])
            if to_add_to_list in ms_list:
                new_list = [repr(to_add_to_list)]
                for i, el in enumerate(ms_list):
                    if not el == to_add_to_list and i < 10:
                        new_list.append(el)
                self.md_file_selector['values'] = tuple(new_list)
            else:
                ms_list.append(repr(to_add_to_list))
                self.md_file_selector['values'] = tuple(ms_list)

            while len(self.md_file_selector['values']) > 9:
                self.md_file_selector['values'].pop()

            self.debug.insert('insert',"md file selected\n")


    def ms_cbox_selected(self, event=None):
        self.md_file_name.set(self.md_file_selector.get())

    def select_template_file(self, event=None):
        file = filedialog.askopenfilename(filetypes=[("Ms Word Template file", "*.dotx")])
        if file:
            self.debug.insert('insert',"ms word template selected\n")
            self.template_file.set(file)


    def select_pandoc(self, event=None):
        pandoc_file = filedialog.askopenfilename(filetypes=[("pandoc exe", "*.exe")])
        if pandoc_file:
            self.pandoc_file = pandoc_file
            self.execute_button.config(state='normal')
            self.debug.insert('insert',"pandoc exe selected\n")
        else:
            self.execute_button.config(state='disable')
            self.debug.insert('insert',"pandoc exe missing\n")

    def execute(self, event=None):
        md_file = self.md_file_name.get()
        template_file = self.template_file.get()
        output_word_file_name = self.output_word_file.get()
        self.execute_button.config(state='disable')

        self.debug.insert('insert',"execution started\n")
        #if self.overwrite_option.get():
        #    pass

        if self.pandoc_file and md_file and template_file and os.path.exists(self.pandoc_file ) and os.path.exists(md_file) and os.path.exists(template_file):
            base_path = Path(md_file).parent
            output_word_file = os.path.join(base_path, output_word_file_name)
            command = [
                self.pandoc_file,
                md_file,
                "--output", output_word_file,
                "--reference-doc", template_file
            ]

            try:
                debug_out = subprocess.run(command, check = True, capture_output = True, text = True)
                # self.debug.insert('insert','insert', debug_out)
            except subprocess.CalledProcessError as e:
                self.debug.insert('insert', f"Conversion failed: {e}")

        self.execute_button.config(state='normal')
        self.debug.insert('insert',"execution done\n")


    def open_folder(self, event=None):
        if os.path.exists(self.output_word_file):
            subprocess.run(["explorer", "/select,", self.output_word_file])  # Apre il file explorer con il file evidenziato
        else:
            self.debug.insert('insert',"Il file non esiste!\n")

    def quit(self, event=None):
        self.debug.insert('insert',"exiting\n")
        self.settings['md_file_name'] = self.md_file_name.get()
        self.settings['md_file_name_history'] = self.md_file_selector['values']
        self.settings['template_file'] = self.template_file.get()
        self.settings['pandoc_file'] = self.pandoc_file
        self.settings['output_word_file'] = self.output_word_file.get()
        self.settings['geometry'] = self.mainwindow.geometry()

        self.save_settings()

        self.mainwindow.destroy()

if __name__ == "__main__":
    app = md2word()
    app.run()
