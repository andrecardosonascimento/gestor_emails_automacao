# Gestor de E-mails usando Python e Tkinter
esse aplicativo desktop está sendo desenvolvido em python usando a biblioteca gráfica **Tkinter** e o pacote **YagMail**, O objetivo desse projeto é automatizar o envio de emails, facilitando o envio de anexos de forma rápida, usando uma interface funcional e limpa.

## Funcionalidades:
* **Interface Interativa** Desenvolvida interamente com TKinter/TTK.
* **Envio Simplificado** usando uma integração direta com provedores de email usando 'yagmail'.
* **Suporte a anexos de arquivos** nativos direto do sistema operacional.
* **Cópia Opcional** para o envio de emails com copia(cc).
* **Segurança** no envio dos emails com ocultaçãi de caracteres no campo de senha/app password.

## Estrutura do Projeto 

```text
gestor_emails/
│
├── src/                        # Código-fonte principal
│   ├── main.py                 # Ponto de entrada do aplicativo
│   ├── gui/                    # Módulo da Interface Gráfica
│   │   └── app_interface.py
│   └── services/               # Módulo de Lógica de Negócio
│       └── email_service.py
│
├── requirements.txt            # Dependências do projeto
└── README.md                   # Manual de instruções
```
## Instruções para o envio do email - IMPORTANTE!

Se o email for da google (gmail), é necessário criar uma senha de autenticação

Por que acontece?: O Gmail não aceita mais o método antigo de "permitir apps menos seguros" fazendo a conta exigir uma senha de aplicativo ou autenticação mais segura.

Como resolver?: Ative a verificação em duas etapas na sua conta Google.

Crie uma senha de app:

Acesse: https://myaccount.google.com/security
Em “Acesso ao Google”, clique em Senhas de app
Gere uma senha para “Email” / “Outro” e copie a senha gerada
Use essa senha no campo Senha do seu programa em vez da sua senha normal do Gmail.