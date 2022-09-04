from dataclasses import dataclass
from typing import Dict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Вывод сообщения о результатах тренировки."""

        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration:.3f} ч.; '
            f'Дистанция: {self.distance:.3f} км; '
            f'Ср. скорость: {self.speed:.3f} км/ч; '
            f'Потрачено ккал: {self.calories:.3f}.'
        )


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_H: int = 60

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float
    ) -> None:

        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.get_distance()) / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""
    def get_spent_calories(self) -> float:
        R_COEFF_CALORIE_1: float = 18
        R_COEFF_CALORIE_2: float = 20
        self.spent_calories = (
            (R_COEFF_CALORIE_1
             * self.get_mean_speed()
             - R_COEFF_CALORIE_2)
            * self.weight
            / self.M_IN_KM
            * self.MIN_IN_H
            * self.duration
        )
        return self.spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        height: float
    ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        SP_COEFF_CALORIE_1: float = 0.035
        SP_COEFF_CALORIE_2: int = 2
        SP_COEFF_CALORIE_3: float = 0.029
        self.spent_calories = (
            (SP_COEFF_CALORIE_1
             * self.weight
             + (self.get_mean_speed()**SP_COEFF_CALORIE_2
                // self.height)
             * SP_COEFF_CALORIE_3
             * self.weight)
            * self.duration
            * self.MIN_IN_H
        )
        return self.spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: float,
        count_pool: float
    ) -> None:

        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        self.mean_speed = (
            self.length_pool
            * self.count_pool
            / self.M_IN_KM
            / self.duration
        )
        return self.mean_speed

    def get_spent_calories(self) -> float:
        SW_COEFF_CALORIE_1: float = 1.1
        SW_COEFF_CALORIE_2: int = 2
        self.spent_calories = (
            (self.get_mean_speed()
             + SW_COEFF_CALORIE_1)
            * SW_COEFF_CALORIE_2
            * self.weight
        )
        return self.spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_type: Dict = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type in training_type:
        return training_type[workout_type](*data)
    else:
        raise ValueError(f'Вид тренировки не определен{workout_type}')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
