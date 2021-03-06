from mailtrail.backends.base import MailTrailBase
from django.core.mail.backends.console import EmailBackend as ConsoleEmailBackend


class EmailBackend(MailTrailBase, ConsoleEmailBackend):
    """
    Send email and print it to the console.

    REPLACES: django.core.mail.backends.console.EmailBackend
    """
    BACKEND = 'CONSOLE'

    def send_messages(self, email_messages):
        for message in email_messages:
            self.save_message(message)

        return super(EmailBackend, self).send_messages(email_messages)
