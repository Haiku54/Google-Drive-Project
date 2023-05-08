from enum import Enum

class response_type(Enum):
    NOT_ENOUGH_PERMISSIONS = 1
    FILE_NOT_FOUND = 2
    FOLDER_EXISTS = 3
    

class InsufficientSpaceException(Exception):
    pass


NOT_ENOUGH_PERMISSIONS_MESSAGE = """
היי :)
אנחנו מצטערים אבל עדיין אין תמיכה בסוג קובץ זה (ענייני הרשאות בהגדרת וכו)\nמבטיחים לעבוד על זה בקרוב ! 😊
"""

FILE_NOT_FOUND_MESSAGE ="""
היי :) 
נתקלנו בבעיה בהמרה של הקובץ. זה יכול להיות מ2 סיבות, או שהקובץ כבר לא קיים או שאין לנו אפשרות כרגע להעתיק סוג קובץ ספציפי זה, אולי בהמשך...
😊 בכל אופן מוזמנים לנסות עם קבצים אחרים
"""

FOLDER_EXISTS_MESSAGE = """
היי :)
קיבלנו קישור לתיקייה, בגלל שכרגע אנחנו עובדים רק עם קישורים לקבצים, מצורף פה כל רשימת הקבצים בתיקייה ששלחת. מוזמן לשלוח את הקישור הרלוונטי עבורך.
שים לב: אם בתיקייה היו תיקיות נוספות, קיבלת גם קישורים לאותם תיקיות. כמובן שגם אותם ניתן לשלוח ולקבל את הקבצים ו.או תיקיות נוספות
😊
"""