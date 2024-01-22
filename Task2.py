import os
import time
import inspect

def logger(*paths):
    def __logger(old_function):
        def new_function(*args, **kwargs):
            # Записываем дату и время вызова функции
            for path in paths:
                with open(path, 'a') as log_file:
                    log_file.write(f'{time.strftime("%Y-%m-%d %H:%M:%S")} - Вызов функции {old_function.__name__}\n')

            # Записываем аргументы, переданные в функцию
            args_str = ', '.join(map(str, args))
            kwargs_str = ', '.join(f'{k}={v}' for k, v in kwargs.items())
            for path in paths:
                with open(path, 'a') as log_file:
                    log_file.write(f'Аргументы: {args_str}, {kwargs_str}\n')

            # Вызываем исходную функцию и записываем возвращаемое значение
            result = old_function(*args, **kwargs)
            for path in paths:
                with open(path, 'a') as log_file:
                    log_file.write(f'Возвращаемое значение: {result}\n\n')

            return result

        return new_function

    return __logger



def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger(path)
        def hello_world():
            return 'Hello World'

        @logger(path)
        def summator(a, b=0):
            return a + b

        @logger(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_2()
