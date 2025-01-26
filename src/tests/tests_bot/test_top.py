import os
import sys
import pytest

from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from service.bot_service import sorting_count_up


class TestSortingCountUp:

    # Sort list of tuples/lists in ascending order based on first element
    @pytest.mark.asyncio
    async def test_sort_tuples_by_first_element(self):
        # Arrange
        input_list = [(3, "c"), (1, "a"), (2, "b")]
        expected = [(1, "a"), (2, "b"), (3, "c")]

        # Act
        result = await sorting_count_up(input_list)

        # Assert
        assert result == expected

    # Handle empty list input
    @pytest.mark.asyncio
    async def test_sort_empty_list(self):
        # Arrange
        input_list = []
        expected = []

        # Act
        result = await sorting_count_up(input_list)

        # Assert
        assert result == expected

    @pytest.mark.asyncio
    async def test_sort_tuples_time_control(self):
        array = []  # Инициализация пустого массива

        with open('D:/Code/fitbase/src/tests/tests_bot/large_input_list.txt', 'r') as file:
            for line in file:
                # Удаляем символы перевода строки и пробелы
                line = line.strip()
                if line:
                    # Преобразуем строку в кортеж (eval используется для преобразования строки в Python-объект)
                    try:
                        data = eval(line)
                        if isinstance(data, tuple):
                            array.append(data)
                        else:
                            print(f"Пропущена строка, так как она не является кортежем: {line}")
                    except Exception as e:
                        print(f"Ошибка при обработке строки '{line}': {e}")

        start = datetime.now()
        result = await sorting_count_up(array)
        print(f"Количество нормативов: {len(result)}")
        end = datetime.now()

        assert end - start < timedelta(seconds=1.5)
