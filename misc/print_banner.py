from termcolor import colored, cprint
from pyfiglet import Figlet
from rich import print as rprint
from rich.markdown import Markdown
from rich.table import Table
from rich.console import Console

f = Figlet(font="big")

title = ""
for ln in f.renderText('LoNG').splitlines():
    print(f"ln.strip()= -->{ln.strip()}<--")
    if ln.strip():
        if title:
            print("append to title")
            title = f"{title}\n{ln}"
        else:
            title = ln

# title = f"[bold dark_blue]{f.renderText('LoNG')}[/bold dark_blue]"
title = f"[bold dark_blue]{title}[/bold dark_blue]"
rprint(title)

sub_title = "[dark_blue][bold][italic]Lo[/bold][/italic]ngitudinal [bold][italic]N[/bold][/italic]LP [bold][italic]G[/bold][/italic]UI[/dark_blue]"
sub_title = "[dark_blue][bold]The [italic]Lo[/italic]ngitudinal [italic]N[/italic]LP [italic]G[/italic]UI[/dark_blue]"
# md = Markdown(sub_title)
print()
rprint(sub_title)
print()

table = Table()

table.add_column(title, justify="center")
table.add_row(sub_title)

console = Console()
console.print(table)
