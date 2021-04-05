# -*- coding: utf-8 -*-

import tkinter as tk
import pathlib
import pickle

root = tk.Tk()

# configure root
root.title('Tasks')
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=10)
root.rowconfigure(1, weight=1)

icon_path = pathlib.Path(__file__).with_name("icon.ico").absolute()
root.iconbitmap(icon_path)

# Designate height and width of window
window_width = 600
window_height = 500

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

root.geometry('{}x{}+{}+{}'.format(window_width, window_height, x, y))
# root.minsize(window_width, window_height)

active_category = None
active_checklist = None

edit_index = None
input_edit_task = None
edit_task_button = None
edit_task_frame = None


class Task:
    def __init__(self, name, status):
        self.name = name
        self.status = status


# unpickles data that may have been previously pickled
try:
    with open('data.pkl', 'rb') as handle:
        categories = pickle.load(handle)
except FileNotFoundError:
    # all tasks, their respective status, as well as their category will be saved in this dictionary:
    categories = {}


def save():
    """
    calls the method store_checked_tasks on the currently active checklist
    (there only is one after diplay_checklist ran at least once),
    then pickles the categories dictionary.
    """
    if not active_checklist:
        return
    active_checklist.store_checked_tasks()
    with open('data.pkl', 'wb') as handle:
        pickle.dump(categories, handle)

    # clears the status bar
    status_bar.configure(text="")


class Checklist(tk.Frame):
    """
    An instance of checklist is a tk.Frame that wraps tk.CheckButtons and tk.Labels
    vertically in a grid layout.
    """

    def __init__(self, master, tasks, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        self.tasks = tasks
        self.task_statuses = []
        self.columnconfigure(2, weight=2)
        # c_subtask = 0, then add it to the row of checkbutton and task_label

        # creates CheckButton (plus control variable) and Label for every task
        for task in self.tasks:
            task_status = tk.IntVar()
            task_status.set(task.status)
            self.task_statuses.append(task_status)

            task_index = self.tasks.index(task)

            checkbutton = tk.Checkbutton(self, var=task_status, justify="left")
            checkbutton.grid(row=task_index, column=1, sticky=tk.W)
            # checkbutton.bind("<Button>", self.strikethrough_task())

            task_label = tk.Label(self, text=task.name)
            task_label.grid(row=task_index, column=2, sticky=tk.W)
            # for subtasks in task.subtasks:
            #     c_subtask += 1
            #     checkbutton = tk.Checkbutton(self, var=task_status, justify="left")
            #     checkbutton.grid(row=c_subtask + self.tasks.index(task), column=2, sticky=tk.W)
            #     # checkbutton.bind("<Button>", self.strikethrough_task())
            #
            #     task_label = tk.Label(self, text=task.name)
            #     task_label.grid(row=c_subtask + self.tasks.index(task), column=3, sticky=tk.W)

            edit_task_button = tk.Button(self, text='edit', command=lambda task=task: edit_task(task))
            edit_task_button.grid(row=task_index, column=3, sticky=tk.E)

            self.delete_task_button = tk.Button(self, text='delete', command=lambda task=task: delete_task(task))
            self.delete_task_button.grid(row=task_index, column=4, sticky=tk.E)

    """
        strikethrough task
        # automatically strikes through the text of a task when it is marked as complete

        def update(self):
            # creates CheckButton (plus control variable) and Label for every task
            for task in self.tasks:
                task_label = tk.Label(self, text=task.name)
                task_label.grid(row=self.tasks.index(task), column=2, sticky=tk.W)

        def strikethrough_task(self):
            for i in range(len(self.task_statuses)):
                status = self.task_statuses[i].get()
                task = self.tasks[i]
                if status:
                    strikethrough_task = ''
                    for c in task.name:
                        strikethrough_task = strikethrough_task + c +
                    self.tasks[i].name = strikethrough_task
            self.store_checked_tasks()
            self.update()
    """

    # incorporates the task_statuses into the main dictionary
    def store_checked_tasks(self):
        global active_category
        for i in range(len(self.task_statuses)):
            status = self.task_statuses[i].get()
            self.tasks[i].status = status
        categories[active_category] = self.tasks


def add_category(*args):
    """
    Reads the EntryBox, then updates the categories dictionary accordingly
    and adds it to the ListBox, where it is then displayed among the other categories.
    """
    new_category_name = input_new_category.get()

    if not new_category_name == "Enter a new category here.":
        if new_category_name and new_category_name not in categories:
            categories[new_category_name] = []
            category_select.insert(tk.END, new_category_name)

            # makes sure the newly created category is selected and visible
            category_select.selection_clear(0, 'end')
            category_select.select_set('end')
            category_select.see('end')

            input_new_category.delete(0, 'end')
            display_checklist()


def delete_category():
    """
    Removes the selected category in the categories dictionary,

    """
    if category_select.curselection():
        # gets the name of the category from the ListBox
        selected_category = category_select.get(category_select.curselection()[0])
        del categories[selected_category]

        # deletes currently selected category from the ListBox
        category_select.delete(category_select.curselection())

        # the focus gets put on the first category in the ListBox after each deletion
        category_select.select_set(0)

        # the checklist of the category gets destroyed
        active_checklist.destroy()

        # this event must generated so that display_checklist gets called for the newly selected category
        root.event_generate("<<ListBoxSelect>>")

        save()


def display_checklist(*args):
    """
    Destroys previous checklist and display newly selected or created one.
    """
    global active_category
    global active_checklist

    # Previously displayed checklist is destroyed
    if active_category:
        # active_checklist.store_checked_tasks()
        active_checklist.destroy()

    # makes an instance of Checklist using the selected category
    if category_select.curselection():
        active_category = category_select.get(category_select.curselection()[0])
        active_checklist = Checklist(root, categories[active_category], padx=5, pady=5)
        active_checklist.grid(row=1, column=2, sticky=tk.E + tk.W + tk.S + tk.N, padx=5, pady=5)
    save()


def add_task(*args):
    """
    Reads the EntryBox, then updates the categories dictionary accordingly
    and adds it to the checklist, where it is then displayed among the other tasks.

    Does not allow creating task without a category being selected.
    """
    new_task = input_new_task.get()
    if not new_task == "Enter a new task here, then press enter.":

        # update the list of the corresponding category
        if category_select.curselection():
            selected = category_select.get(category_select.curselection()[0])
            if selected and new_task and new_task not in categories[selected]:
                categories[selected].append(Task(new_task, 0))
        else:
            status_bar.configure(text="Create or select a category before creating a task.")

        display_checklist()

        input_new_task.delete(0, 'end')
        save()


def edit_task(task):
    global active_checklist
    global active_category

    global edit_index
    global input_edit_task
    global edit_task_button
    global edit_task_frame

    edit_index = categories[active_category].index(task)

    edit_task_frame = tk.Frame()
    edit_task_frame.grid(row=1, column=2)

    # spawn EntryBox
    input_edit_task = tk.Entry(edit_task_frame)
    input_edit_task.grid(row=1, column=2, sticky=tk.E + tk.W, padx=(0, 5), pady=5)
    input_edit_task.focus_set()

    # spawn confirm button
    edit_task_button = tk.Button(edit_task_frame, text='confirm', command=confirm_edit_task)
    edit_task_button.grid(row=1, column=3)


def confirm_edit_task():
    # get the user entry and update the list of tasks accordingly
    edited_task = input_edit_task.get()
    categories[active_category][edit_index].name = edited_task

    # make the EntryBox and Button disappear
    edit_task_frame.destroy()
    edit_task_button.destroy()
    input_edit_task.destroy()

    display_checklist()


def delete_task(task):
    global active_category

    categories[active_category].remove(task)
    display_checklist()


def delete_completed():
    global active_category
    global active_checklist

    # update the task_statuses
    Checklist.store_checked_tasks(active_checklist)
    # finds out which tasks in the currently selected category are completed, then deletes them
    for i in range(len(categories[active_category]) - 1, -1, -1):
        task = categories[active_category][i]
        if task.status == 1:
            delete_task(task)
            # categories[active_category].remove(task)

    # category_select.event_generate("<<ListBoxSelect>>")
    # display_checklist()


# Grey example text in EntryBoxes
def handle_focus_in(_):
    input_new_task.delete(0, tk.END)
    input_new_task.config(fg='black')


def handle_focus_out(_):
    input_new_task.delete(0, tk.END)
    input_new_task.config(fg='grey')
    input_new_task.insert(0, "Enter a new task here, then press enter.")


def handle_focus_in_new_category_input(_):
    input_new_category.delete(0, tk.END)
    input_new_category.config(fg='black')


def handle_focus_out_new_category_input(_):
    input_new_category.delete(0, tk.END)
    input_new_category.config(fg='grey')
    input_new_category.insert(0, "Enter a new category here.")


def handle_focus_in_edit_task(_):
    input_edit_task.delete(0, tk.END)
    input_edit_task.config(fg='black')


def handle_focus_out_edit_task(_):
    input_edit_task.delete(0, tk.END)
    input_edit_task.config(fg='grey')
    input_edit_task.insert(0, "Enter the edited task here.")


# categories
category_select = tk.Listbox(root)
category_select.grid(row=1, column=1, sticky=tk.E + tk.W + tk.S + tk.N, padx=5, pady=5)

# goes through each element of categories, adds it to the Listbox
for category in categories:
    category_select.insert(tk.END, category)

# input new category
input_new_category = tk.Entry(root, bg='white', fg='grey')
input_new_category.grid(row=98, column=1, sticky=tk.E + tk.W, padx=5, pady=5, ipadx=2, ipady=2)

# new category button
add_category_button = tk.Button(root, text='add category')
add_category_button.grid(row=99, column=1, sticky=tk.E + tk.W, padx=5, pady=(0, 5))

input_new_category.insert(0, "Enter a new category here.")

# delete category button
delete_category_button = tk.Button(root, text='delete category')
delete_category_button.grid(row=100, column=1, sticky=tk.E + tk.W, padx=5, pady=(0, 5))

# input new task
input_new_task = tk.Entry(root, bg='white', fg='grey')
input_new_task.grid(row=98, column=2, sticky=tk.E + tk.W, padx=(0, 5), pady=5, ipadx=2, ipady=2)

input_new_task.insert(0, "Enter a new task here, then press enter.")

# new task button
add_task_button = tk.Button(root, text='add task')
add_task_button.grid(row=99, column=2, sticky=tk.E + tk.W, padx=(0, 5), pady=(0, 5))

# delete completed button
delete_completed_button = tk.Button(root, text='delete completed tasks')
delete_completed_button.grid(row=100, column=2, sticky=tk.E + tk.W, padx=(0, 5), pady=(0, 5))

# status bar
status_bar = tk.Label(root, borderwidth=2)
status_bar.grid(row=101, column=1, columnspan=2, sticky=tk.E + tk.W)

# buttons
add_task_button.configure(command=add_task)
add_category_button.configure(command=add_category)
delete_category_button.configure(command=delete_category)
delete_completed_button.configure(command=delete_completed)

# binds
category_select.bind('<<ListboxSelect>>', display_checklist)

input_new_task.bind('<Return>', add_task)
input_new_task.bind("<FocusIn>", handle_focus_in)
input_new_task.bind("<FocusOut>", handle_focus_out)

input_new_category.bind('<Return>', add_category)
input_new_category.bind("<FocusIn>", handle_focus_in_new_category_input)
input_new_category.bind("<FocusOut>", handle_focus_out_new_category_input)


# saves data on quit
def on_closing():
    if active_checklist:
        save()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)

if __name__ == "__main__":
    root.mainloop()
