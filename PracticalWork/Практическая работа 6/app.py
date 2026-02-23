import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

class DecisionNode:
    def __init__(self, question, yes_node=None, no_node=None, result=None):
        self.question = question
        self.yes_node = yes_node
        self.no_node = no_node
        self.result = result

class DecisionTreeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Дерево решений: Запуск нового продукта")
        self.root.geometry("1000x700")
        
        self.current_node = None
        self.history = []
        self.node_history = []
        self.build_decision_tree()
        self.current_node = self.root_node
        self.node_history.append(self.current_node)
        
        self.setup_ui()
        self.update_display()
    
    def build_decision_tree(self):
        leaf1 = DecisionNode(None, result="РЕКОМЕНДАЦИЯ: Агрессивный запуск с максимальным бюджетом. Высокий спрос, низкая конкуренция, уникальный продукт, сильная команда, есть инвестиции.")
        leaf2 = DecisionNode(None, result="РЕКОМЕНДАЦИЯ: Запуск в ограниченном режиме. Высокий спрос, низкая конкуренция, но слабая команда - наймите ключевых специалистов перед запуском.")
        leaf3 = DecisionNode(None, result="РЕКОМЕНДАЦИЯ: Запуск с фокусом на маркетинг. Высокий спрос, средняя конкуренция, бюджет позволяет выделиться.")
        leaf4 = DecisionNode(None, result="РЕКОМЕНДАЦИЯ: Нишевый запуск. Высокий спрос, средняя конкуренция, но бюджет ограничен - сфокусируйтесь на конкретном сегменте.")
        leaf5 = DecisionNode(None, result="РЕКОМЕНДАЦИЯ: Стратегия низких цен. Высокий спрос, высокая конкуренция, есть возможность демпинговать.")
        leaf6 = DecisionNode(None, result="ПРЕДУПРЕЖДЕНИЕ: Высокорисковый запуск. Высокий спрос, высокая конкуренция, слабая команда - требуется усиление или партнерство.")
        leaf7 = DecisionNode(None, result="РЕКОМЕНДАЦИЯ: Запуск с уникальным торговым предложением. Средний спрос, низкая конкуренция, продукт с изюминкой.")
        leaf8 = DecisionNode(None, result="РЕКОМЕНДАЦИЯ: Тестовый маркетинг. Средний спрос, низкая конкуренция, но бюджет ограничен - запустите пилот в одном регионе.")
        leaf9 = DecisionNode(None, result="РЕКОМЕНДАЦИЯ: Запуск после доработки. Средний спрос, средняя конкуренция, продукт нуждается в улучшениях.")
        leaf10 = DecisionNode(None, result="ПРЕДУПРЕЖДЕНИЕ: Высокий риск провала. Средний спрос, средняя конкуренция, слабая команда, низкий бюджет.")
        leaf11 = DecisionNode(None, result="РЕКОМЕНДАЦИЯ: Не запускать. Средний спрос, высокая конкуренция, слабые позиции по всем параметрам.")
        leaf12 = DecisionNode(None, result="РЕКОМЕНДАЦИЯ: Поиск инвестора. Средний спрос, высокая конкуренция, сильная команда, но нет денег.")
        leaf13 = DecisionNode(None, result="РЕКОМЕНДАЦИЯ: Отложить запуск. Низкий спрос, но уникальная технология - подождите созревания рынка.")
        leaf14 = DecisionNode(None, result="РЕКОМЕНДАЦИЯ: Искать другую нишу. Низкий спрос, слабая команда, низкий бюджет - не тратьте ресурсы.")
        leaf15 = DecisionNode(None, result="РЕКОМЕНДАЦИЯ: Запуск как дополнительный продукт. Низкий спрос, но есть существующая клиентская база.")
        leaf16 = DecisionNode(None, result="КАТЕГОРИЧЕСКИ НЕ РЕКОМЕНДУЕТСЯ. Низкий спрос, высокая конкуренция, слабая команда, нет денег - провал неизбежен.")

        node15 = DecisionNode("Есть ли у вас уникальная технология или патенты?", leaf13, leaf14)
        node14 = DecisionNode("Есть ли существующая клиентская база для кросс-продаж?", leaf15, leaf16)
        node13 = DecisionNode("Есть ли бюджет на маркетинговые исследования?", node14, node15)

        node12 = DecisionNode("Есть ли возможность привлечь инвестиции?", leaf11, leaf12)
        node11 = DecisionNode("Требует ли продукт доработок перед запуском?", leaf9, leaf10)
        node10 = DecisionNode("Сильная ли у вас команда?", node11, node12)
        
        node9 = DecisionNode("Есть ли бюджет на разработку УТП?", leaf7, leaf8)
        node8 = DecisionNode("Есть ли бюджет на тестовый запуск?", node9, node10)

        node7 = DecisionNode("Можете ли вы обеспечить низкие производственные затраты?", leaf5, leaf6)
        node6 = DecisionNode("Есть ли у вас сильная маркетинговая команда?", leaf3, leaf4)
        node5 = DecisionNode("Сильная ли у вас команда разработки?", leaf1, leaf2)
        
        node4 = DecisionNode("Есть ли бюджет на агрессивный маркетинг?", node6, node7)
        node3 = DecisionNode("Уникален ли ваш продукт по сравнению с конкурентами?", node4, node5)
        
        node2 = DecisionNode("Высокая ли конкуренция в этом сегменте?", node3, node8)
        node1 = DecisionNode("Есть ли высокий спрос на рынке?", node2, node13)
        
        self.root_node = DecisionNode("Есть ли подтвержденный спрос (исследования/опросы)?", node1, node13)
    
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        main_frame.rowconfigure(3, weight=0)
        
        left_frame = ttk.LabelFrame(main_frame, text="Дерево решений", padding="10")
        left_frame.grid(row=0, column=0, rowspan=4, sticky="nsew", padx=(0, 10))
        
        self.tree_display = scrolledtext.ScrolledText(left_frame, width=40, height=35, wrap=tk.WORD)
        self.tree_display.pack(fill=tk.BOTH, expand=True)
        
        question_frame = ttk.LabelFrame(main_frame, text="Текущий вопрос", padding="10")
        question_frame.grid(row=0, column=1, sticky="nsew", pady=(0, 10))
        
        self.question_label = ttk.Label(question_frame, text="", font=("Arial", 12, "bold"), wraplength=500)
        self.question_label.pack(fill=tk.BOTH, expand=True, pady=20)
        
        result_frame = ttk.LabelFrame(main_frame, text="Результат", padding="10")
        result_frame.grid(row=1, column=1, sticky="nsew", pady=(0, 10))
        
        self.result_label = ttk.Label(result_frame, text="", font=("Arial", 11), wraplength=500, justify=tk.LEFT)
        self.result_label.pack(fill=tk.BOTH, expand=True, pady=20)
        
        history_frame = ttk.LabelFrame(main_frame, text="История ответов", padding="10")
        history_frame.grid(row=2, column=1, sticky="nsew")
        
        self.history_text = scrolledtext.ScrolledText(history_frame, height=8, wrap=tk.WORD)
        self.history_text.pack(fill=tk.BOTH, expand=True)
        
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=3, column=1, sticky="ew", pady=(10, 0))
        
        self.btn_yes = ttk.Button(control_frame, text="Да", command=self.answer_yes, width=12)
        self.btn_yes.pack(side=tk.LEFT, padx=5)
        
        self.btn_no = ttk.Button(control_frame, text="Нет", command=self.answer_no, width=12)
        self.btn_no.pack(side=tk.LEFT, padx=5)
        
        self.btn_back = ttk.Button(control_frame, text="← Назад", command=self.go_back, width=12)
        self.btn_back.pack(side=tk.LEFT, padx=5)
        
        self.btn_reset = ttk.Button(control_frame, text="Сбросить", command=self.reset_tree, width=12)
        self.btn_reset.pack(side=tk.LEFT, padx=5)
        
        self.info_label = ttk.Label(control_frame, text="Всего вопросов: 7-10", font=("Arial", 9))
        self.info_label.pack(side=tk.RIGHT, padx=10)
        
        self.update_tree_display()
    
    def update_tree_display(self):
        self.tree_display.delete(1.0, tk.END)
        self.tree_display.insert(tk.END, "ДЕРЕВО РЕШЕНИЙ (запуск продукта)\n", "title")
        self.tree_display.insert(tk.END, "═"*40 + "\n\n")
        self.tree_display.tag_configure("title", font=("Arial", 11, "bold"), foreground="darkblue")
        self.display_node(self.root_node, 0)
    
    def display_node(self, node, level):
        if not node:
            return
        
        indent = "  " * level
        
        if node == self.current_node and node.question:
            self.tree_display.insert(tk.END, f"{indent}▶ ", "highlight")
            self.tree_display.tag_configure("highlight", foreground="red", font=("Arial", 10, "bold"))
        else:
            self.tree_display.insert(tk.END, f"{indent}  ")
        
        if node.question:
            if level == 0:
                self.tree_display.insert(tk.END, f"📋 {node.question}\n")
            else:
                self.tree_display.insert(tk.END, f"❓ {node.question}\n")
            self.display_node(node.yes_node, level + 1)
            self.display_node(node.no_node, level + 1)
        elif node.result:
            lines = node.result.split(". ")
            for i, line in enumerate(lines):
                if i == 0:
                    self.tree_display.insert(tk.END, f"{indent}  📌 {line}")
                else:
                    self.tree_display.insert(tk.END, f"{indent}     {line}")
                if i < len(lines)-1:
                    self.tree_display.insert(tk.END, ".\n")
            self.tree_display.insert(tk.END, "\n")
    
    def update_display(self):
        if self.current_node.question:
            self.question_label.config(text=self.current_node.question)
            self.result_label.config(text="")
            self.btn_yes.config(state=tk.NORMAL)
            self.btn_no.config(state=tk.NORMAL)
        else:
            self.question_label.config(text="✅ РЕШЕНИЕ ПРИНЯТО")
            self.result_label.config(text=self.current_node.result, foreground="darkgreen")
            self.btn_yes.config(state=tk.DISABLED)
            self.btn_no.config(state=tk.DISABLED)
        
        self.update_history_display()
        self.update_tree_display()
    
    def update_history_display(self):
        self.history_text.delete(1.0, tk.END)
        if not self.history:
            self.history_text.insert(tk.END, "История пуста. Начните отвечать на вопросы.")
            return
        
        for i, entry in enumerate(self.history, 1):
            if "Да" in entry:
                self.history_text.insert(tk.END, f"{i}. {entry}\n", "yes_answer")
            else:
                self.history_text.insert(tk.END, f"{i}. {entry}\n", "no_answer")
        
        self.history_text.tag_configure("yes_answer", foreground="green")
        self.history_text.tag_configure("no_answer", foreground="red")
    
    def answer_yes(self):
        if self.current_node and self.current_node.yes_node:
            self.history.append(f"Вопрос: {self.current_node.question} -> ОТВЕТ: ДА")
            self.node_history.append(self.current_node)
            self.current_node = self.current_node.yes_node
            self.update_display()
    
    def answer_no(self):
        if self.current_node and self.current_node.no_node:
            self.history.append(f"Вопрос: {self.current_node.question} -> ОТВЕТ: НЕТ")
            self.node_history.append(self.current_node)
            self.current_node = self.current_node.no_node
            self.update_display()
    
    def go_back(self):
        if len(self.node_history) > 1:
            self.node_history.pop()
            self.current_node = self.node_history[-1]
            if self.history:
                self.history.pop()
            self.update_display()
        else:
            messagebox.showinfo("Информация", "Вы уже в начале дерева решений")
    
    def reset_tree(self):
        result = messagebox.askyesno("Подтверждение", "Сбросить все ответы и начать заново?")
        if result:
            self.current_node = self.root_node
            self.history = []
            self.node_history = [self.current_node]
            self.update_display()

if __name__ == "__main__":
    root = tk.Tk()
    app = DecisionTreeApp(root)
    root.mainloop()