# Create a html kanban board out of a todo.txt file.
# Copyright (C) 2022  KrisNumber24

# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; 
# version 2.1 of the License, or any later version.

# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  
# If not, see https://github.com/KrisNumber24/makeHtmlKanbanTxt/blob/main/LICENSE

import os
import re
import argparse

def fread(filename):
    """Read file and close the file."""
    with open(filename, 'r') as f:
        return f.read()

def fwrite(filename, text):
    """Write content to file and close the file."""
    basedir = os.path.dirname(filename)
    if len(basedir) > 0 and not os.path.isdir(basedir):
        os.makedirs(basedir)

    with open(filename, 'w') as f:
        f.write(text)


def parse_todo_txt(todo_txt):
    """ Read a todo.txt file and fill a dictionary that represents the
        four columns of the kanban """
    todo_list =  re.findall(r'^.+$', todo_txt, re.MULTILINE)# todo_txt.split("\n")

    task_cards = {
        "todo": [],
        "important": [],
        "in_progress": [],
        "validation": [],
        "done": []
    }

    for todo in todo_list:
        if len(todo) > 0:
            todo_data = re.match(
                r'^(?P<isDone>x )? '
                r'?(?P<priority>\([A-Z]\))? '
                r'?(?P<dates>\d\d\d\d-\d\d-\d\d( \d\d\d\d-\d\d-\d\d)?)? '
                r'?(?P<subject>[^@\+]+) ?' 
                r'?(?P<project>\+[^@\s]+)? '
                r'?(?P<context>@\S+)?',
                todo)
            
            todo_dict = todo_data.groupdict()
            
            task_card = '<li class="task">' + "<p>" + todo_dict.get("subject", "no subject") + "<p>"

            if todo_dict.get("project"):
                task_card += '<p class="project"><span>' + todo_dict['project'] + '</span></p>'
            
            if todo_dict.get("context"):
                task_card += '<p class="context"><span>' + todo_dict['context'] + '</span></p>'

            task_card += '</li>\n'

            category = "todo"

            if todo_dict.get("isDone"):
                category = "done"
            
            elif todo_dict.get("priority"):
                priority = todo_dict['priority']

                if priority == "(B)":
                    task_card = task_card.replace('<li class="task">', '<li class="important task">')
                    category = "important"

                elif priority == "(A)":
                    category ='in_progress'
                
                elif priority == "(C)":
                    category = 'validation'

            task_cards[category].append(task_card + "\n")
    
    return task_cards


def render_progess_bar(kanban_model, layout):
    """ Replace the progress bars placeholders in the HTML layout """
    nb_done_tasks = len(kanban_model['done'])
    nb_in_progress_tasks = len(kanban_model['in_progress'])
    nb_validation_tasks = len(kanban_model['validation'])
    nb_todo_tasks = len(kanban_model["todo"]) + len(kanban_model["important"])
    total_tasks = nb_done_tasks + nb_in_progress_tasks + nb_validation_tasks + nb_todo_tasks

    todo_percent = (nb_todo_tasks / total_tasks) * 100
    in_progress_percent = (nb_in_progress_tasks / total_tasks) * 100
    validation_percent = (nb_validation_tasks / total_tasks) * 100
    done_percent = (nb_done_tasks / total_tasks) * 100

    output = layout.replace("{{ todo-bar-size }}", str(todo_percent))\
            .replace("{{ in-progress-bar-size }}", str(in_progress_percent))\
            .replace("{{ validation-bar-size }}", str(validation_percent))\
            .replace("{{ done-bar-size }}", str(done_percent))\
            .replace("{{ todo-progress }}", 'To Do: ' + str(nb_todo_tasks))\
            .replace("{{ in-progress-progress }}", 'In progress: ' + str(nb_in_progress_tasks))\
            .replace("{{ validation-progress }}", 'Validation: ' + str(nb_validation_tasks))\
            .replace("{{ done-progress }}", 'Done: ' + str(nb_done_tasks))

    return output


def render_kanban(kanban_model, layout):
    """ Replace the placeholders in the kanban column of the html layout """
    output = layout.replace("{{ todo }}", "".join(kanban_model["important"] + kanban_model["todo"]))\
            .replace("{{ in_progress }}", "".join(kanban_model["in_progress"]))\
            .replace("{{ validation }}", "".join(kanban_model["validation"]))\
            .replace("{{ done }}", "".join(kanban_model["done"]))
    
    return output


def main(args):
    todo_txt = fread(args.src)

    layout = """
<html>
    <head>
        <style>
            body {
                margin: 10px;
            }

            div#kanban-container {
                width: 100%;
                display: flex;
                flex-direction: row;
            }

            div.column {
                background: #daecf1;
                padding: 5px 15px;
                border-radius: 10px;
                flex: 1;
                margin: 10px;
            }

            div > ul {
                list-style: none;
                padding: 0;
            }

            div.column > ul li.task {
                background: white;
                border-radius: 5px;
                padding: 5px 15px;
                margin-top: 15px;
                margin-bottom: 15px;
                box-shadow: 0 5px 7px rgba(0, 0, 0, 0.1),
                    0 0 5px rgba(0, 0, 0, .2);
                color: #4c6066;
            }

            div#todo {
                border-top: solid 15px #e12360;
            }

            div#in-progress {
                border-top: solid 15px rgb(0, 182, 228);
            }

            div#validation {
                border-top: solid 15px rgb(34, 181, 127);
            }

            div#done {
                border-top: solid 15px rgb(104, 204, 133);
            }

            div#done > ul li.task {
                background: #ffffffb1;
            }

            h2 {
                font-family: roboto, arial;
                font-weight: 300;
                color: white;
                margin-top: 5px;
            }

            div#todo h2 {
                color: #e12360
            }

            div#in-progress h2 {
                color: rgb(0, 182, 228)
            }

            div#validation h2 {
                color: rgb(34, 181, 127)
            }
            
            div#done h2 {
                color: rgb(104, 204, 133)
            }

            p {
                font-family: roboto, arial;
                font-weight: 300;
                color: #2e3a49;
                margin-top: 5px;
                margin-bottom: 10px;
            }

            div#done > ul > li.task > p:not(.project):not(.context) {
                text-decoration: line-through;
            }

            p.project, p.context {
                font-family: roboto, arial;
                font-weight: 300;
                font-size: 10pt;
                text-align: right;
            }

            p.project > span {
                color: rgb(0, 182, 228);
            }

            p.context > span {
                color: #1c9c6d;
            }

            li.important.task {
                border-left: 7px solid #e12360; 
            }

            li.important.task::before {
                content: "*";
                display: block;
                color: #a7083b;
                border: 2px solid #a7083b;
                border-radius: 12px;
                width: 11px;
                height: 11px;
                line-height: 11pt;
                text-align: center;
                font-size: 14pt;
                margin-left: -12px;
                margin-bottom: -5px;
            }

            div#progress-bar-container {
                height: 15px;
                margin: 10px;
            }

            div#progress-bar {
                height: 100%;
                width: 100%;
            }

            div#progress-bar > div > span {
                color: white;
                font-family: roboto, arial;
                font-size: 8pt;
                margin: 2px 5px;
            }

            div#todo-bar {
                width: {{ todo-bar-size }}%;
                height: 100%;
                background: #e12360;
                float: left;
                border-radius: 5px 0 0 5px;
            }

            div#in-progress-bar {
                width: {{ in-progress-bar-size }}%;
                height: 100%;
                background: rgb(0, 182, 228);
                float: left;
            }

            div#validation-bar {
                width: {{ validation-bar-size }}%;
                height: 100%;
                background: rgba(34, 181, 127);
                float: left;
            }

            div#done-bar {
                width: {{ done-bar-size }}%;
                height: 100%;
                background: rgb(104, 204, 133);
                float: left;
                border-radius: 0 5px 5px 0;
            }

            @media (max-width: 990px) {
                div#kanban-container {
                    flex-direction: column;    
                }
            }

        </style>
    </head>

    <body>
        <div id="progress-bar-container">
            <div id="progress-bar">
                <div id="todo-bar">
                    <span>{{ todo-progress }}</span>
                </div>
                <div id="in-progress-bar">
                    <span>{{ in-progress-progress }}</span>
                </div>
                <div id="validation-bar">
                    <span>{{ validation-progress }}</span>
                </div>
                <div id="done-bar">
                    <span>{{ done-progress }}</span>
                </div>
            </div>
        </div>

        <div id="kanban-container">
            <div class="column" id="todo">
                <h2> To Do </h2>
                <ul>
                    {{ todo }}
                </ul>
            </diV>

            <div class="column" id="in-progress">
                <h2> In progress </h2>
                <ul>
                    {{ in_progress }}
                </ul>
            </diV>

            <div class="column" id="validation">
                <h2> Validation </h2>
                <ul>
                    {{ validation }}
                </ul>
            </diV>

            <div class="column" id="done">
                <h2> Done </h2>
                <ul>
                    {{ done }}
                </ul>
            </diV>
        </div>
    
    </body>
</html>
"""
    task_cards = parse_todo_txt(todo_txt)

    output = render_progess_bar(task_cards, layout)
    output = render_kanban(task_cards, output) 

    fwrite(args.dest, output)


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(
        description='Generate an html file containing a kanban containing the' 
            'tasks of the todo.txt file')
    
    arg_parser.add_argument(
        'src', 
        help='Path to a todo.txt file', 
        default='',
        type=str
    )

    arg_parser.add_argument(
        'dest', 
        help='Path to the html file in which to write the kanban data', 
        default='',
        type=str
    )

    args = arg_parser.parse_args()
    main(args)
