import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
from datetime import datetime

FILE_NAME = "todo.csv"

# Ensure file exists
def initialize_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Task", "Priority", "Due Date", "Status"])

def load_tasks():
    for item in todo_tree.get_children():
        todo_tree.delete(item)

    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                todo_tree.insert("", "end", values=(row["Task"], row["Priority"], row["Due Date"], row["Status"]))

def add_task():
    task = task_entry.get().strip()
    priority = priority_combo.get()
    due_date = due_date_entry.get().strip()

    if not task:
        messagebox.showerror("Error", "Task cannot be empty.")
        return

    # Optional: validate date format
    if due_date:
        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Date must be in YYYY-MM-DD format.")
            return

    with open(FILE_NAME, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([task, priority, due_date, "Pending"])

    clear_inputs()
    load_tasks()

def delete_task():
    selected_items = todo_tree.selection()
    if not selected_items:
        messagebox.showwarning("Warning", "Select a task to delete.")
        return

    confirm = messagebox.askyesno("Delete", "Are you sure you want to delete the selected task(s)?")
    if not confirm:
        return

    selected_data = [todo_tree.item(item)["values"] for item in selected_items]

    with open(FILE_NAME, mode='r') as file:
        reader = list(csv.reader(file))

    updated_rows = [reader[0]]  # Header
    for row in reader[1:]:
        if row not in selected_data:
            updated_rows.append(row)

    with open(FILE_NAME, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(updated_rows)

    load_tasks()

def mark_completed():
    selected_item = todo_tree.selection()
    if not selected_item:
        messagebox.showinfo("Info", "Select a task to mark as completed.")
        return

    selected_data = todo_tree.item(selected_item[0])["values"]

    with open(FILE_NAME, mode='r') as file:
        rows = list(csv.reader(file))

    header = rows[0]
    updated_rows = [header]
    for row in rows[1:]:
        if row == selected_data:
            updated_rows.append([row[0], row[1], row[2], "Completed"])
        else:
            updated_rows.append(row)

    with open(FILE_NAME, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(updated_rows)

    load_tasks()

def clear_inputs():
    task_entry.delete(0, tk.END)
    priority_combo.set("")
    due_date_entry.delete(0, tk.END)

# GUI setup
root = tk.Tk()
root.title("📝 To-Do List Manager")
root.geometry("700x500")
root.resizable(False, False)

initialize_file()

# Input Frame
input_frame = tk.LabelFrame(root, text="Add New Task", padx=10, pady=10)
input_frame.pack(padx=10, pady=10, fill="x")

tk.Label(input_frame, text="Task:").grid(row=0, column=0, sticky="w")
task_entry = tk.Entry(input_frame, width=40)
task_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Priority:").grid(row=1, column=0, sticky="w")
priority_combo = ttk.Combobox(input_frame, values=["Low", "Medium", "High"], state="readonly", width=37)
priority_combo.grid(row=1, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Due Date (YYYY-MM-DD):").grid(row=2, column=0, sticky="w")
due_date_entry = tk.Entry(input_frame, width=40)
due_date_entry.grid(row=2, column=1, padx=5, pady=5)

add_button = tk.Button(input_frame, text="Add Task", command=add_task, bg="#4CAF50", fg="white", width=20)
add_button.grid(row=3, column=0, columnspan=2, pady=10)

# Treeview Frame
tree_frame = tk.Frame(root)
tree_frame.pack(padx=10, pady=10, fill="both", expand=True)

columns = ("Task", "Priority", "Due Date", "Status")
todo_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=10, selectmode="browse")

for col in columns:
    todo_tree.heading(col, text=col)
    todo_tree.column(col, width=150)

todo_tree.pack(side="left", fill="both", expand=True)

scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=todo_tree.yview)
todo_tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right", fill="y")

# Action Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

delete_button = tk.Button(button_frame, text="🗑️ Delete Task", command=delete_task, bg="#f44336", fg="white", width=20)
delete_button.grid(row=0, column=0, padx=10)

complete_button = tk.Button(button_frame, text="✅ Mark Completed", command=mark_completed, bg="#2196F3", fg="white", width=20)
complete_button.grid(row=0, column=1, padx=10)

# Load tasks initially
load_tasks()
root.mainloop()
