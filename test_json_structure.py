import json

def print_json_structure(data, indent=0):
    if isinstance(data, dict):
        for key, value in data.items():
            print(' ' * indent + f'- {key}: ', end='')
            if isinstance(value, (dict, list)):
                print()
                print_json_structure(value, indent + 2)
            else:
                print(f'{type(value).__name__}')
    elif isinstance(data, list):
        print(' ' * indent + '- []')
        if len(data) > 0:
            print_json_structure(data[0], indent + 2)

if __name__ == '__main__':
    file_path = 'data1/china.json'
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f'Structure of {file_path}:')
    print_json_structure(data)