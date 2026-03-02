from pathlib import Path
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from jinja2 import Environment, FileSystemLoader
from utils.settings import config
import os


BASE_DIR = Path(__file__).resolve().parent.parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"


env = Environment(loader=FileSystemLoader(TEMPLATES_DIR), autoescape=True)

# SMTP Connection Configuration
conf = ConnectionConfig(
    MAIL_USERNAME=config.MAIL_USERNAME,
    MAIL_PASSWORD=config.MAIL_PASSWORD,
    MAIL_FROM=config.MAIL_FROM,
    MAIL_SERVER=config.MAIL_SERVER,
    MAIL_PORT=config.MAIL_PORT,
    MAIL_STARTTLS=config.MAIL_STARTTLS,
    MAIL_SSL_TLS=config.MAIL_SSL_TLS,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

async def send_email(
    subject: str, 
    recipient_email: list, 
    template_name: str, 
    context: dict
):
    """
    Core utility to render an HTML template and send it via SMTP.
    Used by the EmailChannel in the notification system.
    """
    try:
       
        template = env.get_template(template_name)
        html_content = template.render(context)

 
        message = MessageSchema(
            subject=subject,
            recipients=recipient_email,
            body=html_content,
            subtype=MessageType.html
        )

     
        fm = FastMail(conf)
        await fm.send_message(message)
        
    except Exception as e:
   
        print(f"Failed to send email: {str(e)}")
        raise e