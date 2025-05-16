import random
import math
from typing import List, Dict, Tuple, Optional

class DataProcessor:
    def __init__(self, data: List[int]):
        self.data = data
        self._processed = False
        self._results = None
    
    def process_data(self) -> None:
        """Обрабатывает данные, выполняя различные операции"""
        if not self.data:
            raise ValueError("Данные не могут быть пустыми")
        
        temp_results = []
        for num in self.data:
            # Первая операция
            if num % 2 == 0:
                res = num ** 2
            else:
                res = math.sqrt(abs(num))
            
            # Вторая операция
            if res > 100:
                res = res / 10
            elif res < 1:
                res = res * 10
            
            temp_results.append(res)
        
        self._results = temp_results
        self._processed = True
    
    def get_results(self) -> List[float]:
        if not self._processed:
            self.process_data()
        return self._results
    
    def calculate_stats(self) -> Dict[str, float]:
        if not self._processed:
            self.process_data()
        
        stats = {
            'mean': sum(self._results) / len(self._results),
            'max': max(self._results),
            'min': min(self._results),
            'std_dev': self._calculate_std_dev()
        }
        return stats
    
    def _calculate_std_dev(self) -> float:
        mean = sum(self._results) / len(self._results)
        variance = sum((x - mean) ** 2 for x in self._results) / len(self._results)
        return math.sqrt(variance)

class DataGenerator:
    @staticmethod
    def generate_random_data(size: int = 100) -> List[int]:
        return [random.randint(-50, 50) for _ in range(size)]
    
    @staticmethod
    def generate_fibonacci_sequence(length: int) -> List[int]:
        if length <= 0:
            return []
        elif length == 1:
            return [0]
        
        sequence = [0, 1]
        while len(sequence) < length:
            sequence.append(sequence[-1] + sequence[-2])
        return sequence[:length]

class DataAnalyzer:
    def __init__(self, processor: DataProcessor):
        self.processor = processor
    
    def find_outliers(self, threshold: float = 2.0) -> List[Tuple[int, float]]:
        results = self.processor.get_results()
        stats = self.processor.calculate_stats()
        mean = stats['mean']
        std_dev = stats['std_dev']
        
        outliers = []
        for idx, value in enumerate(results):
            if abs(value - mean) > threshold * std_dev:
                outliers.append((idx, value))
        return outliers
    
    def group_values(self) -> Dict[str, List[float]]:
        results = self.processor.get_results()
        groups = {
            'low': [],
            'medium': [],
            'high': []
        }
        
        for value in results:
            if value < 10:
                groups['low'].append(value)
            elif 10 <= value <= 50:
                groups['medium'].append(value)
            else:
                groups['high'].append(value)
        
        return groups

class ReportGenerator:
    @staticmethod
    def generate_text_report(analyzer: DataAnalyzer) -> str:
        stats = analyzer.processor.calculate_stats()
        outliers = analyzer.find_outliers()
        groups = analyzer.group_values()
        
        report = []
        report.append("=== Статистический отчет ===")
        report.append(f"Среднее значение: {stats['mean']:.2f}")
        report.append(f"Максимальное значение: {stats['max']:.2f}")
        report.append(f"Минимальное значение: {stats['min']:.2f}")
        report.append(f"Стандартное отклонение: {stats['std_dev']:.2f}")
        report.append("\n=== Выбросы ===")
        for idx, value in outliers:
            report.append(f"Индекс {idx}: {value:.2f}")
        report.append("\n=== Группировка значений ===")
        report.append(f"Низкие значения (кол-во): {len(groups['low'])}")
        report.append(f"Средние значения (кол-во): {len(groups['medium'])}")
        report.append(f"Высокие значения (кол-во): {len(groups['high'])}")
        
        return "\n".join(report)
    
    @staticmethod
    def save_report_to_file(report: str, filename: str) -> None:
        with open(filename, 'w') as f:
            f.write(report)

def example_usage():
    # Генерация данных
    data = DataGenerator.generate_random_data(150)
    
    # Обработка данных
    processor = DataProcessor(data)
    processor.process_data()
    
    # Анализ данных
    analyzer = DataAnalyzer(processor)
    
    # Генерация отчета
    report = ReportGenerator.generate_text_report(analyzer)
    print(report)
    
    # Сохранение отчета в файл
    ReportGenerator.save_report_to_file(report, "data_report.txt")

def complex_operation(x: int, y: int, z: Optional[int] = None) -> float:
    """Выполняет комплексную математическую операцию"""
    result = x * y
    if z is not None:
        if z == 0:
            raise ValueError("z не может быть нулем")
        result /= z
    
    if result > 0:
        result = math.log(result)
    else:
        result = math.log(abs(result) + 1)
    
    return result * math.pi

def validate_input(value: str) -> Tuple[bool, Optional[int]]:
    """Проверяет ввод пользователя"""
    try:
        num = int(value)
        if num < 0:
            return False, None
        return True, num
    except ValueError:
        return False, None

def process_user_input():
    """Обрабатывает ввод пользователя"""
    print("Введите положительное целое число:")
    user_input = input().strip()
    
    is_valid, number = validate_input(user_input)
    if not is_valid:
        print("Ошибка: введено недопустимое значение")
        return
    
    print(f"Вы ввели: {number}")
    print(f"Результат комплексной операции: {complex_operation(number, number + 5, number - 3):.2f}")

if __name__ == "__main__":
    print("Запуск примера использования...")
    example_usage()
    
    print("\nЗапуск обработки пользовательского ввода...")
    process_user_input()