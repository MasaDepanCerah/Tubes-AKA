import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from performance import run_single, run_graph
from graph import draw_graph
from coinChange import coin_change_iterative


class App:
    def __init__(self, root):
        root.title("Coin Change – Algorithm Complexity")

        # window size
        root.geometry("900x1000")
        root.resizable(False, False)

        # main frame
        main = tk.Frame(root)
        main.pack(fill="both", expand=True, padx=10, pady=10)

        # input
        input_frame = tk.LabelFrame(main, text="Input")
        input_frame.pack(fill="x")

        tk.Label(input_frame, text="Target Amount (n)").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.entry_n = tk.Entry(input_frame, width=20)
        self.entry_n.grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="Coins (k)  ex: 1,5,10").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.entry_k = tk.Entry(input_frame, width=20)
        self.entry_k.grid(row=1, column=1, padx=5)

        # button
        btn_frame = tk.Frame(main)
        btn_frame.pack(fill="x", pady=10)

        left = tk.LabelFrame(btn_frame, text="Standard")
        left.pack(side="left", expand=True, fill="x", padx=5)

        #right = tk.LabelFrame(btn_frame, text="Optimized")
        #right.pack(side="right", expand=True, fill="x", padx=5)

        tk.Button(left, text="Run Iterative",
                  command=lambda: self.run_single_algo("iterative")).pack(fill="x", pady=2)

        tk.Button(left, text="Run Recursive",
                  command=lambda: self.run_single_algo("recursive")).pack(fill="x", pady=2)

        #tk.Button(right, text="Run Iterative (Early Termination)",
        #          command=lambda: self.run_single_algo("iterative_opt")).pack(fill="x", pady=2)

        #tk.Button(right, text="Run Recursive (Constant-Factor Optimization)",
        #          command=lambda: self.run_single_algo("recursive_opt")).pack(fill="x", pady=2)

        # result single run
        result_frame = tk.LabelFrame(main, text="Result")
        result_frame.pack(fill="x", pady=5)

        self.result_label = tk.Label(
            result_frame,
            text="Result will appear here",
            fg="blue",
            anchor="w",
            justify="left"
        )
        self.result_label.pack(fill="x", padx=5, pady=3)

        # opsi checkbox grafik
        check_frame = tk.LabelFrame(main, text="Graph Options")
        check_frame.pack(fill="x", pady=5)

        self.flags = {
            "Iterative": tk.BooleanVar(value=True),
            "Recursive": tk.BooleanVar(value=True),
            #"Iterative (Optimized)": tk.BooleanVar(value=True),
            #"Recursive (Optimized)": tk.BooleanVar(value=True)
        }

        for name in self.flags:
            tk.Checkbutton(check_frame, text=name,
                           variable=self.flags[name]).pack(anchor="w")

        tk.Button(check_frame, text="Run Graph", command=self.run_graph_all).pack(fill="x", pady=5)

        # grafik
        graph_container = tk.LabelFrame(
            main,
            text="Performance Graph",
            height=400,
            width=890
        )
        graph_container.pack(padx=5, pady=5)
        graph_container.pack_propagate(False)

        self.graph_frame = tk.Frame(graph_container)
        self.graph_frame.pack(fill="both", expand=True)

        

        # table
        table_container = tk.LabelFrame(main, text="Execution Time Table")
        table_container.pack(fill="both", padx=5, pady=5)

        #scrollbar = tk.Scrollbar(table_container)
        #scrollbar.pack(side="right", fill="y")

        #self.table = tk.Listbox(
        #    table_container,
        #    font=("Consolas", 10),
        #    yscrollcommand=scrollbar.set
        #)
        #self.table.pack(side="left", fill="both", expand=True)

        table_frame = tk.Frame(table_container)
        table_frame.pack(fill="both", expand=True)

        columns = ("n", "result", "iter_time", "rec_time")

        self.table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        # header
        self.table.heading("n", text="n")
        self.table.heading("result", text="Result (Min Coins)")
        self.table.heading("iter_time", text="Iterative Time (ms)")
        self.table.heading("rec_time", text="Recursive Time (ms)")

        # kolom
        self.table.column("n", width=80, anchor="center")
        self.table.column("result", width=200, anchor="center")
        self.table.column("iter_time", width=200, anchor="center")
        self.table.column("rec_time", width=200, anchor="center")

        self.table.pack(side="left", fill="both", expand=True)

        # baris
        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.table.yview
        )
        self.table.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        #scrollbar.config(command=self.table.yview)

    # logic
    def get_input(self):
        try:
            n = int(self.entry_n.get())
            k = list(map(int, self.entry_k.get().split(",")))
            return k, n
        except:
            messagebox.showerror("Error", "Input tidak valid")
            return None, None

    def run_single_algo(self, mode):
        from performance import run_single

        k, n = self.get_input()
        if k is None:
            return

        result, exec_time = run_single(k, n, mode)
        self.result_label.config(
            text=(
                f"{'Algorithm':25}: {mode}\n"
                f"{'Minimum coins':25}: {result}\n"
                f"{'Execution Time':25}: {exec_time:.4f} ms"
            )
        )

    def update_result_table(self, coins, max_n, flags):
        self.table.delete(*self.table.get_children())

        step = 1
        if step == 0:
            step = 1

        for n in range(step, max_n + 1, step):
            # ke-n
            row = [n]

            # result
            res = coin_change_iterative(coins, n)
            row.append(res if res != -1 else "No solution")

            # waktu iteratif
            if flags.get("Iterative", False):
                _, t = run_single(coins, n, "iterative")
                row.append(f"{t:.4f}")
            else:
                row.append("-")

            # waktu rekursif
            if flags.get("Recursive", False):
                _, t = run_single(coins, n, "recursive")
                row.append(f"{t:.4f}")
            else:
                row.append("-")

            self.table.insert("", "end", values=row)


    def run_graph_all(self):
        k, n = self.get_input()
        if k is None:
            return

        flags = {name: self.flags[name].get() for name in self.flags}
        data = run_graph(k, n, flags)

        draw_graph(self.graph_frame, data)
        self.update_result_table(k, n, flags)


def start():
    root = tk.Tk()
    App(root)
    root.mainloop()


start()
