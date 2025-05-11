from tabulate import tabulate

def format_table_ascii(columns, rows):
    return tabulate(rows, headers=columns, tablefmt="github")

def format_table_for_md(columns, rows):
    return tabulate(rows, headers=columns, tablefmt="github", floatfmt=".0f")