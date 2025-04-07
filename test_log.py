import pytest
from pathlib import Path
from app.log_analyze import exist_files, check_log, generate_report


# Тест для проверки существования файлов
def test_exist_files_existing_file():
    # Создаём временный файл
    file = Path("temp_file.txt")
    file.touch()
    
    # Проверяем, что файл существует
    exist_files([file])
    
    # Удаляем файл
    file.unlink()


def test_exist_files_non_existing_file():
    # Проверяем, что будет ошибка при отсутствии файла
    with pytest.raises(FileNotFoundError):
        exist_files([Path("non_existent_file.txt")])


# Тест для анализа логов
def test_check_log():
    log_lines = [
        "2025-04-07 11:42:23,000 DEBUG django.request:/api/v1/auth/login/",
        "2025-04-07 11:42:24,000 INFO django.request:/api/v1/orders/",
        "2025-04-07 11:42:25,000 ERROR django.request:/api/v1/orders/"
    ]
    log_file = Path("temp_log.txt")
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(log_lines))

    # Проверяем, что данные из лога правильно анализируются
    log_data = check_log([str(log_file)])  # передаем путь как строку
    expected_data = {
        '/api/v1/auth/login/': {'DEBUG': 1, 'INFO': 0, 'WARNING': 0, 'ERROR': 0, 'CRITICAL': 0},
        '/api/v1/orders/': {'DEBUG': 0, 'INFO': 1, 'WARNING': 0, 'ERROR': 1, 'CRITICAL': 0}
    }

    assert log_data == expected_data

    log_file.unlink()  # удаляем файл после теста



# Тест для генерации отчета
def test_generate_report():
    log_data = {
        '/api/v1/auth/login/': {'DEBUG': 1, 'INFO': 0, 'WARNING': 0, 'ERROR': 0, 'CRITICAL': 0},
        '/api/v1/orders/': {'DEBUG': 0, 'INFO': 1, 'WARNING': 0, 'ERROR': 1, 'CRITICAL': 0}
    }

    # Проверяем, что отчет генерируется без ошибок
    report = generate_report(log_data)
    
    # Проверка на наличие ключевых данных в отчете
    assert '/api/v1/auth/login/' in report
    assert '/api/v1/orders/' in report
    assert 'DEBUG' in report
    assert 'INFO' in report
    assert 'ERROR' in report
    assert 'Total requests' in report

