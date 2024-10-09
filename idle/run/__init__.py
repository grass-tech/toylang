import threading
import tkinter as tk
import platform
import time

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import Interpreter


class RunUI(tk.Tk):
    def __init__(self, father, x, y, ox, is_selection=False):
        super().__init__()
        __version__ = f"""ToyLang 1.1.5 Interpreter on {platform.system()} at {time.strftime('%H:%M:%S')} running
[MISC for this]\n\n"""
        self.key_pressed = None
        self.timer_id = None
        self.title("Run - ToyLang with IDLE : Official Version")
        if x + ox < self.winfo_screenwidth() and 0 > x - ox:
            fx = x + ox
            oy = 0
        else:
            fx = x - ox
            oy = 0
        self.geometry(f"500x600+{fx}+{y + oy}")

        self.yscroll_bar = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.colm_bar = tk.Text(self, width=3, state=tk.DISABLED, yscrollcommand=self.yscroll_bar.set,
                                font=(father.settings['view']['font']['name'], father.settings['view']['font']['size']))
        self.colm_bar.pack(side=tk.LEFT, fill=tk.Y)

        self.content_bar = tk.Text(self, yscrollcommand=self.yscroll_bar.set,
                                   font=(
                                       father.settings['view']['font']['name'],
                                       father.settings['view']['font']['size']))
        self.content_bar.insert(tk.END, __version__)
        self.content_bar.insert(tk.END, f'= {father.filename}\n\n')

        self.content_bar.tag_config("output", foreground='blue')
        self.content_bar.tag_config("error", foreground='red')

        self.content_bar.pack(padx=5, fill=tk.BOTH, expand=True)

        threading.Thread(target=self.run, args=(is_selection, father)).start()

    def println(self, rs):
        self.content_bar.insert(tk.END, rs, 'output')
        self.content_bar.yview_moveto(True)
        self.content_bar.update()

    def readline(self, info):
        self.content_bar.unbind_all("<Return>")
        self.colm_bar.delete(0.0, tk.END)
        self.colm_bar.configure(state=tk.NORMAL)
        self.colm_bar.insert(tk.END, '\n' * len(self.content_bar.get(0.0, tk.END).split("\n")[:-2]))
        self.colm_bar.insert(tk.END, '>>>')
        self.colm_bar.configure(state=tk.DISABLED)

        self.content_bar.insert(tk.END, info)
        self.content_bar.bind("<Return>", lambda event: self.get_readline())
        while self.key_pressed is None: pass
        return self.key_pressed[len(info):]

    def get_readline(self):
        cursor_position = self.content_bar.index(tk.INSERT)
        line_number = int(cursor_position.split('.')[0])
        start_of_line = f"{line_number}.0"
        end_of_line = f"{line_number}.end"
        current_line_content = self.content_bar.get(start_of_line, end_of_line)
        self.key_pressed = current_line_content

    def run(self, is_selection, father):
        idle = {
            "println": self.println,
            "readline": self.readline
        }
        if is_selection:
            try:
                err, out = runner(father.content_bar.get(tk.SEL_FIRST, tk.SEL_LAST), father.filename, idle)
            except tk.TclError:
                err, out = runner(father.content_bar.get(0.0, tk.END), father.filename, idle)
        else:
            err, out = runner(father.content_bar.get(0.0, tk.END), father.filename, idle)

        if err is None:
            self.content_bar.insert(tk.END, out, "output")
            ec = 0
        else:
            self.content_bar.insert(tk.END, err, "error")
            ec = -1

        self.content_bar.insert(tk.END, f"\n\nRun finished with exit code {ec}")


def runner(text, file, idle):
    res = Interpreter.execute(file, text, None, True, idle)
    if res is not None:
        if isinstance(res, str):
            return [res, None]
        elif isinstance(res, list):
            return [None, '\n'.join(res)]
    else:
        return [None, '']


if __name__ == '__main__':
    RunUI().mainloop()
