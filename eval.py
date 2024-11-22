import json

TEDS_sum = 0
TEDS_struct_sum = 0
with open("your/path/output.jsonl", 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        TEDS_sum += data['TEDS_score']
        TEDS_struct_sum += data['TEDS_struct']
data_sum = 1500
print("{:.4f}".format(TEDS_sum / data_sum))
print("{:.4f}".format(TEDS_struct_sum / data_sum))
