
import ipywidgets as widgets
import re
import pandas as pd

from collections import OrderedDict
from pathlib import Path
# from IPython import display


def get_dirs(dir_path: str):
    """ Returns a Choice widget to list the dirs under the current one """
    # if dir_path == None:
    #     cwd =
    # else:
    #   cwd = Path(dir_path)

    cwd = Path.cwd() if dir_path == None else Path(dir_path)

    list_dir = [d.name for d in cwd.iterdir() if d.is_dir()]

    choices = widgets.Dropdown(
        options=list_dir,
        description='Dir:',
        value=None,
        disabled=False
    )
    display(choices)

    return choices


def get_files(dir_path: str, extensions: []):
    """ Returns a Choice widget to list the files in the given dir """
    path = Path(dir_path)
    list_files = [f.name for f in path.iterdir() if f.is_file()
                  and f.suffix.rsplit('.', 1)[1] in extensions]
    list_files.sort()

    choices = widgets.Dropdown(
        options=list_files,
        description='Files:',
        value=None,
        disabled=False
    )
    display(choices)

    return choices


def get_data_path():
    """ Returns a Text widget to enter a dir path"""
    text = widgets.Text(
        value='data',
        placeholder='data',
        description='Dir:',
        disabled=False
    )
    display(text)

    return text


def get_year():
    """ Returns a Text widget to enter a year"""
    text = widgets.Text(
        placeholder='2019',
        description='Year:',
        disabled=False
    )
    display(text)

    return text


def get_sheets(workbook: OrderedDict, name: str):
    """ Return a Choice widget of available sheet starting with the {name}"""
    sheet_names = list(workbook.keys())
    regex = f'^{name}'
    sheets = filter(lambda sheet: re.search(regex, sheet), sheet_names)
    sheet_names = list(sheets)

    choices = widgets.Dropdown(
        options=sheet_names,
        description='Sheet:',
        value=None,
        disabled=False
    )
    display(choices)

    return choices


def get_reports(workbook: OrderedDict):
    """ Return the first sheet containing the ToC as dict"""
    # TOC located on the first sheet of the workbook
    toc = workbook[list(workbook)[0]]

    reports = {}
    category = ''
    d = []

    for r in toc:
        title = r

        if re.search('^[Table|Box]', title):
            d.append(title)
        else:
            if d:
                reports[category] = d
            d = []
            category = title

    return reports


def get_category(description: str, options: [], displaying=True):
    style = {'description_width': 'initial'}
    layout = {'width': 'max-content'}

    choices = widgets.Dropdown(
        options=options,
        description=f'{description}:',
        disabled=False,
        style=style,
        layout=layout
    )
    if displaying:
        display(choices)

    return choices


def display_category(category_data):
    output = widgets.Output(value=list(category_data)[0])

    dropdown = widgets.Dropdown(
        options=category_data,
        description='Data: ',
        disabled=False,
        style={'description_width': 'initial'},
        layout={'width': 'max-content'}
    )

    def display_data(tablename):
        output.clear_output()
        sheet = wb[tablename.new.split(':')[0]]

        with output:
            display(sheet)

    def dropdown_eventhandler(change):
        display_data(change)

    dropdown.observe(dropdown_eventhandler, names='value')

    return widgets.VBox([dropdown, output])


def tabbed_categories(categories):
    category_selector = widgets.Tab()

    children = []
    i = 0

    for c in categories:
        children.append(display_category(categories[c]))
        category_selector.set_title(i, c)
        i = i + 1

    category_selector.children = children

    display(category_selector)
