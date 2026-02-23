import tkinter as tk
from tkinter import messagebox, simpledialog
import math
import uuid

class Atom:
    def __init__(self, x, y, element='C', name=None):
        self.id = str(uuid.uuid4())
        self.x = x
        self.y = y
        self.element = element
        self.name = name if name else element
        self.canvas_id = None
        self.text_id = None
        self.selected = False
        self.connections = []
        self.bond_count = 0
    
    def get_valence(self):
        valence_dict = {'C': 4, 'H': 1, 'O': 2, 'N': 3}
        return valence_dict.get(self.element, 4)

class Bond:
    def __init__(self, atom1, atom2, bond_type=1):
        self.id = str(uuid.uuid4())
        self.atom1 = atom1
        self.atom2 = atom2
        self.bond_type = bond_type
        self.canvas_id = None
        self.text_id = None
        self.selected = False

class MoleculeEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Редактор структурных формул (Вариант 12)")
        self.root.geometry("1000x700")
        
        self.atoms = []
        self.bonds = []
        self.selected_atom = None
        self.selected_bond = None
        self.temp_bond_atom = None
        self.drag_data = None
        self.current_element = 'C'
        self.atom_radius = 20
        
        self.setup_ui()
        self.setup_bindings()
    
    def setup_ui(self):
        self.canvas = tk.Canvas(self.root, bg='white', width=800, height=600)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        control_panel = tk.Frame(self.root, width=200, bg='lightgray')
        control_panel.pack(side=tk.RIGHT, fill=tk.Y)
        control_panel.pack_propagate(False)
        
        tk.Label(control_panel, text="Элементы", bg='lightgray', font=('Arial', 12, 'bold')).pack(pady=10)
        
        elements = [('Углерод (C)', 'C', 'gray'), ('Водород (H)', 'H', 'lightblue'), 
                   ('Кислород (O)', 'O', 'red'), ('Азот (N)', 'N', 'blue')]
        for text, elem, color in elements:
            btn = tk.Button(control_panel, text=text, bg=color, fg='white' if elem!='H' else 'black', 
                          width=20, command=lambda e=elem: self.set_current_element(e))
            btn.pack(pady=2)
        
        tk.Label(control_panel, text="Действия", bg='lightgray', font=('Arial', 12, 'bold')).pack(pady=10)
        
        tk.Button(control_panel, text="Проверить валентность", bg='yellow', width=20,
                 command=self.check_valence).pack(pady=5)
        
        tk.Button(control_panel, text="Редактировать связь", bg='orange', width=20,
                 command=self.edit_selected_bond).pack(pady=5)
        
        tk.Button(control_panel, text="Снять выделение", bg='lightblue', width=20,
                 command=self.deselect_all).pack(pady=5)
        
        tk.Button(control_panel, text="Очистить всё", bg='red', fg='white', width=20,
                 command=self.clear_all).pack(pady=5)
        
        self.status_label = tk.Label(control_panel, text="Готов к работе", bg='lightgray', wraplength=180)
        self.status_label.pack(pady=10)
        
        tk.Label(control_panel, text="Управление:", bg='lightgray', font=('Arial', 10, 'bold')).pack(pady=5)
        tk.Label(control_panel, text="ЛКМ - выбрать/переместить\nShift+ЛКМ - создать связь\nПКМ - контекстное меню\nCtrl+ЛКМ - создать атом\nCtrl+E - изменить элемент", 
                bg='lightgray', justify=tk.LEFT).pack(pady=5)
    
    def setup_bindings(self):
        self.canvas.bind("<Button-1>", self.on_left_click)
        self.canvas.bind("<Button-3>", self.on_right_click)
        self.canvas.bind("<Shift-Button-1>", self.on_shift_click)
        self.canvas.bind("<Control-Button-1>", self.on_ctrl_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_drag_end)
        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.root.bind("<Control-e>", self.on_ctrl_e)
        self.root.bind("<Control-E>", self.on_ctrl_e)
    
    def set_current_element(self, element):
        self.current_element = element
        color = {'C': 'серый', 'H': 'голубой', 'O': 'красный', 'N': 'синий'}.get(element, '')
        self.update_status(f"Выбран элемент: {element} ({color})")
    
    def find_atom(self, x, y):
        for atom in self.atoms:
            if math.sqrt((atom.x - x)**2 + (atom.y - y)**2) <= self.atom_radius:
                return atom
        return None
    
    def find_bond(self, x, y):
        for bond in self.bonds:
            x1, y1 = bond.atom1.x, bond.atom1.y
            x2, y2 = bond.atom2.x, bond.atom2.y
            
            line_length = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            if line_length == 0:
                continue
            
            distance = abs((y2 - y1)*x - (x2 - x1)*y + x2*y1 - y2*x1) / line_length
            
            if distance <= 5:
                t = ((x - x1)*(x2 - x1) + (y - y1)*(y2 - y1)) / (line_length**2)
                if 0 <= t <= 1:
                    return bond
        return None
    
    def create_atom(self, x, y):
        if self.find_atom(x, y):
            return
        
        atom = Atom(x, y, self.current_element)
        
        color = {'C': 'gray', 'H': 'lightblue', 'O': 'red', 'N': 'blue'}.get(atom.element, 'purple')
        text_color = 'black' if atom.element == 'H' else 'white'
        
        atom.canvas_id = self.canvas.create_oval(x-self.atom_radius, y-self.atom_radius,
                                                x+self.atom_radius, y+self.atom_radius,
                                                fill=color, outline='black', width=2)
        atom.text_id = self.canvas.create_text(x, y, text=atom.element, 
                                              font=('Arial', 12, 'bold'), fill=text_color)
        
        self.atoms.append(atom)
        self.update_status(f"Создан атом {atom.element} (ID: {atom.id[:8]}...)")
        return atom
    
    def create_bond(self, atom1, atom2):
        if atom1 == atom2:
            self.update_status("Нельзя создать связь с самим собой")
            return
        
        for bond in self.bonds:
            if (bond.atom1 == atom1 and bond.atom2 == atom2) or \
               (bond.atom1 == atom2 and bond.atom2 == atom1):
                self.update_status("Связь уже существует")
                return
        
        distance = math.sqrt((atom1.x - atom2.x)**2 + (atom1.y - atom2.y)**2)
        if distance > 150:
            self.update_status("Атомы слишком далеко друг от друга")
            return
        
        bond_type = simpledialog.askinteger("Тип связи", "Введите тип связи (1 - одинарная, 2 - двойная):",
                                           minvalue=1, maxvalue=2)
        if bond_type is None:
            bond_type = 1
        
        bond = Bond(atom1, atom2, bond_type)
        
        bond.canvas_id = self.canvas.create_line(atom1.x, atom1.y, atom2.x, atom2.y,
                                                fill='black', width=2 if bond_type==1 else 4)
        
        mid_x = (atom1.x + atom2.x) / 2
        mid_y = (atom1.y + atom2.y) / 2
        bond.text_id = self.canvas.create_text(mid_x, mid_y, text=f"{bond_type}",
                                              font=('Arial', 10), fill='darkblue')
        
        atom1.connections.append(atom2)
        atom2.connections.append(atom1)
        atom1.bond_count += bond_type
        atom2.bond_count += bond_type
        
        self.bonds.append(bond)
        self.update_status(f"Создана {bond_type}-ная связь")
        return bond
    
    def delete_atom(self, atom):
        bonds_to_delete = []
        for bond in self.bonds[:]:
            if bond.atom1 == atom or bond.atom2 == atom:
                bonds_to_delete.append(bond)
                self.canvas.delete(bond.canvas_id)
                if bond.text_id:
                    self.canvas.delete(bond.text_id)
        
        for bond in bonds_to_delete:
            self.bonds.remove(bond)
            if bond.atom1 in atom.connections:
                bond.atom1.connections.remove(atom)
                bond.atom1.bond_count -= bond.bond_type
            if bond.atom2 in atom.connections:
                bond.atom2.connections.remove(atom)
                bond.atom2.bond_count -= bond.bond_type
        
        if atom.text_id:
            self.canvas.delete(atom.text_id)
        if atom.canvas_id:
            self.canvas.delete(atom.canvas_id)
        
        self.atoms.remove(atom)
        if self.selected_atom == atom:
            self.selected_atom = None
        if self.temp_bond_atom == atom:
            self.temp_bond_atom = None
            self.canvas.delete("temp_line")
        
        self.update_status(f"Атом {atom.element} удален")
    
    def delete_bond(self, bond):
        self.canvas.delete(bond.canvas_id)
        if bond.text_id:
            self.canvas.delete(bond.text_id)
        
        if bond.atom1 in bond.atom2.connections:
            bond.atom2.connections.remove(bond.atom1)
        if bond.atom2 in bond.atom1.connections:
            bond.atom1.connections.remove(bond.atom2)
        
        bond.atom1.bond_count -= bond.bond_type
        bond.atom2.bond_count -= bond.bond_type
        
        self.bonds.remove(bond)
        if self.selected_bond == bond:
            self.selected_bond = None
        
        self.update_status("Связь удалена")
    
    def select_atom(self, atom):
        self.deselect_all()
        atom.selected = True
        self.selected_atom = atom
        self.canvas.itemconfig(atom.canvas_id, outline='red', width=3)
        valence = atom.get_valence()
        self.update_status(f"Выбран атом {atom.element}, связей: {atom.bond_count}/{valence}")
    
    def select_bond(self, bond):
        self.deselect_all()
        bond.selected = True
        self.selected_bond = bond
        self.canvas.itemconfig(bond.canvas_id, fill='red', width=4 if bond.bond_type==2 else 3)
        self.update_status(f"Выбрана {bond.bond_type}-ная связь")
    
    def deselect_all(self):
        for atom in self.atoms:
            atom.selected = False
            self.canvas.itemconfig(atom.canvas_id, outline='black', width=2)
        
        for bond in self.bonds:
            bond.selected = False
            self.canvas.itemconfig(bond.canvas_id, fill='black', width=2 if bond.bond_type==1 else 4)
        
        self.selected_atom = None
        self.selected_bond = None
    
    def edit_atom_element(self, atom):
        elements = {'C': 'Углерод (C)', 'H': 'Водород (H)', 'O': 'Кислород (O)', 'N': 'Азот (N)'}
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Выбор элемента")
        dialog.geometry("300x250")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Выберите новый элемент:").pack(pady=10)
        
        listbox = tk.Listbox(dialog, height=4)
        for elem, name in elements.items():
            listbox.insert(tk.END, f"{name}")
        listbox.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        def on_select():
            selection = listbox.curselection()
            if selection:
                new_element = ['C', 'H', 'O', 'N'][selection[0]]
                old_element = atom.element
                atom.element = new_element
                
                color = {'C': 'gray', 'H': 'lightblue', 'O': 'red', 'N': 'blue'}.get(new_element, 'purple')
                text_color = 'black' if new_element == 'H' else 'white'
                
                self.canvas.itemconfig(atom.canvas_id, fill=color)
                self.canvas.itemconfig(atom.text_id, text=new_element, fill=text_color)
                
                self.update_status(f"Атом изменен с {old_element} на {new_element}")
            dialog.destroy()
        
        tk.Button(dialog, text="Выбрать", command=on_select).pack(pady=10)
    
    def edit_bond(self, bond):
        new_type = simpledialog.askinteger("Тип связи", "Введите новый тип связи (1 - одинарная, 2 - двойная):",
                                          minvalue=1, maxvalue=2, initialvalue=bond.bond_type)
        if new_type and new_type != bond.bond_type:
            old_type = bond.bond_type
            bond.atom1.bond_count = bond.atom1.bond_count - old_type + new_type
            bond.atom2.bond_count = bond.atom2.bond_count - old_type + new_type
            bond.bond_type = new_type
            
            self.canvas.itemconfig(bond.canvas_id, width=2 if new_type==1 else 4)
            self.canvas.itemconfig(bond.text_id, text=str(new_type))
            
            self.update_status(f"Тип связи изменен с {old_type} на {new_type}")
    
    def edit_selected_bond(self):
        if self.selected_bond:
            self.edit_bond(self.selected_bond)
        else:
            self.update_status("Сначала выберите связь")
    
    def show_context_menu(self, event, atom=None, bond=None):
        menu = tk.Menu(self.root, tearoff=0)
        
        if atom:
            menu.add_command(label="Изменить элемент", command=lambda: self.edit_atom_element(atom))
            menu.add_separator()
            menu.add_command(label="Удалить атом", command=lambda: self.delete_atom(atom))
        elif bond:
            menu.add_command(label="Изменить тип связи", command=lambda: self.edit_bond(bond))
            menu.add_separator()
            menu.add_command(label="Удалить связь", command=lambda: self.delete_bond(bond))
        else:
            menu.add_command(label="Создать атом", command=lambda: self.create_atom(event.x, event.y))
        
        menu.post(event.x_root, event.y_root)
    
    def on_left_click(self, event):
        self.drag_data = {'x': event.x, 'y': event.y, 'atom': None}
        
        atom = self.find_atom(event.x, event.y)
        if atom:
            self.select_atom(atom)
            self.drag_data['atom'] = atom
        else:
            bond = self.find_bond(event.x, event.y)
            if bond:
                self.select_bond(bond)
            else:
                self.deselect_all()
    
    def on_drag(self, event):
        if self.drag_data and self.drag_data['atom']:
            atom = self.drag_data['atom']
            
            dx = event.x - self.drag_data['x']
            dy = event.y - self.drag_data['y']
            
            self.canvas.move(atom.canvas_id, dx, dy)
            self.canvas.move(atom.text_id, dx, dy)
            
            for bond in self.bonds:
                if bond.atom1 == atom or bond.atom2 == atom:
                    x1, y1 = bond.atom1.x, bond.atom1.y
                    x2, y2 = bond.atom2.x, bond.atom2.y
                    self.canvas.coords(bond.canvas_id, x1, y1, x2, y2)
                    
                    mid_x = (x1 + x2) / 2
                    mid_y = (y1 + y2) / 2
                    self.canvas.coords(bond.text_id, mid_x, mid_y)
            
            self.drag_data['x'] = event.x
            self.drag_data['y'] = event.y
    
    def on_drag_end(self, event):
        if self.drag_data and self.drag_data['atom']:
            atom = self.drag_data['atom']
            atom.x = event.x
            atom.y = event.y
            self.drag_data = None
    
    def on_right_click(self, event):
        atom = self.find_atom(event.x, event.y)
        if atom:
            self.show_context_menu(event, atom=atom)
        else:
            bond = self.find_bond(event.x, event.y)
            if bond:
                self.show_context_menu(event, bond=bond)
            else:
                self.show_context_menu(event)
    
    def on_shift_click(self, event):
        atom = self.find_atom(event.x, event.y)
        if atom and self.temp_bond_atom is None:
            self.temp_bond_atom = atom
            self.canvas.itemconfig(atom.canvas_id, outline='blue', width=3)
            self.update_status("Выберите второй атом для создания связи")
        elif atom and self.temp_bond_atom:
            self.create_bond(self.temp_bond_atom, atom)
            self.canvas.itemconfig(self.temp_bond_atom.canvas_id, outline='black', width=2)
            self.temp_bond_atom = None
            self.canvas.delete("temp_line")
    
    def on_ctrl_click(self, event):
        if not self.find_atom(event.x, event.y):
            self.create_atom(event.x, event.y)
    
    def on_ctrl_e(self, event):
        if self.selected_atom:
            self.edit_atom_element(self.selected_atom)
        else:
            self.update_status("Сначала выберите атом")
    
    def on_mouse_move(self, event):
        if self.temp_bond_atom:
            self.canvas.delete("temp_line")
            self.canvas.create_line(self.temp_bond_atom.x, self.temp_bond_atom.y,
                                   event.x, event.y, fill='blue', width=2, dash=(5, 5), tag="temp_line")
    
    def check_valence(self):
        errors = []
        for atom in self.atoms:
            max_valence = atom.get_valence()
            if atom.bond_count > max_valence:
                errors.append(f"Атом {atom.element} (ID: {atom.id[:8]}...): связей {atom.bond_count}, максимум {max_valence}")
            elif atom.bond_count < max_valence and atom.element != 'H':
                pass
        
        if errors:
            messagebox.showwarning("Ошибки валентности", "\n".join(errors))
            for atom in self.atoms:
                if atom.bond_count > atom.get_valence():
                    self.canvas.itemconfig(atom.canvas_id, outline='red', width=3)
                else:
                    self.canvas.itemconfig(atom.canvas_id, outline='black', width=2)
        else:
            messagebox.showinfo("Проверка", "Все валентности соблюдены!")
            self.update_status("Валентности в порядке")
    
    def clear_all(self):
        if messagebox.askyesno("Подтверждение", "Очистить всё?"):
            for atom in self.atoms:
                self.canvas.delete(atom.canvas_id)
                self.canvas.delete(atom.text_id)
            for bond in self.bonds:
                self.canvas.delete(bond.canvas_id)
                self.canvas.delete(bond.text_id)
            
            self.atoms.clear()
            self.bonds.clear()
            self.selected_atom = None
            self.selected_bond = None
            self.temp_bond_atom = None
            self.drag_data = None
            self.canvas.delete("temp_line")
            self.update_status("Все очищено")
    
    def update_status(self, message):
        self.status_label.config(text=message)

if __name__ == "__main__":
    root = tk.Tk()
    app = MoleculeEditor(root)
    root.mainloop()