import re
from rest_framework.exceptions import ValidationError


class LinkValidator:

    def __init__(self, field=None, fields=None):
        self.field = field
        self.fields = fields

    def __call__(self, value):
        pattern = r'(https?://(?!www\.youtube\.com)[\w.-]+(?:\.[\w.-]+)+(/[\w.-]*)*)'

        if self.field:
            user_data = dict(value).get(self.field)
            matches = re.findall(pattern, user_data)

        elif self.fields:
            user_data = [dict(value).get(field) for field in self.fields]
            for data in user_data:
                if data is not None:
                    matches = re.findall(pattern, data)

        if bool(matches):
            raise ValidationError('Ссылки на материалы можно прикреплять только с платформы YouTube!')
