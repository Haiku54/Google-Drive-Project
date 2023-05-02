from enum import Enum

class response_type(Enum):
    NOT_ENOUGH_PERMISSIONS = 1
    FILE_NOT_FOUND = 2

NOT_ENOUGH_PERMISSIONS_MESSAGE = """
היי :)
אנחנו מצטערים אבל עדיין אין תמיכה בסוג קובץ זה (ענייני הרשאות בהגדרת וכו)\nמבטיחים לעבוד על זה בקרוב ! 😊
"""

FILE_NOT_FOUND_MESSAGE ="""
היי :) 
נתקלנו בבעיה בהמרה של הקובץ. זה יכול להיות מ2 סיבות, או שהקובץ כבר לא קיים או שאין לנו אפשרות כרגע להעתיק סוג קובץ ספציפי זה, אולי בהמשך...
😊 בכל אופן מוזמנים לנסות עם קבצים אחרים
"""