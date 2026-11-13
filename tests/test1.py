from datetime import date

import src.object_catalog as oc

s1 = oc.Auditorium(
    uid="123",
    name="Name",
    category="category",
    date="01.07.2008",
    number=101,
    size="large"
)
print(s1)