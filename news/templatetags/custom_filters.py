from django import template


register = template.Library()


# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter()
def censor(value):
   """
   value: значение, к которому нужно применить фильтр
   """
   # Возвращаемое функцией значение подставится в шаблон.
   return f'{value} Р'




# @register.filter()
# def censor(in_text):
#     if not isinstance(in_text, str):
#         raise ValueError('Можно применить только к стоке!') # проверим, строка ли. Если строка, то в ней уже поищем плохие слова
#
#     for word in bad_words:
#         if word in bad_words:
#             in_text = in_text.replace(word, f'{word[0]}{"*" * (len(word) - 1)}')
#             return in_text