import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import asyncio
import json
from main import main

class DisjorkDadosGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hygark's DisjorkDados")
        self.root.geometry("600x500")
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
            text="Clone servidores Discord!", 
            font=("Arial", 10, "italic"), 
            bg="#2c2f33", 
            fg="#ffffff"
        ).pack()

        # Formulário
        form_frame = ttk.Frame(root)
        form_frame.pack(padx=20, pady=10, fill="both")
        
        ttk.Label(form_frame, text="Bot Token:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.token_entry = ttk.Entry(form_frame, width=40, show="*")
        self.token_entry.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="ID do servidor origem:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.source_entry = ttk.Entry(form_frame, width=40)
        self.source_entry.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="ID do servidor destino:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.dest_entry = ttk.Entry(form_frame, width=40)
        self.dest_entry.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Grafana API Key (opcional):").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.grafana_key_entry = ttk.Entry(form_frame, width=40)
        self.grafana_key_entry.grid(row=3, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Ordem de clonagem:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.order_var = tk.StringVar(value="roles,categories,channels")
        ttk.Combobox(
            form_frame, 
            textvariable=self.order_var, 
            values=["roles,categories,channels", "categories,channels,roles", "channels,roles,categories"],
            state="readonly"
        ).grid(row=4, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Nível de logs:").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.log_var = tk.StringVar(value="normal")
        ttk.Combobox(
            form_frame, 
            textvariable=self.log_var, 
            values=["minimal", "normal", "detailed"],
            state="readonly"
        ).grid(row=5, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Configuração JSON (opcional):").grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.json_entry = ttk.Entry(form_frame, width=30)
        self.json_entry.grid(row=6, column=1, padx=5, pady=5, sticky="w")
        ttk.Button(form_frame, text="Carregar JSON", command=self.load_json).grid(row=6, column=1, padx=5, pady=5, sticky="e")
        
        # Barra de progresso
        self.progress = ttk.Progressbar(root, length=400, mode="indeterminate")
        self.progress.pack(pady=10)
        
        # Botão de iniciar
        ttk.Button(root, text="Iniciar Clonagem", command=self.start_clone).pack(pady=10)
        
        # Status
        self.status_label = ttk.Label(root, text="Pronto para clonar!", foreground="#ffffff", background="#2c2f33")
        self.status_label.pack(pady=5)
    
    def load_json(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            self.json_entry.delete(0, tk.END)
            self.json_entry.insert(0, file_path)
    
    def start_clone(self):
        token = self.token_entry.get()
        source = self.source_entry.get()
        dest = self.dest_entry.get()
        grafana_key = self.grafana_key_entry.get()
        order = self.order_var.get()
        log_level = self.log_var.get()
        json_path = self.json_entry.get()
        
        if not all([token, source, dest]):
            messagebox.showerror("Erro", "Preencha todos os campos obrigatórios!")
            return
        
        self.progress.start()
        self.status_label.config(text="Clonando servidor... Aguarde!")
        self.root.update()
        
        try:
            config = {"order": order, "log_level": log_level}
            if json_path:
                with open(json_path, 'r') as f:
                    config.update(json.load(f))
            asyncio.run(main(token, source, dest, grafana_key, config))
            self.progress.stop()
            self.status_label.config(text="Clonagem concluída!")
            messagebox.showinfo("Sucesso", "Clonagem concluída! Verifique output.json, chart.html e Grafana.")
        except Exception as e:
            self.progress.stop()
            self.status_label.config(text="Erro na clonagem!")
            messagebox.showerror("Erro", f"Falha na clonagem: {str(e)}")

if __name__ == '__main__':
    root = tk.Tk()
    app = DisjorkDadosGUI(root)
    root.mainloop()