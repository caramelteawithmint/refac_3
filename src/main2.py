import random
import math
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod

class DataTransformer:
    """Преобразует данные по заданным правилам"""
    @staticmethod
    def transform_even_number(num: int) -> float:
        return num ** 2
    
    @staticmethod
    def transform_odd_number(num: int) -> float:
        return math.sqrt(abs(num))
    
    @staticmethod
    def adjust_value_range(value: float) -> float:
        if value > 100:
            return value / 10
        if value < 1:
            return value * 10
        return value

class DataStatisticsCalculator:
    """Вычисляет статистические показатели данных"""
    @staticmethod
    def calculate_mean(values: List[float]) -> float:
        return sum(values) / len(values)
    
    @staticmethod
    def calculate_standard_deviation(values: List[float]) -> float:
        mean = DataStatisticsCalculator.calculate_mean(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return math.sqrt(variance)
    
    @staticmethod
    def calculate_basic_stats(values: List[float]) -> Dict[str, float]:
        return {
            'mean': DataStatisticsCalculator.calculate_mean(values),
            'max': max(values),
            'min': min(values),
            'std_dev': DataStatisticsCalculator.calculate_standard_deviation(values)
        }

@dataclass
class ProcessedData:
    """Хранит результаты обработки данных"""
    values: List[float]
    is_processed: bool = False

class DataProcessor:
    def __init__(self, data: List[int]):
        self.raw_data = data
        self._results = ProcessedData([], False)
    
    def process_data(self) -> None:
        """Обрабатывает данные, выполняя различные операции"""
        if not self.raw_data:
            raise ValueError("Данные не могут быть пустыми")
        
        transformed_values = []
        for num in self.raw_data:
            transformed = (DataTransformer.transform_even_number(num) 
                          if num % 2 == 0 
                          else DataTransformer.transform_odd_number(num))
            adjusted = DataTransformer.adjust_value_range(transformed)
            transformed_values.append(adjusted)
        
        self._results = ProcessedData(transformed_values, True)
    
    def get_results(self) -> List[float]:
        if not self._results.is_processed:
            self.process_data()
        return self._results.values
    
    def calculate_stats(self) -> Dict[str, float]:
        return DataStatisticsCalculator.calculate_basic_stats(self.get_results())

class DataGenerator:
    """Генерирует различные типы данных"""
    @staticmethod
    def generate_random_data(size: int = 100, min_val: int = -50, max_val: int = 50) -> List[int]:
        return [random.randint(min_val, max_val) for _ in range(size)]
    
    @staticmethod
    def generate_fibonacci_sequence(length: int) -> List[int]:
        if length <= 0:
            return []
        if length == 1:
            return [0]
        
        sequence = [0, 1]
        while len(sequence) < length:
            sequence.append(sequence[-1] + sequence[-2])
        return sequence[:length]

class DataAnalyzer:
    """Анализирует обработанные данные"""
    def __init__(self, processor: DataProcessor):
        self.processor = processor
    
    def find_outliers(self, threshold: float = 2.0) -> List[Tuple[int, float]]:
        results = self.processor.get_results()
        stats = self.processor.calculate_stats()
        mean = stats['mean']
        std_dev = stats['std_dev']
        
        return [
            (idx, value) 
            for idx, value in enumerate(results) 
            if abs(value - mean) > threshold * std_dev
        ]
    
    def group_values_by_ranges(self) -> Dict[str, List[float]]:
        results = self.processor.get_results()
        return {
            'low': [v for v in results if v < 10],
            'medium': [v for v in results if 10 <= v <= 50],
            'high': [v for v in results if v > 50]
        }

class ReportGenerator:
    """Генерирует отчеты по анализу данных"""
    @staticmethod
    def generate_text_report(analyzer: DataAnalyzer) -> str:
        stats = analyzer.processor.calculate_stats()
        outliers = analyzer.find_outliers()
        groups = analyzer.group_values_by_ranges()
        
        report_lines = [
            "=== Статистический отчет ===",
            f"Среднее значение: {stats['mean']:.2f}",
            f"Максимальное значение: {stats['max']:.2f}",
            f"Минимальное значение: {stats['min']:.2f}",
            f"Стандартное отклонение: {stats['std_dev']:.2f}",
            "\n=== Выбросы ===",
            *[f"Индекс {idx}: {value:.2f}" for idx, value in outliers],
            "\n=== Группировка значений ===",
            f"Низкие значения (кол-во): {len(groups['low'])}",
            f"Средние значения (кол-во): {len(groups['medium'])}",
            f"Высокие значения (кол-во): {len(groups['high'])}"
        ]
        
        return "\n".join(report_lines)
    
    @staticmethod
    def save_report_to_file(report: str, filename: str) -> None:
        with open(filename, 'w') as file:
            file.write(report)

class MathOperations:
    """Выполняет сложные математические операции"""
    @staticmethod
    def perform_complex_calculation(x: int, y: int, z: Optional[int] = None) -> float:
        """Выполняет комплексную математическую операцию"""
        result = x * y
        if z is not None:
            if z == 0:
                raise ValueError("Делитель не может быть нулем")
            result /= z
        
        log_base = result if result > 0 else abs(result) + 1
        return math.log(log_base) * math.pi

class InputValidator:
    """Проверяет и обрабатывает пользовательский ввод"""
    @staticmethod
    def validate_positive_integer(value: str) -> Tuple[bool, Optional[int]]:
        """Проверяет, что введено положительное целое число"""
        try:
            num = int(value)
            return (num >= 0), num if num >= 0 else None
        except ValueError:
            return False, None
    
    @staticmethod
    def process_user_input():
        """Обрабатывает ввод пользователя"""
        print("Введите положительное целое число:")
        user_input = input().strip()
        
        is_valid, number = InputValidator.validate_positive_integer(user_input)
        if not is_valid:
            print("Ошибка: введено недопустимое значение")
            return
        
        print(f"Вы ввели: {number}")
        result = MathOperations.perform_complex_calculation(number, number + 5, number - 3)
        print(f"Результат комплексной операции: {result:.2f}")

def main():
    print("Запуск примера использования...")
    
    # Генерация и обработка данных
    data = DataGenerator.generate_random_data(150)
    processor = DataProcessor(data)
    analyzer = DataAnalyzer(processor)
    
    # Генерация и сохранение отчета
    report = ReportGenerator.generate_text_report(analyzer)
    print(report)
    ReportGenerator.save_report_to_file(report, "data_report.txt")
    
    print("\nЗапуск обработки пользовательского ввода...")
    InputValidator.process_user_input()

if __name__ == "__main__":
    main()