import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as font
import tkinter.messagebox as messagebox

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import idle.highlight as highlight


preview_code = """/* This is a preview code */

function main() {
    println('Welcome to use ToyLang!');
    var q = readline('');
    if q == 'hello' {
        println('Hello, World');
    } else {
        println('This is ToyLang');
    }
    var number = int(readline(''));
    if number == 0 {
        println(114514 + number);
    } else {
        println(0.0);
    }
    return ['Finished', 'Finished'];
}

main();
"""


def save_preference(self, config):
    config['view']['font']['name'] = self.font_choice.get()
    config['view']['font']['size'] = int(self.size_bar['text'])
    with open(f"{__import__('os').getcwd()}/idle/config.json", "w", encoding="utf-8") as f:
        __import__('json').dump(config, f, ensure_ascii=False, indent=4)
    messagebox.showinfo("Info", "You need to restart IDLE to apply this change.")
    self.destroy()


class Configure(tk.Tk):
    def __init__(self, x, y, config, syntaxes=None, function=None):
        super().__init__()
        self.config = config
        self.syntaxes = syntaxes
        self.function = function

        self.title("Preference - ToyLang with IDLE : Official Version")
        self.geometry(f"500x600+{x + 40}+{y + 15}")

        self.notebook = ttk.Notebook(self)

        self.font_frame = tk.Frame(self)
        self.notebook.add(self.font_frame, text="Fonts")

        self.preview_bar = tk.Text(self.font_frame, width=500, height=400)
        self.preview_bar.insert(1.0, preview_code)
        self.preview_bar.place(x=0, y=200)
        self.preview_bar.tag_config('keyword', foreground=config['highlight']['keyword'])
        self.preview_bar.tag_config('builtin', foreground=config['highlight']['builtin'])
        self.preview_bar.tag_config('number', foreground=config['highlight']['number'])
        self.preview_bar.tag_config('string', foreground=config['highlight']['string'])
        self.preview_bar.tag_config('comment', foreground=config['highlight']['comment'])

        tk.Label(self.font_frame, text="Choose Font: ", font=("", 9)).place(x=10, y=12)
        self.font_choice = ttk.Combobox(self.font_frame, values=font.families(), state="readonly", width=50)
        self.font_choice.set(config['view']['font']['name'])

        self.size_bar = tk.Label(self.font_frame, text=config['view']['font']['size'])
        self.size_bar.place(x=430, y=35)
        tk.Label(self.font_frame, text="Font Size: ", font=("", 9)).place(x=10, y=37)
        self.font_size = ttk.Scale(self.font_frame, from_=5, to=72, orient=tk.HORIZONTAL, length=300,
                                   command=self.font_size_show)
        self.font_size.set(config['view']['font']['size'])

        self.preview_bar.bind(
            "<KeyRelease>",
            lambda event: highlight.highlight(self.preview_bar, self.syntaxes, self.function, self.config)
        )
        self.font_choice.bind(
            "<<ComboboxSelected>>",
            lambda event: self.font_size_show(self.font_size.get()))
        self.font_size.place(x=100, y=35)
        self.font_choice.place(x=100, y=10)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        ttk.Button(
            self, text="Save Preference",
            command=lambda: save_preference(self, config)).pack(side=tk.BOTTOM, fill=tk.X)

    def font_size_show(self, value):
        value = int(round(float(value), 0))
        self.size_bar['text'] = value
        self.preview_bar.config(font=(self.font_choice.get(), value))
        highlight.highlight(self.preview_bar, self.syntaxes, self.function, self.config)


if __name__ == '__main__':
    with open('../config.json', 'r', encoding="utf-8") as f:
        config = __import__('json').load(f)
    Configure(10, 50, config).mainloop()
