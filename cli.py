import click
import pickle
from gui import Task

# unpickles data that may have been previously pickled
try:
    with open('data.pkl', 'rb') as handle:
        categories = pickle.load(handle)
except FileNotFoundError:
    # all tasks, their respective status, as well as their category will be saved in this dictionary:
    categories = {}


def save():
    with open('data.pkl', 'wb') as handle:
        pickle.dump(categories, handle)


@click.group()
def cli():
    pass


@cli.command()
def display():
    '''
    Display an overview of all categories and tasks.
    '''
    for category in categories:
        click.echo(f'{category} \n')
        for task in categories[category]:
            if task.status == 1:
                task_status_as_text = '\u2713'
            else:
                task_status_as_text = ''
            click.echo(f'\t {task.name} {task_status_as_text}')


@cli.command()
@click.argument('name')
def add_category(name):
    '''
    Adds new category to categories.
    '''
    categories[name] = []
    save()


@cli.command()
@click.argument('name')
def delete_category(name):
    '''
    Allows you to delete a category.
    '''
    del categories[name]
    save()


@cli.command()
@click.argument('category')
@click.argument('name')
def add_task(category, name):
    '''
    Adds new task to a certain category.
    '''
    task = Task(name, 0)
    categories[category].append(task)
    save()


@cli.command()
@click.argument('category')
@click.argument('task')
def delete_task(category, task):
    '''
    Allows you to delete a task
    that is contained in a certain category.
    '''
    categories[category].remove(task)
    save()


@cli.command()
@click.argument('category')
def display_tasks(category):
    '''
    Allows you to display a list of all the tasks that
    are contained in a certain category.
    '''
    for task in categories[category]:
        if task.status == 1:
            task_status_as_text = '\u2713'
        else:
            task_status_as_text = ''

        click.echo(f'{task.name} {task_status_as_text} \n')


@cli.command()
def display_categories():
    '''
    Allows you to display a list of all saved categories.
    '''
    for key in categories:
        click.echo(f'{key} \n')


@cli.command()
@click.argument('category')
@click.argument('name')
def check(category, name):
    '''
    Allows you to check a task.
    '''
    task = get_task_by_name(category, name)
    if task:
        task.status = 1
        save()


@cli.command()
@click.argument('category')
@click.argument('name')
def uncheck(category, name):
    '''
    Allows you to uncheck a task.
    '''
    task = get_task_by_name(category, name)
    if task:
        task.status = 0
        save()


def get_task_by_name(category, name):
    if category in categories:
        for task in categories[category]:
            if name == task.name:
                return task
