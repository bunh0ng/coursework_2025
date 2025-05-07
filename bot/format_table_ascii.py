from tabulate import tabulate

def format_table_ascii(columns, rows):
    return tabulate(rows, headers=columns, tablefmt="github")
