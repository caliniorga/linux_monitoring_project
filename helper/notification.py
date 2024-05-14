from datetime import datetime
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Notification:
    def __init__(self, host: str, password: str, from_addr: str, to_addr: str, table: str, to_addr_cc: str = "", to_addr_bcc: str = ""):
        """
        Initializes the Notification class with email settings and table information.

        Parameters:
            host (str): The SMTP host.
            password (str): The SMTP password for the sender's email account.
            from_addr (str): The sender's email address.
            to_addr (str): The primary recipient's email address.
            table (str): The database table name related to the notification.
            to_addr_cc (str, optional): The CC recipients' email addresses, separated by commas.
            to_addr_bcc (str, optional): The BCC recipients' email addresses, separated by commas.
        """
        self.host = host
        self.password = password
        self.author = from_addr
        self.recipients = to_addr
        self.table = table
        self.cc_recipients = to_addr_cc
        self.bcc_recipients = to_addr_bcc
        self.date = datetime.now().strftime("%B %d, %Y")

    def current_date(self) -> str:
        """
        Returns the current date formatted as a string.

        Returns:
            str: The current date in 'Month day, Year' format.
        """
        return datetime.now().strftime("%B %d, %Y")

    def send_empty_table_email(self, subject: str):
        """
        Sends an email to notify about an empty table.

        Parameters:
            subject (str): The subject of the email.

        Returns:
            None
        """
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

    def send_error_prediction_email(self, subject: str, date: str):
        """
        Sends an email to notify about a spike in processor resources.

        Parameters:
            subject (str): The subject of the email.
            date (str): The date of the detected spike, formatted as 'Month day, Year'.

        Returns:
            None
        """
        regex = re.compile('\w+')
        name = regex.search(self.recipients).group()

        message = f"""
           <html>
           <body>
           Hi <b>{name}</b>, <br><br>
             A spike in processor resources has been detected in <b>{self.table}</b> table on <b>{date}</b>. <br><br>
             Please be vigilant as the system may experience lag, become unresponsive, or crash. Check the related systems and pass the information to DevOps.
             <hr>
             <br>
             <b>Reference Information</b>: System Performance Documentation.
             <br>
             <b>For Further Info, Contact</b>: Calin Iorga - +40 726 505 030.
             <br><br>
             Regards,<br>
             Linux Monitoring System
             </body>
             </html>
           """

        msg = MIMEMultipart("alternative")
        msg['From'] = self.author
        msg['To'] = self.recipients
        msg['Cc'] = self.cc_recipients
        msg['Subject'] = subject

        part = MIMEText(message, 'html')
        msg.attach(part)

        server = smtplib.SMTP(self.host, 587)
        server.starttls()
        server.login(self.author, self.password)

        try:
            all_recipients = [email.strip() for email in (self.recipients.split(",") + self.cc_recipients.split(",") + self.bcc_recipients.split(",") if email)]
            server.sendmail(self.author, all_recipients, msg.as_string())
        finally:
            server.quit()
