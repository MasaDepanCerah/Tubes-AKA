from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def draw_graph(frame, data):
    for widget in frame.winfo_children():
        widget.destroy()

    fig = Figure(figsize=(7, 7))
    ax = fig.add_subplot(111)

    for label in data:
        ax.plot(
            data[label]["n"],
            data[label]["time"],
            label=label
        )

    ax.set_xlabel("n (Target Amount)")
    ax.set_ylabel("Execution Time (seconds)")
    ax.set_title("Coin Change – Complexity Analysis")
    ax.legend()
    ax.grid(True)

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
