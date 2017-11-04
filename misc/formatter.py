import re
import json

lines = []
for line in open('./gbdt_prediction_formatted.cpp'):
  line = line[:-1]

  line = line.replace(' {', ':')
  
  line = line.replace('} else', 'else')

  line = re.sub(r'^double', 'def', line)

  line = line.replace('const double *arr', 'arr')

  line = line.replace('const std::vector<uint32_t> cat_threshold = {};', '')
  
  line = line.replace('double ', '')
  
  line = line.replace('0.0f', '0.0')
  
  if 'const' in line:
    continue

  if 'namespace' in line:
    continue
  if len(line) >= 1:
    if line[-1] == '}':
      ...
    else:
      lines.append( line )

text = '\n'.join(lines)
text = re.sub(r'arr.*?\n.*?\[', 'arr[', text, flags=re.MULTILINE)
text = re.sub(r'=.*?\n\s{1,}?arr', '= arr', text, flags=re.MULTILINE)
text = re.sub(r'<=\s{1,}?\n\s{1,}?0', '<= 0', text, flags=re.MULTILINE)
text = re.sub(r'<=\s{1,}?\n\s{1,}?1', '<= 1', text, flags=re.MULTILINE)
print(text)
