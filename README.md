# makeHtmlKanbanTxt

Generate a html kanban board from a todo.txt to do list. See [here](https://github.com/todotxt/todo.txt) for a detailled description of the todo.txt format.

## Prerequisites

- Python 3
- Know the todo.txt syntax (see [here](https://github.com/todotxt/todo.txt) for a detailled description of the format)

## Installation

Just download the makeHtmlKanbanTxt.py script.

## Usage

### Run makeHtmlKanbanTxt.py

```
python makeHtmlKanbanTxt.py path/to/a/todo.txt path/to/the/generated/kanban.html
```

### How the tasks are organized in the different columns ?

I used the todo.txt priority prefixes to define in which column each task should appear. I am not sure it fully respect the todo.txt format but it does not seems a total nonsense either.

- **(A)** A task in progress and therefore a task with the highest priority. Goes to the *To Do* column.
- **(B)** The very next step to do when all the tasks in progress are done. It is a *To Do* task tagged as important. 
- **(C)** This task is done but need to be validate before considering it as finished. It goes to the *Validation* column.
- **x** This task is finished and goes to the *Done* column.
- A task with no priority prefix goes to the *To Do* column, waiting to be treated.

## Current support of the todo.txt format

- [x] priority prefixes
- [x] project tags `+project`
- [x] context tags `@context`
- [ ] creation date
- [ ] completion date
- [ ] special key/value tags
