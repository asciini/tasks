#Tasks - A simple task management application  
Author: Nils Durner, Matrikel: 122770

###How can the program be run and used?
To use the GUI interface, simple run the gui.py using the command:

    `python3 gui.py`

Using this interface, you can save your tasks in an organized way.
Every task is associated to a category, that's why a category has to be created and selected
before creating tasks.
Before creating a task using the "add" button, the name of the category has to be selected on
the left side of your window.

To use the CLI interface, install dependencies as shown below,
then type `tasks --help` to learn more.
You must always start by typing "tasks", then the operation you want to perform.
This could be `add-task`, `add-category`, `display` etc. Again, use `--help` to see more.
If the operation is on a category, specify its name in the next word,
if the operation is on a task, specify its category, then its name.

Example command: 
How to add the task "Milk" to the category "Purchase list"

    `tasks add-task "Purchase list" Milk`



###Are any other dependencies required?
In order to use the app through the command line, the projects package "tasks" must be installed by
executing the following command in the folder "tasks":

    "pip install --editable ."

I'm not sure why the flag --editable is needed but it only works this way.

###Which optional features were carried out?
"Projektzuordnung" and "CLI"

###What else should be noted?
It is not recommended running the GUI and CLI simultaneously.