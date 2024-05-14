from datetime import datetime
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Notification:
    def __init__(
        self, host, password, from_addr, to_addr, table, to_addr_cc="", to_addr_bcc=""
    ):
        self.host = host
        self.password = password
        self.author = from_addr
        self.recipients = to_addr
        self.table = table
        self.cc_recipients = to_addr_cc
        self.bcc_recipients = to_addr_bcc

    def current_date(self):
        return datetime.now().strftime("%B %d, %Y")

    def send_email(self, subject):
        regex = re.compile("\w+")
        name = regex.search(self.recipients).group()
        date = self.current_date()

        message = f"""
        <html>
        <body>
        Hi <b>{name}</b>, <br><br>
        The <b>{self.table}</b> table you are trying to access on <b>{date}</b> is empty. <br>
        If your dashboards or reporting views depend on this table, please notify your stakeholders.
        <br><br>
        <b>Note</b>: Operational team is working to fix the problem. For further info: Contact: Calin Iorga - +40 726 505 030.
        <br><br>
        Best regards,<br>
        Linux Monitoring System
        </body>
        </html>
        """

        msg = MIMEMultipart()
        msg["From"] = self.author
        msg["To"] = self.recipients
        msg["Cc"] = self.cc_recipients
        msg["Subject"] = subject

        msg.attach(MIMEText(message, "html"))

        server = smtplib.SMTP(self.host, 587)
        server.starttls()
        server.login(self.author, self.password)

        try:
            # Combine all recipient lists, and ensure to handle cases where CC or BCC might be empty
            all_recipients = [
                email
                for email in self.recipients.split(",")
                + self.cc_recipients.split(",")
                + self.bcc_recipients.split(",")
                if email
            ]
            server.sendmail(self.author, all_recipients, msg.as_string())
        finally:
            server.quit()
