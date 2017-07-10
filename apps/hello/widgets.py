from django import forms


class DatePickerWidget(forms.DateInput):
    class Media:
        css = {
            'all': (
                "https://code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css",
                )
        }
        js = (
            "https://code.jquery.com/ui/1.12.1/jquery-ui.js",
        )

    def __init__(self, attrs=None):
        if attrs is None:
            attrs = {
                        "dateFormat": 'yy-mm-dd',
                        "changeYear": True,
                        "yearRange": '-70:'
                    }
        self.attrs = attrs
        super(DatePickerWidget, self).__init__(attrs=attrs)

    def render(self, name, value, attrs):
        rendered = super(DatePickerWidget, self).render(
            name,
            value,
            attrs=attrs
        )
        return rendered
