import email.message
import smtplib
import os
from datetime import datetime
from app_backend.conf.settings import settings

def send_direct_email(to_email: str, subject: str, body: str, user_name: str = "Pengguna LARAS"):
    """
    Kirim email secara langsung (synchronous) menggunakan SMTP.
    Digunakan untuk pengetesan atau email kritikal.
    """
    # Load Template
    template_path = os.path.join(os.path.dirname(__file__), "templates", "email_base.html")
    logo_path = os.path.join(os.path.dirname(__file__), "templates", "logo.png")

    if os.path.exists(template_path):
        with open(template_path, "r") as f:
            html_content = f.read()
    else:
        html_content = f"<html><body><h2>{{ title }}</h2><p>{{ message }}</p></body></html>"

    # Replace Placeholders
    now = datetime.now()
    html_content = html_content.replace("{{ user_name }}", user_name)
    html_content = html_content.replace("{{ title }}", subject)
    html_content = html_content.replace("{{ message }}", body.replace("\n", "<br>"))
    html_content = html_content.replace("{{ year }}", str(now.year))
    html_content = html_content.replace("{{ timestamp }}", now.strftime("%d %b %Y, %H:%M"))

    msg = email.message.EmailMessage()
    msg["Subject"] = subject
    msg["From"] = f"{settings.smtp_from_name} <{settings.smtp_from_email}>"
    msg["To"] = to_email

    msg.set_content(body)  # Plain text version
    msg.add_alternative(html_content, subtype="html")

    # Attach Logo as CID
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            logo_data = f.read()
            msg.get_payload()[1].add_related(
                logo_data,
                maintype="image",
                subtype="png",
                cid="logo"
            )

    try:
        if settings.smtp_port == 465:
            server = smtplib.SMTP_SSL(settings.smtp_host, settings.smtp_port)
        else:
            server = smtplib.SMTP(settings.smtp_host, settings.smtp_port)
            server.starttls()

        server.login(settings.smtp_user, settings.smtp_password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Gagal mengirim email: {e}")
        return False
