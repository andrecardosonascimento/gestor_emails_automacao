import yagmail

class EmailService:
    @staticmethod
    def send(sender, password, recipient, subject, body, cc=None, file_path=None):
        # iniciando o yagmail
        yag = yagmail.SMTP(user=sender, password=password)

        contents = [body]
        if file_path:
            contents.append(file_path)

            #comando para disparar o email
            yag.send(
                to=recipient,
                cc=cc if cc else None,
                subject=subject,
                contents=contents
            )