import matplotlib.pyplot as plt
from io import BytesIO

def create_plot(data: list, plot_type: str, title: str, xlabel='', ylabel=''):
    plt.switch_backend('Agg')
    fig, ax = plt.subplots()
    if plot_type == 'bar':
        labels = [row[0] for row in data]
        values = [row[1] for row in data]
        ax.bar(labels, values, color='lightgreen')
    elif plot_type == 'pie':
        labels = [row[0] for row in data]
        sizes = [row[1] for row in data]
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=['#FA8072', '#90EE90', '#FFFFCB'])
    elif plot_type == '2bars':
        labels = [row[0] for row in data]
        values1 = [row[1] for row in data]
        values2 = [row[2] for row in data]
        ax.bar(labels, values1, color='lightgreen')
        ax.bar(labels, values2, bottom=values1, color='salmon')

    plt.title(title)
    plt.xlabel(xlabel,)
    plt.ylabel(ylabel)
    plt.xticks(rotation=90, fontsize=8)
    plt.tight_layout()
    plt.grid(True, axis='y', linestyle='--', color='black')
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return buf


            

