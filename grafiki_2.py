import numpy as np
import matplotlib.pyplot as plt

# Генерация двух наборов случайных данных
x = np.random.rand(100)
y = np.random.rand(100)

# Построение диаграммы рассеяния
plt.scatter(x, y, color='blue', alpha=0.7)
plt.title('Диаграмма рассеяния случайных данных')
plt.xlabel('X значения')
plt.ylabel('Y значения')
plt.grid(True)
plt.show()
