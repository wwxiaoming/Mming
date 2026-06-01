import re
text = open('帝王战队资料/世界书条目v4/专属装置/01_榨精自行车.md', encoding='utf-8').read()
# Find ALL triple backticks
positions = []
for m in re.finditer(r'```', text):
    positions.append(m.start())
print(f'Found {len(positions)} triple-backticks at positions: {positions}')
# The pattern needs the last ``` to be the end of the file
print(f'\nLast 100 chars: {text[-100:]!r}')
print(f'\nLength: {len(text)}')

# Test simpler regex
code_block_pattern = re.compile(r'```yaml\n(.*?)\n```', re.DOTALL)
matches = list(code_block_pattern.finditer(text))
print(f'\nSimpler regex matches: {len(matches)}')
for m in matches:
    print(f'  Range: {m.start()}-{m.end()}')
    print(f'  Content (first 100): {m.group(1)[:100]!r}')
