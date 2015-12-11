import json
import tkinter as tk


class QAGeneratorUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        '''This initialisation runs the whole program'''
        self.story_buffer = None
        self.question_buffer = None
        self.story_line = 0
        self.story_length = 0

        tk.Tk.__init__(self, *args, **kwargs)
        self.title('QAGenerator')
        self.geometry('820x660')
        self.canvas = tk.Canvas(self)
        self.frame = tk.Frame(self.canvas)
        self.canvas.pack(fill='both', expand='yes')
        self.canvas.create_window((0, 0), window=self.frame, anchor='nw')
        self.frame.bind('<Configure>',
                        lambda x: self.canvas.configure(scrollregion=self.canvas.bbox('all')))  # lambda function

        # Story Board
        self.story_board = tk.Text(self.frame, height=20, width=100)
        self.sb_scroll = tk.Scrollbar(self.frame)
        self.sb_scroll.config(command=self.story_board.yview)
        self.story_board.config(yscrollcommand=self.sb_scroll.set)
        self.story_board.grid(row=0, column=0)  # grid instead
        self.sb_scroll.grid(row=0, column=1, sticky='ns')  # grid instead

        # Question Board
        self.question_board = tk.Text(self.frame, height=20, width=100)
        self.qb_scroll = tk.Scrollbar(self.frame)
        self.qb_scroll.config(command=self.question_board.yview)
        self.question_board.config(yscrollcommand=self.qb_scroll.set)
        self.question_board.grid(row=1, column=0)  # grid instead
        self.qb_scroll.grid(row=1, column=1, sticky='ns')  # grid instead

        self.b_prev = tk.Button(self.frame, text="Previous", command=self.on_click_prev)
        self.b_next = tk.Button(self.frame, text="Next", command=self.on_click_next)
        self.b_prev.grid(row=2, column=0, sticky='w', ipadx=138)
        self.b_next.grid(row=2, column=0, sticky='e', ipadx=138)

    def set_buffers(self, story, questions):
        self.story_buffer = story
        self.question_buffer = questions
        self.story_length = len(story)
        self.story_board.insert(tk.END, self.story_buffer[self.story_line])
        self.question_board.insert(tk.END, self.question_buffer[self.story_line])
        print('buffers set')

    def on_click_prev(self):
        if self.story_line > 0:
            self.story_line -= 1
            self.story_board.delete(1.0, tk.END)
            self.story_board.insert(tk.END, self.story_buffer[self.story_line])
            self.question_board.delete(1.0, tk.END)
            self.question_board.insert(tk.END, self.question_buffer[self.story_line])
        #		print('prev clicked')

    def on_click_next(self):
        if self.story_line < self.story_length - 1:
            self.story_line += 1
            self.story_board.delete(1.0, tk.END)
            self.story_board.insert(tk.END, self.story_buffer[self.story_line])
            self.question_board.delete(1.0, tk.END)
            self.question_board.insert(tk.END, self.question_buffer[self.story_line])
        elif self.story_line == self.story_length - 1:
            self.story_line += 1
            self.story_board.delete(1.0, tk.END)
            self.story_board.insert(tk.END, "\n".join(self.story_buffer))
            self.question_board.delete(1.0, tk.END)
            self.question_board.insert(tk.END, "\n".join(self.question_buffer))


# print('next clicked')

ui = QAGeneratorUI()
with open("story_ui_stmts") as f:
    story = json.load(f)
with open("story_ui_qa") as f:
    questions = json.load(f)
ui.set_buffers(story, questions)
ui.mainloop()
