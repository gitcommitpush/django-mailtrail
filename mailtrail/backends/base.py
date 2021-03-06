from mailtrail.models import Email, get_recipient_model, get_recipient_model_attribute


class MailTrailBase:
    # Used to help identify which backend was used to send emails
    BACKEND = None

    BLANK = ''

    def _get_content(self, msg, content_type, fallback=None):
        payload = fallback

        for part in msg.walk():
            if part.get_content_type() == content_type:
                # Message has this content_type, return it
                payload = part.get_payload()

        return payload

    def save_message(self, message):
        """
        Save a sent message in the database
        """
        Recipient = get_recipient_model()

        # Uses email library to parse messages
        payload = message.message()

        plaintext = self._get_content(payload, 'text/plain', fallback='')
        html = self._get_content(payload, 'text/html')

        email = Email.objects.create(
            subject=message.subject,
            payload=message.message(),
            plaintext_message=plaintext,
            html_message=html,
            from_email=message.from_email,
            backend=self.BACKEND
        )

        for recipient_email in message.recipients():
            # Create recipients if they do not exist
            data = {
                get_recipient_model_attribute(): recipient_email
            }

            # Key 0 is the recipient object, key 1 is irrelevant
            recipient = Recipient.objects.get_or_create(**data)[0]
            email.recipients.add(recipient)
