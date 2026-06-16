import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from src.services.email_service import EmailService

# Adicionar novas funções ao sistema na proxima versão 1.2


class EmailSenderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Emails - Python & Tkinter")
        self.root.geometry("600x650")
        self.root.configure(bg="#f0f0f0")

        self.file_path = None
        self._setup_styles()
        self._create_widgets()

    def _setup_styles(self):
        style = ttk.Style()
        style.configure("TLabel", font=("Arial", 10))
        style.configure("TButton", font=("Arial", 10, "bold"))
        style.configure("Header.TLabel", font=("Arial", 12, "bold"), background="#f0f0f0")

    def _create_widgets(self):
        # --- Cabeçalho ---
        header_frame = tk.Frame(self.root, bg="#f0f0f0")
        header_frame.pack(fill="x", padx=20, pady=10)
        
        lbl_title = tk.Label(header_frame, text="Novo Email", font=("Arial", 16, "bold"), bg="#f0f0f0", fg="#333")
        lbl_title.pack()

        # --- Frame Principal ---
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True, padx=20, pady=5)

        # 1. Remetente
        sender_group = tk.LabelFrame(main_frame, text="Remetente (Sua Conta)", bg="#f0f0f0", padx=10, pady=10)
        sender_group.pack(fill="x", pady=5)

        tk.Label(sender_group, text="E-mail:", bg="#f0f0f0").grid(row=0, column=0, sticky="w")
        self.entry_sender = tk.Entry(sender_group, width=50)
        self.entry_sender.grid(row=0, column=1, columnspan=2, padx=5, pady=2, sticky="w")

        tk.Label(sender_group, text="Senha:", bg="#f0f0f0").grid(row=1, column=0, sticky="w")
        self.entry_password = tk.Entry(sender_group, width=42, show="*")
        self.entry_password.grid(row=1, column=1, padx=5, pady=2, sticky="w")

        # Implementação do Botão de Mostrar/Ocultar Senha 
        self.var_show_pass = tk.BooleanVar(value=False)
        self.btn_show_pass = tk.Checkbutton(
            sender_group, 
            text="esconder senha", 
            variable=self.var_show_pass, 
            command=self.toggle_password,
            bg="#f0f0f0",
            activebackground="#f0f0f0",
            font=("Arial", 10)
        )
        self.btn_show_pass.grid(row=1, column=2, padx=2, pady=2, sticky="w")

        # 2. Destinatário
        recipient_group = tk.LabelFrame(main_frame, text="Destinatário", bg="#f0f0f0", padx=10, pady=10)
        recipient_group.pack(fill="x", pady=5)

        tk.Label(recipient_group, text="Para:", bg="#f0f0f0").grid(row=0, column=0, sticky="w")
        self.entry_to = tk.Entry(recipient_group, width=50)
        self.entry_to.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(recipient_group, text="CC (Opcional):", bg="#f0f0f0").grid(row=1, column=0, sticky="w")
        self.entry_cc = tk.Entry(recipient_group, width=50)
        self.entry_cc.grid(row=1, column=1, padx=5, pady=2)

        # 3. Mensagem
        content_group = tk.LabelFrame(main_frame, text="Mensagem", bg="#f0f0f0", padx=10, pady=10)
        content_group.pack(fill="x", pady=5)

        tk.Label(content_group, text="Assunto:", bg="#f0f0f0").grid(row=0, column=0, sticky="nw")
        self.entry_subject = tk.Entry(content_group, width=50)
        self.entry_subject.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(content_group, text="Corpo do Email:", bg="#f0f0f0").grid(row=1, column=0, sticky="nw")
        self.text_body = tk.Text(content_group, width=50, height=8)
        self.text_body.grid(row=1, column=1, padx=5, pady=2)

        # 4. Anexos
        attach_group = tk.LabelFrame(main_frame, text="4. Anexos", bg="#f0f0f0", padx=10, pady=10)
        attach_group.pack(fill="x", pady=5)

        self.lbl_file = tk.Label(attach_group, text="Nenhum arquivo selecionado", bg="#f0f0f0", fg="gray", width=40, anchor="w")
        self.lbl_file.grid(row=0, column=0, padx=5)

        btn_attach = ttk.Button(attach_group, text="Procurar Arquivo", command=self.select_file)
        btn_attach.grid(row=0, column=1, padx=5)

        # Botão Enviar
        btn_send = tk.Button(self.root, text="✉️ ENVIAR EMAIL", command=self.handle_send, 
                              bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), height=2)
        btn_send.pack(fill="x", padx=20, pady=20)

    def toggle_password(self):
        """Alterna a visibilidade da senha com base no estado do Checkbutton."""
        if self.var_show_pass.get():
            self.entry_password.config(show="")
        else:
            self.entry_password.config(show="*")

    def select_file(self):
        self.file_path = filedialog.askopenfilename(
            title="Selecione o arquivo",
            filetypes=[("Todos os arquivos", "*.*")]
        )
        if self.file_path:
            filename = os.path.basename(self.file_path)
            self.lbl_file.config(text=filename, fg="black")

    def handle_send(self):
        sender = self.entry_sender.get().strip()
        password = self.entry_password.get().strip()
        recipient = self.entry_to.get().strip()
        subject = self.entry_subject.get().strip()
        body = self.text_body.get("1.0", tk.END).strip()
        cc = self.entry_cc.get().strip()

        if not sender or not password or not recipient or not subject:
            messagebox.showerror("Erro", "Preencha todos os campos obrigatórios!")
            return

        try:
            EmailService.send(
                sender=sender,
                password=password,
                recipient=recipient,
                subject=subject,
                body=body,
                cc=cc,
                file_path=self.file_path
            )
            messagebox.showinfo("Sucesso", "Email enviado com sucesso!")
            self._clear_fields()
            
        except Exception as e:
            messagebox.showerror("Erro ao Enviar", f"Ocorreu um erro:\n{str(e)}")

    def _clear_fields(self):
        self.entry_to.delete(0, tk.END)
        self.entry_subject.delete(0, tk.END)
        self.text_body.delete('1.0', tk.END)
        self.lbl_file.config(text="Nenhum arquivo selecionado", fg="gray")
        self.file_path = None