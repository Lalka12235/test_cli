from app.log_analyze import exist_files,check_log,generate_report
import argparse



def main():
    parser = argparse.ArgumentParser(description='Анализ логов')
    parser.add_argument('log_files',nargs='+', help='Список лог файлов для анализа')
    parser.add_argument('--report',choices=['handlers'],default='handlers',help='Тип отчета')

    args = parser.parse_args()

    exist_files(args.log_files)

    log_data = check_log(args.log_files)

    
    generate_report(log_data)


if __name__ == '__main__':
    main()