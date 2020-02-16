import re

redaction = '/* REDACTED */'

with open('README.md', 'r') as readme_file:
    readme = readme_file.read()
    readme = re.sub(
        r'<userID>((?!EdupointDistrictInfo).+)<\/userID>',
        '<userID>' + redaction + '</userID>', readme)
    readme = re.sub(
        r'<password>((?!Edup01nt).+)</password>',
        '<password>' + redaction + '</password>', readme
    )
    readme = re.sub(r'Cookie: (.+)', 'Cookie: ' + redaction, readme)
    readme = re.sub(r'Set-Cookie: (.+)', 'Set-Cookie: ' + redaction, readme)

with open('README.md', 'w') as readme_file:
    readme_file.write(readme)
