import re

print(bool(re.match(r"^[^\x00]*$", "hello")))
print(bool(re.match(r"^[^\x00]*$", "hel\x00lo")))
