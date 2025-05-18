import tkinter as tk
from tkinter import messagebox

def find_minimum_people(item_to_people):
    # Invert the mapping: person -> items
    person_to_items = {}
    all_items = set()

    for item, people in item_to_people.items():
        all_items.add(item)
        for person in [p.strip() for p in people.split(",") if p.strip()]:
            if person not in person_to_items:
                person_to_items[person] = set()
            person_to_items[person].add(item)

    needed = set(all_items)
    selected_people = []
    result = {}

    while needed:
        best_person = None
        covered = set()
        for person, items in person_to_items.items():
            cover = needed & items
            if len(cover) > len(covered):
                best_person = person
                covered = cover

        if not best_person:
            break  # no one can cover remaining items

        selected_people.append(best_person)
        result[best_person] = list(covered)
        needed -= covered

    return selected_people, result

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Item Supplier Optimizer")
        self.entries = []

        self.frame = tk.Frame(root)
        self.frame.pack(padx=20, pady=20)

        self.add_row()

        self.add_btn = tk.Button(root, text="+ Add Item", command=self.add_row)
        self.add_btn.pack(pady=5)

        self.run_btn = tk.Button(root, text="Find Minimum People", command=self.solve)
        self.run_btn.pack(pady=10)

        self.result_text = tk.Text(root, height=15, width=60)
        self.result_text.pack(pady=10)

    def add_row(self):
        row_frame = tk.Frame(self.frame)
        row_frame.pack(pady=2)

        item_entry = tk.Entry(row_frame, width=25)
        item_entry.insert(0, "Item")
        item_entry.pack(side=tk.LEFT, padx=5)

        people_entry = tk.Entry(row_frame, width=35)
        people_entry.insert(0, "Person1, Person2")
        people_entry.pack(side=tk.LEFT)

        self.entries.append((item_entry, people_entry))

    def solve(self):
        item_to_people = {}
        for item_entry, people_entry in self.entries:
            item = item_entry.get().strip()
            people = people_entry.get().strip()
            if item and people:
                item_to_people[item] = people

        if not item_to_people:
            messagebox.showerror("Input Error", "Please enter at least one item.")
            return

        people, assignments = find_minimum_people(item_to_people)

        output = "✅ People to Contact:\n" + ", ".join(people) + "\n\n"
        output += "📦 Order Plan:\n"
        for person, items in assignments.items():
            output += f" - {person}: {', '.join(items)}\n"

        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, output)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
