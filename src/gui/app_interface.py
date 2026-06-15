import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

try:
    from ..services.email_service import EmailService
except ImportError:
    from src.services.email_service import EmailService

class EmailSenderApp():
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Emails")
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
        # cabeçalho do programa
        header_frame = tk.Frame(self.root, bg="#f0f0f0")
        header_frame.pack(fill="x", padx=20, pady=10)

        lbl_title = tk.Label(header_frame, text="Novo Email", font=("Arial", 16, "bold"))
        lbl_title.pack()

        # tela (Frame) principal
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(fill="both", expand=True, padx=20, pady=5)

        # remetente
        sender_group = tk.LabelFrame(main_frame, text="Remetente - Sua conta", bg="#f0f0f0")
        sender_group.pack(fill="x", pady=5)

        tk.Label(sender_group, text="E-Mail: ", bg="#f0f0f0",).grid(row=0, column=0, sticky="w")
        self.entry_sender = tk.Entry(sender_group, width=50)
        self.entry_sender.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(sender_group, text="Senha: ", bg="#f0f0f0").grid(row=1, column=0, sticky="w")
        self.entry_password = tk.Entry(sender_group, width=50, show="*")
        self.entry_password.grid(row=1, column=1, padx=5, pady=2)

        # aba destinatário
        recipient_group = tk.LabelFrame(main_frame, text="Destinatário", bg="#f0f0f0", padx=10, pady=10)
        recipient_group.pack(fill="x", pady=5)

        tk.Label(recipient_group, text='para: ', bg="#f0f0f0").grid(row=0, column=0, sticky="w")
        self.entry_to = tk.Entry(recipient_group, width=50)
        self.entry_to.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(recipient_group, text="CC (Com Cópia): ", bg="#f0f0f0").grid(row=1, column=0, sticky="w")
        self.entry_cc = tk.Entry(recipient_group, width=50)
        self.entry_cc.grid(row=1, column=1, padx=5, pady=2)

        # Email - Mensagem 
        content_group = tk.LabelFrame(main_frame, text="Mensagem", bg="#f0f0f0", padx=10, pady=10)
        content_group.pack(fill="x", pady=5)

        tk.Label(content_group, text="Assunto", bg="#f0f0f0").grid(row=0, column=0, sticky="nw")
        self.entry_subject = tk.Entry(content_group, width=50)
        self.entry_subject.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(content_group, text="Corpo do Email: ", bg="#f0f0f0").grid(row=1, column=0, sticky="nw")
        self.text_body = tk.Text(content_group, width=50, height=8)
        self.text_body.grid(row=1, column=1, padx=5, pady=2)

        # anexos de arquivos 
        attach_group = tk.LabelFrame(main_frame, text="Anexos", bg="#f0f0f0", padx=10, pady=10)
        attach_group.pack(fill="x", pady=5)

        self.lbl_file = tk.Label(attach_group, text="Nenhum Arquivo Selecionado", fg="gray", width=40, anchor="w")
        self.lbl_file.grid(row=0, column=0, padx=5)

        btn_attach = ttk.Button(attach_group, text="Procurar Arquivo", command=self.select_file)
        btn_attach.grid(row=0, column=1, padx=5)

        btn_send = tk.Button(self.root, text="Enviar Email", command=self.handle_send, 
                             bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), height=2)
        btn_send.pack(fill="x", padx=20, pady=20)

    def select_file(self):
        self.file_path = filedialog.askopenfilename(
            title="selecione o arquivo",
            filetypes=[("Todos os arquivos", "*.*")]
        )
        if self.file_path:
            filename = os.path.basename(self.file_path)
            self.lbl_file.config(text=filename, fg="black")
    
    # modulo de coleta de dados e envio
    def handle_send(self):
        sender = self.entry_sender.get().strip()
        password = self.entry_password.get().strip()
        recipient = self.entry_to.get().strip()
        subject = self.entry_subject.get().strip()
        body = self.text_body.get("1.0", tk.END).strip()
        cc = self.entry_cc.get().strip()

        if not sender or not password or not recipient or not subject:
            messagebox.showerror("ERRO", "Preencha os campos obrigatórios")
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
            messagebox.showinfo("Email Enviado com Sucesso")
            self._clear_fields()

        except Exception as e:
            messagebox.showerror("Erro ao enviar email", f"{e}")
        
    def _clear_fields(self):
        self.entry_to.delete(0, tk.END)
        self.entry_subject.delete(0, tk.END)
        self.text_body.delete("1.0", tk.END)
        self.lbl_file.config(text="Nenhum arquivo selecionado", fg="gray")
        self.file_path = None
