import tkinter as tk
from tkinter import messagebox, ttk
import asyncio
from main import create_server

class DisjorkDadosGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hygark's DisjorkDados")
        self.root.geometry("800x700")
        self.root.configure(bg="#2c2f33")
        
        # Estilo
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12), padding=10)
        style.configure("TLabel", font=("Arial", 12), background="#2c2f33", foreground="#ffffff")
        style.configure("TEntry", font=("Arial", 12))
        
        # Título
        title_frame = tk.Frame(root, bg="#2c2f33")
        title_frame.pack(pady=10)
        tk.Label(
            title_frame, 
            text="Hygark's DisjorkDados", 
            font=("Arial", 20, "bold"), 
            bg="#2c2f33", 
            fg="#7289da"
        ).pack()
        tk.Label(
            title_frame, 
            text="Crie servidores Discord manual ou automatizado!", 
            font=("Arial", 10, "italic"), 
            bg="#2c2f33", 
            fg="#ffffff"
        ).pack()

        # Modo (Manual ou Automatizado)
        mode_frame = ttk.Frame(root)
        mode_frame.pack(pady=10)
        ttk.Label(mode_frame, text="Modo:").pack(side="left", padx=5)
        self.mode_var = tk.StringVar(value="Manual")
        ttk.Radiobutton(mode_frame, text="Manual", variable=self.mode_var, value="Manual", command=self.toggle_mode).pack(side="left", padx=5)
        ttk.Radiobutton(mode_frame, text="Automatizado", variable=self.mode_var, value="Automatizado", command=self.toggle_mode).pack(side="left", padx=5)
        
        # Formulário principal
        self.form_frame = ttk.Frame(root)
        self.form_frame.pack(padx=20, pady=10, fill="both")
        
        # Campos para modo Manual
        self.manual_frame = ttk.Frame(self.form_frame)
        ttk.Label(self.manual_frame, text="Bot Token:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.token_entry = ttk.Entry(self.manual_frame, width=40, show="*")
        self.token_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Formulário para estrutura manual
        self.structure_frame = ttk.Frame(self.manual_frame)
        self.structure_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        
        ttk.Label(self.structure_frame, text="Estrutura Manual:").pack(anchor="w")
        self.categories = []
        self.channels = []
        self.roles = []
        
        # Adicionar Categoria
        ttk.Button(self.structure_frame, text="Adicionar Categoria", command=self.add_category).pack(anchor="w", pady=2)
        self.category_listbox = tk.Listbox(self.structure_frame, height=3, width=50)
        self.category_listbox.pack(anchor="w", pady=2)
        
        # Adicionar Canal
        ttk.Label(self.structure_frame, text="Canal: Nome").pack(anchor="w")
        self.channel_name_entry = ttk.Entry(self.structure_frame, width=30)
        self.channel_name_entry.pack(anchor="w")
        ttk.Label(self.structure_frame, text="Tipo de Canal:").pack(anchor="w")
        self.channel_type_var = tk.StringVar(value="text")
        self.channel_type_combo = ttk.Combobox(self.structure_frame, textvariable=self.channel_type_var, values=["text", "voice"])
        self.channel_type_combo.pack(anchor="w")
        ttk.Label(self.structure_frame, text="Categoria:").pack(anchor="w")
        self.channel_category_var = tk.StringVar()
        self.channel_category_combo = ttk.Combobox(self.structure_frame, textvariable=self.channel_category_var, values=[""])
        self.channel_category_combo.pack(anchor="w")
        ttk.Label(self.structure_frame, text="Tópico (para text/announcement):").pack(anchor="w")
        self.channel_topic_entry = ttk.Entry(self.structure_frame, width=30)
        self.channel_topic_entry.pack(anchor="w")
        ttk.Button(self.structure_frame, text="Adicionar Canal", command=self.add_channel).pack(anchor="w", pady=2)
        self.channel_listbox = tk.Listbox(self.structure_frame, height=3, width=50)
        self.channel_listbox.pack(anchor="w", pady=2)
        
        # Adicionar Cargo
        ttk.Label(self.structure_frame, text="Cargo: Nome").pack(anchor="w")
        self.role_name_entry = ttk.Entry(self.structure_frame, width=30)
        self.role_name_entry.pack(anchor="w")
        ttk.Label(self.structure_frame, text="Permissões (ex.: all, none):").pack(anchor="w")
        self.role_perm_entry = ttk.Entry(self.structure_frame, width=30)
        self.role_perm_entry.pack(anchor="w")
        ttk.Label(self.structure_frame, text="Cor (ex.: #00ff00):").pack(anchor="w")
        self.role_color_entry = ttk.Entry(self.structure_frame, width=30)
        self.role_color_entry.pack(anchor="w")
        ttk.Button(self.structure_frame, text="Adicionar Cargo", command=self.add_role).pack(anchor="w", pady=2)
        self.role_listbox = tk.Listbox(self.structure_frame, height=3, width=50)
        self.role_listbox.pack(anchor="w", pady=2)
        
        # Campos para modo Automatizado
        self.auto_frame = ttk.Frame(self.form_frame)
        ttk.Label(self.auto_frame, text="Bot Token:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.auto_token_entry = ttk.Entry(self.auto_frame, width=40, show="*")
        self.auto_token_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Ordem de Clonagem
        self.order_var = tk.StringVar(value="roles,categories,channels")
        ttk.Label(root, text="Ordem de Clonagem:").pack(pady=5)
        ttk.Entry(root, textvariable=self.order_var, width=50).pack(pady=5)
        
        # Nível de Log
        self.log_var = tk.StringVar(value="normal")
        ttk.Label(root, text="Nível de Log:").pack(pady=5)
        ttk.Radiobutton(root, text="Normal", variable=self.log_var, value="normal").pack()
        ttk.Radiobutton(root, text="Detalhado", variable=self.log_var, value="detailed").pack()
        
        # Barra de Progresso
        self.progress = ttk.Progressbar(root, mode="indeterminate")
        self.progress.pack(pady=10)
        self.status_label = ttk.Label(root, text="")
        self.status_label.pack(pady=5)
        
        # Botão Iniciar
        ttk.Button(root, text="Iniciar Clonagem/Restauração", command=self.start_clone).pack(pady=20)
        
        # Modo padrão (Manual)
        self.toggle_mode()
    
    def toggle_mode(self):
        mode = self.mode_var.get()
        if mode == "Manual":
            self.manual_frame.pack()
            self.auto_frame.pack_forget()
        else:
            self.manual_frame.pack_forget()
            self.auto_frame.pack()
    
    def add_category(self):
        name = messagebox.askstring("Adicionar Categoria", "Nome da Categoria:")
        if name:
            self.categories.append({"name": name, "position": len(self.categories)})
            self.category_listbox.insert(tk.END, name)
            self.update_category_combo()
    
    def add_channel(self):
        name = self.channel_name_entry.get()
        type_ = self.channel_type_var.get()
        category = self.channel_category_var.get() or None
        topic = self.channel_topic_entry.get() if type_ == "text" else ""
        if name:
            self.channels.append({"name": name, "type": type_, "category": category, "position": len(self.channels), "topic": topic})
            self.channel_listbox.insert(tk.END, f"{name} ({type_})" + (f" in {category}" if category else "") + (f" - {topic}" if topic else ""))
            self.channel_name_entry.delete(0, tk.END)
            self.channel_topic_entry.delete(0, tk.END)
    
    def add_role(self):
        name = self.role_name_entry.get()
        perms = self.role_perm_entry.get()
        color = self.role_color_entry.get()
        if name:
            self.roles.append({"name": name, "permissions": perms, "color": color, "hoist": False, "mentionable": False})
            self.role_listbox.insert(tk.END, f"{name} ({perms}, {color})")
            self.role_name_entry.delete(0, tk.END)
            self.role_perm_entry.delete(0, tk.END)
            self.role_color_entry.delete(0, tk.END)
            self.role_color_entry.insert(0, "#000000")
    
    def update_category_combo(self):
        self.channel_category_combo['values'] = [""] + [cat["name"] for cat in self.categories]
    
    def start_clone(self):
        mode = self.mode_var.get()
        order = self.order_var.get()
        log_level = self.log_var.get()
        
        config = {"order": order, "log_level": log_level}
        
        if mode == "Manual":
            token = self.manual_token_entry.get()
            if not token:
                messagebox.showerror("Erro", "Preencha o bot token!")
                return
            if self.categories or self.channels or self.roles:
                config.update({"categories": self.categories, "channels": self.channels, "roles": self.roles})
            else:
                messagebox.showerror("Erro", "Adicione categorias/canais/cargos!")
                return
        else:
            token = self.auto_token_entry.get()
            if not token:
                messagebox.showerror("Erro", "Preencha o bot token!")
                return
        
        self.progress.start()
        self.status_label.config(text="Criando servidor... Aguarde!")
        self.root.update()
        
        try:
            asyncio.run(main(token, config, mode == "Automatizado"))
            self.progress.stop()
            self.status_label.config(text="Processo concluído!")
            messagebox.showinfo("Sucesso", "Servidor criado com sucesso!")
        except Exception as e:
            self.progress.stop()
            self.status_label.config(text="Erro no processo!")
            messagebox.showerror("Erro", f"Falha: {str(e)}")

if __name__ == '__main__':
    root = tk.Tk()
    app = DisjorkDadosGUI(root)
    root.mainloop()