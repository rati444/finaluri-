"""
საერთო არჩევანის სიები (dropdown-ებისთვის), რომ ერთ ადგილას იყოს
და forms.py-მაც და routes.py-მაც აქედან წამოიღოს, არ დამჭირდეს
ერთი და იგივეს რამდენჯერმე გამეორება.
"""

SUBJECTS = [
    "მათემატიკა",
    "ისტორია",
    "ფიზიკა",
    "ქართული",
    "ინგლისური",
    "ბიოლოგია",
    "ქიმია",
    "გეოგრაფია",
]

SEMESTERS = [
    "სემესტრი 1",
    "სემესტრი 2",
]

RESOURCE_TYPES = [
    "კონსპექტი",
    "დავალება",
    "პრეზენტაცია",
    "ტესტი",
]

ROLES = [
    "student",
    "teacher",
    "admin",
]

SUBJECT_CHOICES = [(s, s) for s in SUBJECTS]
SEMESTER_CHOICES = [(s, s) for s in SEMESTERS]
RESOURCE_TYPE_CHOICES = [(t, t) for t in RESOURCE_TYPES]
