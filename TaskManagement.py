import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import datetime
import json

class Task:
		def __init__(self, name, description, due_date, priority):
				self.name = name
				self.description = description
				self.due_date = due_date
				self.priority = priority
				self.completed = False

		def to_dict(self):
				return {
						"name": self.name,
						"description": self.description,
						"due_date": self.due_date,
						"priority": self.priority,
						"completed": self.completed
				}

		@staticmethod
		def from_dict(data):
				task = Task(data["name"], data["description"], data["due_date"], data["priority"])
				task.completed = data["completed"]
				return task

class TaskManagerApp:
		def __init__(self, root):
				self.root = root
				root.title("Task Management System")
				self.tasks = []
				self.load_tasks()
    
				self.search_task_button = tk.Button(root, text="Search Task", command=self.search_task)
				self.search_task_button.pack()
				
				self.add_task_button = tk.Button(root, text="Add Task", command=self.add_task)
				self.add_task_button.pack()

				self.modify_task_button = tk.Button(root, text="Modify Task", command=self.modify_task)
				self.modify_task_button.pack()

				self.delete_task_button = tk.Button(root, text="Delete Task", command=self.delete_task)
				self.delete_task_button.pack()

				self.task_display = ttk.Treeview(root, columns=("Name", "Description", "Due Date", "Priority", "Status"), show="headings")
				self.task_display.heading("Name", text="Task Name")
				self.task_display.heading("Description", text="Description")
				self.task_display.heading("Due Date", text="Due Date")
				self.task_display.heading("Priority", text="Priority")
				self.task_display.heading("Status", text="Status")
				self.task_display.pack(expand=True, fill='both')

				self.update_task_display()

		def save_tasks(self):
				with open("tasks.json", "w") as file:
						json.dump([task.to_dict() for task in self.tasks], file)

		def load_tasks(self):
				try:
						with open("tasks.json", "r") as file:
								tasks_data = json.load(file)
								self.tasks = [Task.from_dict(task_data) for task_data in tasks_data]
				except (FileNotFoundError, json.JSONDecodeError):
						self.tasks = []

		def add_task(self):
				name = simpledialog.askstring("Input", "Task Name:", parent=self.root)
				if not name:
						messagebox.showwarning("Warning", "Task name cannot be empty.")
						return

				description = simpledialog.askstring("Input", "Description (or press Cancel for 'N/A'):", parent=self.root)
				description = description if description else "N/A"

				due_date_str = simpledialog.askstring("Input", "Due Date (mm/dd/yyyy):", parent=self.root)
				if due_date_str:
						try:
								due_date = datetime.datetime.strptime(due_date_str, "%m/%d/%Y")
								if due_date < datetime.datetime.now():
										messagebox.showerror("Error", "Due date cannot be in the past.")
										return
						except ValueError:
								messagebox.showerror("Error", "Invalid date format. Use mm/dd/yyyy.")
								return
				else:
						due_date = None

				priority_str = simpledialog.askstring("Input", "Priority (1-High, 2-Medium, 3-Low):", parent=self.root)
				priority = 3 if not priority_str or priority_str not in ["1", "2", "3"] else int(priority_str)

				task = Task(name, description, due_date.strftime("%m/%d/%Y") if due_date else "N/A", priority)
				self.tasks.append(task)
				self.save_tasks()
				messagebox.showinfo("Info", "Task added successfully.")
				self.update_task_display()

		def get_priority_description(self, priority):
				return {1: "High", 2: "Medium", 3: "Low"}.get(priority, "Unknown")

		def search_task(self):
			self.search_aspect_window = tk.Toplevel(self.root)
			self.search_aspect_window.title("Select Search Aspect")
			self.search_aspect_window.geometry("300x200")

			tk.Button(self.search_aspect_window, text="By Name", command=lambda: self.search_by_aspect("name")).pack()
			tk.Button(self.search_aspect_window, text="By Description", command=lambda: self.search_by_aspect("description")).pack()
			tk.Button(self.search_aspect_window, text="By Due Date", command=lambda: self.search_by_aspect("due date")).pack()
			tk.Button(self.search_aspect_window, text="By Priority", command=lambda: self.search_by_aspect("priority")).pack()

		def search_by_aspect(self, aspect):
			self.search_aspect_window.destroy()
			search_query = simpledialog.askstring("Search", f"Enter search query for {aspect}:", parent=self.root)
			if search_query:
				if aspect == "name":
					matching_tasks = [task for task in self.tasks if search_query.lower() in task.name.lower()]
				elif aspect == "description":
					matching_tasks = [task for task in self.tasks if search_query.lower() in task.description.lower()]
				elif aspect == "due date":
					matching_tasks = [task for task in self.tasks if task.due_date == search_query]
				elif aspect == "priority":
					try:
						priority_num = int(search_query)
						matching_tasks = [task for task in self.tasks if task.priority == priority_num]
					except ValueError:
						messagebox.showerror("Error", "Priority search requires a numeric input (1-High, 2-Medium, 3-Low).")
						return
				self.show_search_results(matching_tasks)

		def show_search_results(self, tasks):
			search_result_window = tk.Toplevel(self.root)
			search_result_window.title("Search Results")
			

			result_display = ttk.Treeview(search_result_window, columns=("Name", "Description", "Due Date", "Priority", "Status"), show="headings")
			result_display.heading("Name", text="Task Name")
			result_display.heading("Description", text="Description")
			result_display.heading("Due Date", text="Due Date")
			result_display.heading("Priority", text="Priority")
			result_display.heading("Status", text="Status")
			result_display.pack(expand=True, fill='both')

			for task in tasks:
				status = "Completed" if task.completed else "Incomplete"
				result_display.insert("", tk.END, values=(task.name, task.description, task.due_date, self.get_priority_description(task.priority), status))

		def modify_task(self):
				if not self.tasks:
						messagebox.showinfo("Info", "No tasks to modify. Add tasks first.")
						return

				self.select_task_window = tk.Toplevel(self.root)
				self.select_task_window.title("Select Task to Modify")
				self.select_task_window.geometry("300x700")

				for task in self.tasks:
						tk.Button(self.select_task_window, text=task.name, command=lambda t=task: self.select_aspect_to_modify(t)).pack()

		def select_aspect_to_modify(self, task):
				self.select_task_window.destroy()
				self.modify_task_window = tk.Toplevel(self.root)
				self.modify_task_window.title("Modify Task: " + task.name)
				self.modify_task_window.geometry("300x400")
				tk.Button(self.modify_task_window, text="Name", command=lambda: self.modify_task_detail(task, "name")).pack()
				tk.Button(self.modify_task_window, text="Description", command=lambda: self.modify_task_detail(task, "description")).pack()
				tk.Button(self.modify_task_window, text="Due Date", command=lambda: self.modify_task_detail(task, "due date")).pack()
				tk.Button(self.modify_task_window, text="Priority", command=lambda: self.modify_task_detail(task, "priority")).pack()
				tk.Button(self.modify_task_window, text="Status", command=lambda: self.modify_task_detail(task, "status")).pack()

		def modify_task_detail(self, task, aspect):
				self.modify_task_window.destroy()
				if aspect == "name":
					new_name = simpledialog.askstring("Input", "Enter the new task name:", parent=self.root)
					if new_name:
						task.name = new_name
      
				elif aspect == "description":
						new_description = simpledialog.askstring("Input", "Enter the new task description:", parent=self.root)
						if new_description is not None:
								task.description = new_description

				elif aspect == "due date":
						new_due_date_str = simpledialog.askstring("Input", "Enter the new due date (mm/dd/yyyy):", parent=self.root)
						if new_due_date_str:
								try:
										new_due_date = datetime.datetime.strptime(new_due_date_str, "%m/%d/%Y")
										task.due_date = new_due_date.strftime("%m/%d/%Y")
								except ValueError:
										messagebox.showerror("Error", "Invalid date format.")

				elif aspect == "priority":
						new_priority = simpledialog.askstring("Input", "Enter the new priority (1-High, 2-Medium, 3-Low):", parent=self.root)
						if new_priority in ["1", "2", "3"]:
								task.priority = int(new_priority)

			
				elif aspect == "status":
					self.toggle_task_status(task)

				self.save_tasks()
				self.update_task_display()

		def toggle_task_status(self, task):
			if task.completed:
				if messagebox.askyesno("Incomplete Task", f"Do you want to mark '{task.name}' as incomplete?"):
					task.completed = False
			else:
				if messagebox.askyesno("Complete Task", f"Do you want to mark '{task.name}' as completed?"):
					task.completed = True



		def delete_task(self):
				if not self.tasks:
						messagebox.showinfo("Info", "No tasks to delete. Add tasks first.")
						return

				self.delete_task_window = tk.Toplevel(self.root)
				self.delete_task_window.title("Select Task to Delete")
				self.delete_task_window.geometry("300x200")

				for task in self.tasks:
						tk.Button(self.delete_task_window, text=task.name, command=lambda t=task: self.confirm_delete_task(t)).pack()

		def confirm_delete_task(self, task):
				if messagebox.askyesno("Delete Task", f"Are you sure you want to delete '{task.name}'?"):
						self.tasks.remove(task)
						self.save_tasks()
						self.update_task_display()
				self.delete_task_window.destroy()

		def update_task_display(self):
				for item in self.task_display.get_children():
						self.task_display.delete(item)

				def sort_key(task):
					due_date = datetime.datetime.strptime(task.due_date, "%m/%d/%Y") if task.due_date != "N/A" else datetime.datetime.max
					return (task.completed, due_date, -task.priority)

				sorted_tasks = sorted(self.tasks, key=sort_key)

				for task in sorted_tasks:
					status = "Completed" if task.completed else "Incomplete"
					self.task_display.insert("", tk.END, values=(task.name, task.description, task.due_date, self.get_priority_description(task.priority), status))

		def find_task_by_name(self, task_name):
				for task in self.tasks:
						if task.name == task_name:
								return task
				return None

def main():
		root = tk.Tk()
		app = TaskManagerApp(root)
		root.mainloop()

if __name__ == "__main__":
		main()
