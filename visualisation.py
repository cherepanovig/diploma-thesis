import matplotlib.pyplot as plt


def read_execution_times(filename='execution_times.txt'):
    results = {
        'django': [],
        'sqlalchemy': [],
        'tortoise': []
    }

    try:
        with open(filename, 'r') as f:
            for line in f:
                framework, time_str = line.strip().split(': ')
                results[framework].append(float(time_str))
    except FileNotFoundError:
        print(f"File {filename} not found!")
        return None

    # Вычисляем среднее время для каждого фреймворка
    average_times = {
        framework: sum(times) / len(times) if times else 0
        for framework, times in results.items()
    }

    return average_times


def create_chart(output_path='visualisation.png'):
    # Читаем данные из файла
    results = read_execution_times()
    if not results:
        return

    # Создаем диаграмму
    frameworks = list(results.keys())
    execution_times = list(results.values())

    plt.figure(figsize=(10, 6))
    bars = plt.bar(frameworks, execution_times)

    plt.title('Сравнение времени выполнения тестов', fontsize=14)
    plt.xlabel('Фреймворк', fontsize=12)
    plt.ylabel('Среднее время выполнения (секунды)', fontsize=12)

    # Добавляем значения над столбцами
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2., height,
                 f'{height:.3f}s',
                 ha='center', va='bottom')

    plt.grid(True, axis='y', linestyle='--', alpha=0.7)

    # Разные цвета для столбцов
    colors = ['#2ecc71', '#3498db', '#e74c3c']
    for bar, color in zip(bars, colors):
        bar.set_color(color)

    plt.savefig(output_path)
    plt.close()


if __name__ == '__main__':
    create_chart()