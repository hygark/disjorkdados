import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import asyncio
import json
from main import main

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
        
        # Título com logo
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
            text="Clone ou restaure servidores Discord com estilo!", 
            font=("Arial", 10, "italic"), 
            bg="#2c2f33", 
            fg="#ffffff"
        ).pack()

        # Modo (Bot ou Manual)
        mode_frame = ttk.Frame(root)
        mode_frame.pack(pady=10)
        ttk.Label(mode_frame, text="Modo:").pack(side="left", padx=5)
        self.mode_var = tk.StringVar(value="Manual")  # Modo Manual como padrão
        ttk.Radiobutton(mode_frame, text="Bot", variable=self.mode_var, value="Bot", command=self.toggle_mode).pack(side="left", padx=5)
        ttk.Radiobutton(mode_frame, text="Manual", variable=self.mode_var, value="Manual", command=self.toggle_mode).pack(side="left", padx=5)
        
        # Formulário principal
        self.form_frame = ttk.Frame(root)
        self.form_frame.pack(padx=20, pady=10, fill="both")
        
        # Campos para modo Bot
        self.bot_frame = ttk.Frame(self.form_frame)
        ttk.Label(self.bot_frame, text="Bot Token:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.token_entry = ttk.Entry(self.bot_frame, width=40, show="*")
        self.token_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.bot_frame, text="ID do servidor origem:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.source_entry = ttk.Entry(self.bot_frame, width=40)
        self.source_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(self.bot_frame, text="ID do servidor destino:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.dest_entry = ttk.Entry(self.bot_frame, width=40)
        self.dest_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Campos para modo Manual
        self.manual_frame = ttk.Frame(self.form_frame)
        ttk.Label(self.manual_frame, text="Bot Token:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.manual_token_entry = ttk.Entry(self.manual_frame, width=40, show="*")
        self.manual_token_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.manual_frame, text="ID do servidor destino:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.manual_dest_entry = ttk.Entry(self.manual_frame, width=40)
        self.manual_dest_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Formulário para estrutura manual
        self.structure_frame = ttk.Frame(self.manual_frame)
        self.structure_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        
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
        self.channel_name_entry.pack(anchor="w", pady=2)
        ttk.Label(self.structure_frame, text="Tipo:").pack(anchor="w")
        self.channel_type_var = tk.StringVar(value="text")
        ttk.Combobox(self.structure_frame, textvariable=self.channel_type_var, values=["text", "voice", "forum", "announcement", "stage"], state="readonly").pack(anchor="w", pady=2)
        ttk.Label(self.structure_frame, text="Categoria (opcional):").pack(anchor="w")
        self.channel_category_var = tk.StringVar()
        self.channel_category_combo = ttk.Combobox(self.structure_frame, textvariable=self.channel_category_var, state="readonly")
        self.channel_category_combo.pack(anchor="w", pady=2)
        ttk.Label(self.structure_frame, text="Tópico (opcional, para texto/anúncio):").pack(anchor="w")
        self.channel_topic_entry = ttk.Entry(self.structure_frame, width=30)
        self.channel_topic_entry.pack(anchor="w", pady=2)
        ttk.Button(self.structure_frame, text="Adicionar Canal", command=self.add_channel).pack(anchor="w", pady=2)
        self.channel_listbox = tk.Listbox(self.structure_frame, height=5, width=50)
        self.channel_listbox.pack(anchor="w", pady=2)
        
        # Adicionar Cargo
        ttk.Label(self.structure_frame, text="Cargo: Nome").pack(anchor="w")
        self.role_name_entry = ttk.Entry(self.structure_frame, width=30)
        self.role_name_entry.pack(anchor="w", pady=2)
        ttk.Label(self.structure_frame, text="Permissões (ex.: administrator, view_channel):").pack(anchor="w")
        self.role_perm_entry = ttk.Entry(self.structure_frame, width=30)
        self.role_perm_entry.pack(anchor="w", pady=2)
        ttk.Label(self.structure_frame, text="Cor (ex.: #FF0000):").pack(anchor="w")
        self.role_color_entry = ttk.Entry(self.structure_frame, width=30)
        self.role_color_entry.insert(0, "#000000")
        self.role_color_entry.pack(anchor="w", pady=2)
        ttk.Button(self.structure_frame, text="Adicionar Cargo", command=self.add_role).pack(anchor="w", pady=2)
        self.role_listbox = tk.Listbox(self.structure_frame, height=3, width=50)
        self.role_listbox.pack(anchor="w", pady=2)
        
        # JSON opcional
        ttk.Label(self.manual_frame, text="Configuração JSON (opcional):").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.json_entry = ttk.Entry(self.manual_frame, width=30)
        self.json_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        ttk.Button(self.manual_frame, text="Carregar JSON", command=self.load_json).grid(row=3, column=1, padx=5, pady=5, sticky="e")
        
        # Configurações gerais
        config_frame = ttk.Frame(root)
        config_frame.pack(pady=10)
        ttk.Label(config_frame, text="Grafana API Key (opcional):").pack(side="left", padx=5)
        self.grafana_key_entry = ttk.Entry(config_frame, width=40)
        self.grafana_key_entry.pack(side="left", padx=5)
        
        ttk.Label(config_frame, text="Ordem de clonagem:").pack(side="left", padx=5)
        self.order_var = tk.StringVar(value="roles,categories,channels")
        ttk.Combobox(
            config_frame, 
            textvariable=self.order_var, 
            values=["roles,categories,channels", "categories,channels,roles", "channels,roles,categories"],
            state="readonly"
        ).pack(side="left", padx=5)
        
        ttk.Label(config_frame, text="Nível de logs:").pack(side="left", padx=5)
        self.log_var = tk.StringVar(value="normal")
        ttk.Combobox(
            config_frame, 
            textvariable=self.log_var, 
            values=["minimal", "normal", "detailed"],
            state="readonly"
        ).pack(side="left", padx=5)
        
        # Barra de progresso
        self.progress = ttk.Progressbar(root, length=400, mode="indeterminate")
        self.progress.pack(pady=10)
        
        # Botão de iniciar
        ttk.Button(root, text="Iniciar Clonagem/Restauração", command=self.start_clone).pack(pady=10)
        
        # Status
        self.status_label = ttk.Label(root, text="Pronto para clonar ou restaurar!", foreground="#ffffff", background="#2c2f33")
        self.status_label.pack(pady=5)
        
        # Inicializar modo Manual
        self.toggle_mode()
    
    def toggle_mode(self):
        mode = self.mode_var.get()
        if mode == "Bot":
            self.bot_frame.pack(fill="both")
            self.manual_frame.pack_forget()
        else:
            self.manual_frame.pack(fill="both")
            self.bot_frame.pack_forget()
            self.update_category_combo()
    
    def add_category(self):
        name = tk.simpledialog.askstring("Categoria", "Nome da categoria:", parent=self.root)
        if name:
            self.categories.append({"name": name, "position": len(self.categories)})
            self.category_listbox.insert(tk.END, name)
            self.update_category_combo()
    
    def add_channel(self):
        name = self.channel_name_entry.get()
        type_ = self.channel_type_var.get()
        category = self.channel_category_var.get() or None
        topic = self.channel_topic_entry.get() if type_ in ["text", "announcement"] else ""
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
    
    def load_json(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            self.json_entry.delete(0, tk.END)
            self.json_entry.insert(0, file_path)
    
    def start_clone(self):
        mode = self.mode_var.get()
        grafana_key = self.grafana_key_entry.get()
        order = self.order_var.get()
        log_level = self.log_var.get()
        
        config = {"order": order, "log_level": log_level}
        
        if mode == "Bot":
            token = self.token_entry.get()
            source = self.source_entry.get()
            dest = self.dest_entry.get()
            if not all([token, source, dest]):
                messagebox.showerror("Erro", "Preencha todos os campos obrigatórios!")
                return
        else:
            token = self.manual_token_entry.get()
            dest = self.manual_dest_entry.get()
            json_path = self.json_entry.get()
            if not all([token, dest]):
                messagebox.showerror("Erro", "Preencha bot token e ID do servidor destino!")
                return
            if json_path:
                try:
                    with open(json_path, 'r') as f:
                        config.update(json.load(f))
                except Exception as e:
                    messagebox.showerror("Erro", f"Falha ao carregar JSON: {str(e)}")
                    return
            elif self.categories or self.channels or self.roles:
                config.update({"categories": self.categories, "channels": self.channels, "roles": self.roles})
            else:
                messagebox.showerror("Erro", "Forneça um JSON ou adicione categorias/canais/cargos!")
                return
        
        self.progress.start()
        self.status_label.config(text="Clonando/Restaurando servidor... Aguarde!")
        self.root.update()
        
        try:
            if mode == "Bot":
                asyncio.run(main(token, source, dest, grafana_key, config))
            else:
                asyncio.run(main(token, None, dest, grafana_key, config))
            self.progress.stop()
            self.status_label.config(text="Clonagem/Restauração concluída!")
            messagebox.showinfo("Sucesso", "Processo concluído! Verifique output.json, chart.html e Grafana.")
        except Exception as e:
            self.progress.stop()
            self.status_label.config(text="Erro no processo!")
            messagebox.showerror("Erro", f"Falha: {str(e)}")

if __name__ == '__main__':
    root = tk.Tk()
    app = DisjorkDadosGUI(root)
    root.mainloop()