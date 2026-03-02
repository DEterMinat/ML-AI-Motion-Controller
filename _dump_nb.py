import json

nb = json.load(open('training/train_temporal.ipynb', encoding='utf-8'))
for i, c in enumerate(nb['cells']):
    print(f"=== CELL {i} [{c['cell_type']}] ===")
    print(''.join(c['source']))
    print()
