import sys

section_name = ' '.join(sys.argv[1:])

with open('README.md', 'r') as readme_file:
    lines = readme_file.readlines()
    toc_start_idx = toc_end_idx = lines.index('### TOC\n')
    for i in range(toc_start_idx + 1, len(lines)):
        line = lines[i]
        if line.startswith('#'):
            toc_end_idx = i
            break
    lines.insert(toc_end_idx, '[' + section_name + '](#' + '-'.join(section_name.split(' ')).lower() + ')')
    lines.insert(toc_end_idx + 1, '\n\n')

    lines.append('\n### ' + section_name)
    lines.append('\n[Top](#TOC)\n')
    lines.append('\n**Example Request:**\n')
    lines.append('```xml\n```\n')
    lines.append('\n**Example Response:**\n')
    lines.append('```xml\n```\n')
    lines.append('\n**Notes:**\n\n')

with open('README.md', 'w') as readme_file:
    readme_file.write(''.join(lines))
