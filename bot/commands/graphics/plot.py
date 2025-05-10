import matplotlib.pyplot as plt
import io

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
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True, axis='y', linestyle='--', color='black')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return buf