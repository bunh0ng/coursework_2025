from datetime import datetime
date = str(input())
import re 
pattern = r"^\d{2}\.\d{2}\.\d{4}$"

if re.match(pattern, date):
    print('ok')
else:
    print('no match')

# pattern = r'^\d{2}\.\d{2}\.\d{4}$'
# text = "12.05.2024"

# if re.match(pattern, text):
#     print("Строка соответствует формату")
# else:
#     print("Нет соответствия")
