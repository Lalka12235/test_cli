import os


def exist_files(files: list[str]):
    for file in files:
        if not os.path.isfile(file):
            raise FileNotFoundError(f'Файл не найден: {file}')
    
    return True
        

def check_log(file_paths: list[str]):
    log_data = {}

    for file_path in file_paths:
        with open(file_path, encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) < 5:
                    continue

                level = parts[2]
                logger = parts[3]

                if logger != 'django.request:':
                    continue

                router = next((word for word in parts if word.startswith('/')), None)
                if not router:
                    continue

                if router not in log_data:
                    log_data[router] = {'DEBUG': 0, 'INFO': 0, 'WARNING': 0, 'ERROR': 0, 'CRITICAL': 0}

                if level in log_data[router]:
                    log_data[router][level] += 1

    return log_data



def generate_report(data: dict): 
    total_requests = 0
    debug = info = warning = error = critical = 0

    print(f"{'HANDLER':<25}{'DEBUG':<8}{'INFO':<8}{'WARNING':<8}{'ERROR':<8}{'CRITICAL':<8}")

    for handler, levels in sorted(data.items()):
        print(f"{handler:<25}{levels['DEBUG']:<8}{levels['INFO']:<8}{levels['WARNING']:<8}{levels['ERROR']:<8}{levels['CRITICAL']:<8}")

        debug += levels['DEBUG']
        info += levels['INFO']
        warning += levels['WARNING']
        error += levels['ERROR']
        critical += levels['CRITICAL']

        total_requests += sum(levels.values())
    print(f'{'':<25}{debug:<8}{info:<8}{warning:<8}{error:<8}{critical:<8}')
    
    print(f"\nTotal requests: {total_requests}")