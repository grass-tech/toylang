import tkinter as tk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox

import re
import json
import threading

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import idle.highlight as highlight
import idle.preference as preference
import idle.run as runner

with open(f"{os.getcwd()}/idle/settings.json", "r", encoding="utf-8") as f:
    settings = json.load(f)
run_ui = []


class IdleFunction:
    def __init__(self, idle):
        self.idle = idle

    def create(self):
        if '*' in self.idle.title():
            if messagebox.askyesno(
                    "Do you wanna save this file?",
                    "Click 'Yes' will jump to saving page then create\nClick 'No' will create a new white page"):
                self.save_file()
        self.idle.content_bar.delete(0.0, tk.END)
        self.idle.filename = "undefined"
        self.idle.title(f"{self.idle.filename} | ToyLang with self.idle : Official Version")

    def new_file(self):
        filename = filedialog.asksaveasfilename(defaultextension=".tl", filetypes=[("ToyLang Source File", "*.tl")])
        self.idle.filename = filename if filename else "undefined"
        self.idle.title(f"{filename} | ToyLang with Idle : Official Version")

    def open_file(self):
        filename = filedialog.askopenfilename(defaultextension=".tl", filetypes=[("ToyLang Source File", "*.tl")])
        self.idle.filename = filename if filename else "undefined"
        if self.idle.filename == "undefined":
            messagebox.showerror("Error File", "Cannot Read File")
            return
        self.idle.title(f"{self.idle.filename} | ToyLang with IDLE : Official Version")
        with open(self.idle.filename, "r", encoding="utf-8") as f:
            self.idle.content_bar.delete(0.0, tk.END)
            self.idle.content_bar.insert(tk.END, f.read())
        self.idle.update_line()

    def save_file(self):
        if self.idle.filename == "undefined":
            self.new_file()
        with open(self.idle.filename, "w", encoding="utf-8") as f:
            f.write(self.idle.content_bar.get(0.0, tk.END))
        self.idle.title(f"{self.idle.filename} | ToyLang with IDLE : Official Version")

    def save_as_file(self):
        filename = filedialog.asksaveasfilename(defaultextension=".tl", filetypes=[("ToyLang Source File", "*.tl")])
        if filename:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(self.idle.content_bar.get(0.0, tk.END))
            self.idle.filename = filename
            self.idle.title(f"{filename} | ToyLang with IDLE : Official Version")

    @staticmethod
    def preference(x, y, config, syntaxes, function):
        preference.Configure(x, y, config, syntaxes, function).mainloop()

    @staticmethod
    def auto_indent(event):
        text = event.widget

        line = text.get("insert linestart", "insert")
        match = re.match(r'^(\s+)', line)
        whitespace = match.group(0) if match else ""

        text.insert("insert", f"\n{whitespace}")

        return "break"

    def run(self):
        global run_ui
        for ru in run_ui:
            if ru is not None:
                try:
                    ru.destroy()
                    run_ui.pop(run_ui.index(ru))
                except (AttributeError, RuntimeError):
                    try:
                        run_ui.pop(run_ui.index(ru))
                    except ValueError:
                        pass
        run_ui.clear()
        run_ui.append(runner.RunUI(
            self.idle,
            self.idle.winfo_x(), self.idle.winfo_y(), self.idle.winfo_width()))
        run_ui[-1].mainloop()

    def run_selection(self):
        global run_ui
        for ru in run_ui:
            if ru is not None:
                try:
                    ru.destroy()
                    run_ui.pop(run_ui.index(ru))
                except (AttributeError, RuntimeError):
                    try:
                        run_ui.pop(run_ui.index(ru))
                    except ValueError:
                        pass
        run_ui.clear()
        run_ui.append(runner.RunUI(
            self.idle,
            self.idle.winfo_x(), self.idle.winfo_y(), self.idle.winfo_width()))
        run_ui[-1].mainloop()


def thread_run(func, *args):
    threading.Thread(target=func, args=args).start()


class Idle(tk.Tk):
    def __init__(self, syntaxes, builtin):
        super().__init__()
        self.filename = "undefined"
        self.original_code = []
        self.syntaxes = syntaxes
        self.builtin = builtin
        self.settings = settings

        self.title(f"{self.filename} | ToyLang with IDLE : Official Version")
        self.geometry("500x600+100+50")

        # Edit Menu Bar
        self.menu_bar = tk.Menu(self)
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.edit_menu.add_command(label="New", accelerator="Ctrl+N", command=IdleFunction(self).create)
        self.edit_menu.add_command(label="New File", accelerator="Ctrl+Shift+N", command=IdleFunction(self).new_file)
        self.edit_menu.add_command(label="Open ...", accelerator="Ctrl+O", command=IdleFunction(self).open_file)
        self.edit_menu.add_command(label="Save", accelerator="Ctrl+S", command=IdleFunction(self).save_file)
        self.edit_menu.add_command(
            label="Save As ...", accelerator="Ctrl+Shift+S", command=IdleFunction(self).save_as_file)

        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)

        # View Menu Bar
        self.view_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.view_menu.add_checkbutton(
            label="Preference", accelerator="Ctrl-Shift-P",
            command=lambda: IdleFunction.preference(
                self.winfo_x(), self.winfo_y(), settings, self.syntaxes, self.builtin))

        self.menu_bar.add_cascade(label="View", menu=self.view_menu)

        # Run Menu Bar
        self.run_menu = tk.Menu(self.menu_bar, tearoff=False)
        self.run_menu.add_command(label="Run Whole", accelerator="F5",
                                  command=lambda: thread_run(IdleFunction(self).run))
        self.run_menu.add_command(
            label="Run Selection", accelerator="Alt+F5",
            command=lambda: thread_run(IdleFunction(self).run_selection))

        self.menu_bar.add_cascade(label="Run", menu=self.run_menu)
        self['menu'] = self.menu_bar

        # Main
        self.yscroll_bar = tk.Scrollbar(self, orient=tk.VERTICAL)
        # Line Bar
        self.line_bar = tk.Text(
            self, width=3, bg='#e0e0e0', state=tk.DISABLED, yscrollcommand=self.yscroll_bar.set,
            font=(settings['view']['font']['name'], settings['view']['font']['size'])
        )
        self.line_bar.pack(side=tk.LEFT, fill=tk.Y)
        # Content Bar
        self.xscroll_bar = tk.Scrollbar(self, orient=tk.HORIZONTAL)

        self.content_bar = tk.Text(
            self, wrap=tk.NONE,
            xscrollcommand=self.xscroll_bar.set, yscrollcommand=self.yscroll_bar.set,
            font=(settings['view']['font']['name'], settings['view']['font']['size'])
        )

        self.xscroll_bar.configure(command=self.content_bar.xview)
        self.yscroll_bar.configure(command=lambda *args: (self.content_bar.yview(*args), self.line_bar.yview(*args)))
        self.xscroll_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.yscroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
        self.content_bar.pack(fill=tk.BOTH, expand=True)

        self.content_bar.tag_config('keyword', foreground=settings['highlight']['keyword'])
        self.content_bar.tag_config('builtin', foreground=settings['highlight']['builtin'])
        self.content_bar.tag_config('number', foreground=settings['highlight']['number'])
        self.content_bar.tag_config('string', foreground=settings['highlight']['string'])
        self.content_bar.tag_config('comment', foreground=settings['highlight']['comment'])

        self.bind("<F5>", lambda event: thread_run(IdleFunction(self).run,))
        self.bind("<Alt-F5>", lambda event: thread_run(IdleFunction(self).run_selection))
        self.bind("<Control-n>", lambda event: IdleFunction(self).create())
        self.bind("<Control-N>", lambda event: IdleFunction(self).new_file())
        self.bind("<Control-o>", lambda event: IdleFunction(self).open_file())
        self.bind("<Control-s>", lambda event: IdleFunction(self).save_file())
        self.bind("<Control-S>", lambda event: IdleFunction(self).save_as_file())
        self.bind(
            "<Control-P>",
            lambda event: IdleFunction.preference(self.winfo_x(), self.winfo_y(), settings, syntaxes, builtin))

        self.content_bar.bind("<Return>", IdleFunction(self).auto_indent)
        threading.Thread(target=self.update_highlight).start()
        self.content_bar.bind("<KeyRelease>", self._collect)

        self.mainloop()

    @staticmethod
    def _combine_function(*funcs):
        def combine(*args):
            for f in funcs:
                f(*args)

        return combine

    def _indent(self):
        cursor_position = self.content_bar.index(tk.INSERT)
        line, column = cursor_position.split('.')
        current_line = self.content_bar.get(f"{line}.{column}", f"{line}.end")
        self.content_bar.delete(f"{line}.{int(column) - 1}", f"{line}.{tk.END}")
        self.content_bar.insert(f"{line}.{column}", ' ' * settings['indent'] + current_line)

    def _collect(self, event):
        if event.keycode == 9:
            self._indent()
        self.update_line()

    def update_highlight(self):
        highlight.highlight(self.content_bar, self.syntaxes, self.builtin, settings)
        self.after(500, self.update_highlight)

    def update_line(self):
        text = self.content_bar.get(0.0, tk.END)
        text = text.split("\n")

        if text != self.original_code:
            self.title(f"*{self.filename} | ToyLang with IDLE : Official Version")
        self.original_code = text
        self.line_bar.configure(state=tk.NORMAL)
        self.line_bar.delete(0.0, tk.END)
        for i in range(1, len(text)):
            self.line_bar.insert(tk.END, f"{i}\n")
        self.line_bar.configure(state=tk.DISABLED)
