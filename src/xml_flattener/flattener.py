from pathlib import Path
import typer
import pandas as pd
from pandas import DataFrame
from lxml import etree
from pandas.core.groupby import DataFrameGroupBy
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from enum import Enum
from rich.progress import track

console = Console()
app = typer.Typer()
root_dir = Path(__file__).parent
xslt_default = Path(root_dir,'xslt_default.xslt')


class Mode(Enum):
    FILE = 'file'
    FOLDER = 'folder'

def _print_tables(df, title:str = 'Table: '):
    table = Table(title=title)

    for column in df.columns:
        table.add_column(column, justify="right", style="cyan", no_wrap=True)
    for row in df.itertuples(index=False): #type: tuple
        values = tuple(str(v) for v in row)
        table.add_row(*values)
    console.print(table)

def _group_by_and_split(df: DataFrame) -> DataFrameGroupBy:

    columns = {k:v for k, v in enumerate(df.columns.tolist())}

    for i, label in columns.items():
        console.print(f'[{i}] {label}')

    console.print()
    split_by_index = int(console.input('Split by: '))
    with console.status('Grouping records'):
        grouped = df.groupby(by=columns[split_by_index])
    return grouped


@app.command()
def flatten(xml_file: Path, xslt_template: Path = xslt_default, mode: Mode = Mode.FILE, print_output: bool = False, split: bool = False):
    console.print(Panel('[red]XML ACES Flatenner[/red] developed by [purple]Ricardo Galindo[/purple] for [cyan]CCC1[/cyan] (2025)'), style='cyan')
    files = []
    match mode:
        case Mode.FILE:
            if xml_file.is_file() and xml_file.name.endswith('xml'):
                files = [xml_file]
            else:
                raise AttributeError(f'{xml_file} is not a valid xml file.')

        case Mode.FOLDER:
            if xml_file.is_dir():
                files = [file for file in xml_file.iterdir() if file.is_file() and file.name.endswith('xml')]
                console.print(Panel(f'Flattening [red]{len(files)}[/red] xml files in folder'), style='purple')
            else:
                raise AttributeError(f'{xml_file} is not a directory.')

    dataframes = []
    for file in track(files, description='  Flattening files: '):

        output = file.name.rsplit('.',maxsplit=1)[0]
        df = pd.read_xml(file, parser='lxml', stylesheet=xslt_template)
        if print_output:
            _print_tables(df, title=output)
        dataframes.append(df)
    with console.status('Merging records'):
        df_merged = pd.concat(dataframes, ignore_index=True)

    if split:

        grouped = _group_by_and_split(df_merged)

        for name, group_df in track(grouped, description='  Saving files: '):
            folder = (Path(f'{xml_file}_flatenned'))
            folder.mkdir(exist_ok=True, parents=True)
            group_df.to_csv(f'{folder}/{name}.csv', index=False)
    else:

        output = xml_file.name.rsplit('.', maxsplit=1)[0]
        with console.status(f'Saving file {output}'):
            if print_output:
                _print_tables(df_merged, title=output)
            df_merged.to_csv(f'{output}.csv', index=False)

@app.command()
def preview_xml(xml_file: Path,):
    xml = etree.parse(xml_file)
    xml_string = etree.tostring(xml, pretty_print=True, encoding='unicode')
    syntax = Syntax(xml_string, 'xml', theme='ansi_dark', line_numbers=True)
    console.print(Panel(xml_file.name, style='purple'))
    console.print(Panel(syntax))

@app.command()
def xslt_example():
    root_dir = Path(__file__).parent
    xslt = Path(root_dir,'xslt_example.xslt')  # Replace with the actual path to your text file
    try:
        with open(xslt, "r") as file:
            content = file.read()
            syntax = Syntax(content, 'xml', theme='ansi_dark', line_numbers=True)
            console.print(Panel(xslt.name), style='purple')
            console.print(Panel(syntax, style='purple'))

    except FileNotFoundError:
        console.print(f"[bold red]Error:[/bold red] File '{xslt.name}' not found.")
        exit()


def run():
    app()