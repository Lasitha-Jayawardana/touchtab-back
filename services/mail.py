from mailjet_rest import Client



class EmailService():

    def __init__(self):
        # Todo: get stuff from env instead
        self.api_key = '77970e7f047333b97a14d77ef0705995'
        self.api_secret = 'e672239025374b114c2e35a5b506aed8'
        self.email_sender_email = 'coach@coachello.io'
        self.email_sender_name = 'Ivestwell'
        self.mailjet = Client(auth=(self.api_key, self.api_secret), version='v3.1')

    def send_email(self, receiver_name, receiver_email, subject, reference_id, text=None, html=None):
        data = {
          'Messages': [
            {
              "From": {
                "Email": self.email_sender_email,
                "Name": self.email_sender_name
              },
              "To": [
                {
                  "Email": receiver_email,
                  "Name": receiver_name
                }
              ],
              "Subject": subject,
              "TextPart": text,
              "HTMLPart": html,
              "CustomID": reference_id
            }
          ]
        }
        result = self.mailjet.send.create(data=data)
        return result

    def send_email_template(self, receiver_name, receiver_email, template_id=None, variables=None):
        data = {
            'Messages': [
                {
                    "From": {
                        "Email": self.email_sender_email,
                        "Name": self.email_sender_name
                    },
                    "To": [
                        {
                            "Email": receiver_email,
                            "Name": receiver_name
                        }
                    ],
                    "TemplateID": template_id,
                    "TemplateLanguage": True,
                    "Variables": variables,
                }
            ]
        }
        result = self.mailjet.send.create(data=data)
        return result
