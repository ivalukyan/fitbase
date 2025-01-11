import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, accuracy_score
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# Функция для прогнозирования результата
def predict_next_month(user_data):
    """
    Прогнозирует результат следующего месяца на основе данных прошлых месяцев.

    :param user_data: Список результатов пользователя за прошлые месяцы.
    :return: Прогноз результата на следующий месяц.
    """
    if len(user_data) < 2:
        raise ValueError("Для прогнозирования нужно минимум 2 значения.")

    # Подготовка данных
    months = np.arange(1, len(user_data) + 1).reshape(-1, 1)  # Месяцы (1, 2, 3, ...)
    results = np.array(user_data).reshape(-1, 1)  # Результаты пользователя

    # Разделение данных на обучающую и тестовую выборку
    X_train, X_test, y_train, y_test = train_test_split(months, results, test_size=0.2, random_state=100)

    # Создание и обучение модели линейной регрессии
    model = LinearRegression()
    model.fit(X_train, y_train)
    # model = RandomForestRegressor(random_state=100)
    # model.fit(X_train, y_train)

    # Прогноз результата для следующего месяца
    next_month = np.array([[len(user_data) + 1]])  # Следующий месяц
    prediction = model.predict(next_month)

    # Оценка модели
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"Среднеквадратическая ошибка модели: {mse:.2f}")
    r2_score = model.score(X_test, y_test)
    print(f"Коэффициент детерминации (R^2): {r2_score:.2f}")

    return prediction[0]

# Пример использования
if __name__ == "__main__":
    # Данные пользователя за прошлые месяцы (например, количество отжиманий)
    user_data = [15, 20, 22, 25, 30, 35, 28, 25, 30, 33, 33, 32, 38, 40, 41, 45]

    try:
        next_month_prediction = predict_next_month(user_data)
        print(f"Прогноз результата на следующий месяц: {next_month_prediction:.2f}")
    except ValueError as e:
        print(f"Ошибка: {e}")
