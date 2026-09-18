import matplotlib.pyplot as plt

fig, ax = plt.subplots()

ax.bar(1, 67, label = 'Количество евреев после 2 мировой')

ax.bar(2, 1488, label = 'Количество чурок в Москве')

ax.legend()

plt.show()