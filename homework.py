class InfoMessage:
    """Information message about the training."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """InfoMessage Class's method for displaying messages on the screen."""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Basic class for workout."""
    # adding class attributes
    M_IN_KM: float = 1000   # constant converts meters to kilometers
    LEN_STEP: float = 0.65  # constant converts distance from step to meters
    time_coeff: float = 60  # constant converts hours to minutes

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action = action      # number of performed actions
        self.duration = duration  # workout duration
        self.weight = weight      # user's weight

    def get_distance(self) -> float:
        """Get distance in kilometers."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Get the average speed of movement."""
        speed: float = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Get the number of spent calories."""
        # due to calories spending is unique for each workout
        # we don't do any actions in this method
        pass

    def show_training_info(self) -> InfoMessage:
        """Return an informational message about the completed workout."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Workout: running."""
    coeff_cal_1: float = 18  # basic coefficient for running
    coeff_cal_2: float = 20  # basic coefficient for running

    def get_spent_calories(self) -> float:
        """Counts and return calories for running workout"""
        calories = (((self.coeff_cal_1 * self.get_mean_speed() - self.coeff_cal_2)
                     * self.weight) / self.M_IN_KM * self.duration * self.time_coeff)
        return calories


class SportsWalking(Training):
    """Workout: sports walking."""
    coeff_cal_1: float = 0.035  # basic coefficient for sports walking
    coeff_cal_2: float = 0.029  # basic coefficient for sports walking

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)  # inheriting the properties of basic class
        self.height = height

    def get_spent_calories(self) -> float:
        """Counts and return calories for sports walking workout"""
        calories = (self.coeff_cal_1 * self.weight + (self.get_mean_speed()**2 // self.height)
                    * self.coeff_cal_2 * self.weight) * self.duration * self.time_coeff
        return calories


class Swimming(Training):
    """Workout: swimming."""
    coeff_cal_1: float = 1.1  # basic coefficient for sports swimming
    coeff_cal_2: float = 2    # basic coefficient for sports swimming
    LEN_STEP: float = 1.38    # distance for one stroke

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)  # inheriting the properties of basic class
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Get the average speed of swimming workout."""
        speed: float = self.length_pool * self.count_pool / self.M_IN_KM / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Counts and return calories for swimming workout."""
        calories = (self.get_mean_speed() + self.coeff_cal_1) * self.coeff_cal_2 * self.weight
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Read data from sensors."""
    workout_dict = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return workout_dict[workout_type](*data)



def main(training: Training) -> None:
    """Main function."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())
    pass


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', {9000, 1, 75, 180}),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
