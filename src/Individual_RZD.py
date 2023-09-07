"""Создание программы на объектно-ориентированном языке Python для железнодорожного вокзала"""
import pickle
import time
from datetime import datetime


class RzdDatabase:
    """Класс контейнер использующий сериализацию и для хранения основных сущностей, применяющий словарь"""

    def __init__(self):
        self.filename = 'rzd.pkl'
        self.database = {
            'workers': {},
            'train_timetables': {},
            'trains': {},
            'train_brigades': {},
            'ticket_sales_sheets': {}
        }
        self.index = 0
        try:
            self.open_database()
        except:
            self.save_database()

    def __iter__(self):
        for item in self.database:
            yield self.database[item]

    def next(self):
        if self.index == len(self.database):
            raise StopIteration
        self.index = self.index + 1
        return self.database[self.index]

    def prev(self):
        if self.index == 0:
            raise StopIteration
        self.index = self.index - 1
        return self.database[self.index]

    def open_database(self):
        with open(self.filename, 'rb') as f:
            self.database = pickle.load(f)

    def save_database(self):
        with open(self.filename, 'wb') as f:
            pickle.dump(self.database, f)

    def add_worker(self, surname, name, patronymic, year_of_birth, year_of_employment,
                   seniority, position, gender, address, city, phone):
        worker = WorkerRZD(surname, name, patronymic, year_of_birth, year_of_employment,
                           seniority, position, gender, address, city, phone)
        if worker.name in self.database["workers"]:
            while worker.name in self.database["workers"]:
                worker.name = worker.name + "1"
        self.database["workers"][worker.name] = worker
        self.save_database()
        return worker

    def delete_worker(self, name):
        del self.database["workers"][name]
        self.save_database()

    def get_worker_by_name(self, name):
        if name not in self.database["workers"]:
            return None
        return self.database["workers"][name]

    def change_worker(self, name):
        worker = self.get_worker_by_name(name)
        if not worker:
            raise ValueError('value does not exist')
        # choose = int(input("What changes?\n1.Name\n2.Seniority\nchoose: "))
        choose = 1
        if choose == 1:
            worker.name = input("New name: ")
            # меняем значение ключа на новое имя
            self.database["workers"][worker.name] = self.database["workers"][name]
            # удаляем старый ключ
            del self.database["workers"][name]
        elif choose == 2:
            worker.seniority = int(input("New seniority: "))
        else:
            raise ValueError('value does not exist')
        self.save_database()

    def change_worker_qt(self, name, new_name):
        worker = self.get_worker_by_name(name)
        if not worker:
            raise ValueError('value does not exist')
        worker.name = new_name
        # меняем значение ключа на новое имя
        self.database["workers"][worker.name] = self.database["workers"][name]
        # удаляем старый ключ
        del self.database["workers"][name]
        self.save_database()

    def add_train_timetable(self, date_of_departure, time_of_departure, place_of_departure,
                            date_of_arrival, time_of_arrival, place_of_arrival, route, ticket_price,
                            number, release_year=None, number_of_carriages=None, type_of_train=None):
        train_timetable = TrainTimetable(date_of_departure, time_of_departure, place_of_departure,
                                         date_of_arrival, time_of_arrival, place_of_arrival, route, ticket_price,
                                         number, release_year, number_of_carriages, type_of_train)
        if train_timetable.train.number in self.database["train_timetables"]:
            # если расписание с таким номером уже существует, то добавляем к нему .1
            train_timetable.train.number = str(train_timetable.train.number) + ".1"
        self.database["train_timetables"][train_timetable.train.number] = train_timetable
        if train_timetable.train.number not in self.database["trains"]:
            # если поезда с таким расписанием ещё нет в базе, то добавляем его
            self.database["trains"][train_timetable.train.number] = train_timetable.train
        self.save_database()
        return train_timetable, self.database["trains"][train_timetable.train.number]

    def delete_train_timetable(self, number):
        del self.database["train_timetables"][number]
        self.save_database()

    def get_train_timetable_by_number(self, number):
        if number not in self.database["train_timetables"]:
            return None
        return self.database["train_timetables"][number]

    def change_ticket_price(self, number):
        train_timetable = self.get_train_timetable_by_number(number)
        if not train_timetable:
            raise ValueError('value does not exist')
        train_timetable.ticket_price = int(input("New price: "))
        self.save_database()

    def change_ticket_price_qt(self, number, new_price):
        train_timetable = self.get_train_timetable_by_number(number)
        if not train_timetable:
            raise ValueError('value does not exist')
        train_timetable.ticket_price = int(new_price)
        self.save_database()

    def add_train(self, number, release_year, number_of_carriages, type_of_train):
        train = Train(number, release_year, number_of_carriages, type_of_train)
        if train.number in self.database["trains"]:
            # если поезд с таким номером уже существует, то добавляем к нему 1
            train.number = str(train.number) + ".1"
        self.database["trains"][train.number] = train
        self.save_database()
        return train

    def delete_train(self, number):
        del self.database["trains"][number]
        self.save_database()

    def get_train_by_number(self, number):
        if number not in self.database["trains"]:
            return None
        return self.database["trains"][number]

    def change_number_of_carriages(self, number):
        train = self.get_train_by_number(number)
        if not train:
            raise ValueError('value does not exist')
        new_value = int(input("New number of carriages: "))
        train.number_of_carriages = new_value
        # меняем значение ещё и в расписании
        try:
            train2 = self.get_train_timetable_by_number(number)
            train2.train.number_of_carriages = new_value
        except:
            pass
        self.save_database()

    def change_number_of_carriages_qt(self, number, new_number_of_carriages):
        train = self.get_train_by_number(number)
        if not train:
            raise ValueError('value does not exist')
        new_value = int(new_number_of_carriages)
        train.number_of_carriages = new_value
        # меняем значение ещё и в расписании
        if train.number in self.database["train_timetables"]:
            train2 = self.get_train_timetable_by_number(number)
            train2.train.number_of_carriages = new_value
        self.save_database()

    def add_train_brigade(self, brigade_number, surname, name, position,
                          number_of_train, release_year=None, number_of_carriages=None, type_of_train=None,
                          patronymic=None, year_of_birth=None, year_of_employment=None,
                          seniority=None, gender=None, address=None, city=None, phone=None):
        train_brigade = TrainBrigade(brigade_number, surname, name, position,
                                     number_of_train, release_year, number_of_carriages, type_of_train,
                                     patronymic, year_of_birth, year_of_employment,
                                     seniority, gender, address, city, phone)
        if train_brigade.brigade_number in self.database["train_brigades"]:
            # если бригада с таким номером уже существует, то добавляем к нему 1
            train_brigade.brigade_number = str(train_brigade.brigade_number) + "1"
        self.database["train_brigades"][train_brigade.brigade_number] = train_brigade
        if train_brigade.rzd_workers[0].name not in self.database["workers"]:
            # если работника с таким номером ещё нет в базе, то добавляем его
            self.database["workers"][train_brigade.rzd_workers[0].name] = train_brigade.rzd_workers[0]
        if train_brigade.train.number not in self.database["trains"]:
            # если поезда с таким расписанием ещё нет в базе, то добавляем его
            self.database["trains"][train_brigade.train.number] = train_brigade.train
        self.save_database()
        return train_brigade, self.database["workers"][train_brigade.rzd_workers[0].name], self.database["trains"][
            train_brigade.train.number]

    def delete_train_brigade(self, number):
        del self.database["train_brigades"][number]
        self.save_database()

    def get_train_brigade_by_number(self, number):
        if number not in self.database["train_brigades"]:
            if str(number) not in self.database["train_brigades"]:
                return None
            else:
                number = str(number)
        return self.database["train_brigades"][number]

    def change_brigade_number(self, number):
        number = int(number)
        train_brigade = self.get_train_brigade_by_number(number)
        if not train_brigade:
            raise ValueError('value does not exist')
        train_brigade.brigade_number = int(input("New number of brigade: "))
        # меняем значение ключа на новый номер
        self.database["train_brigades"][train_brigade.brigade_number] = self.database["train_brigades"][number]
        # удаляем старый ключ
        del self.database["train_brigades"][number]
        self.save_database()

    def change_brigade_number_qt(self, number, new_number):
        train_brigade = self.get_train_brigade_by_number(number)
        if not train_brigade:
            raise ValueError('value does not exist')
        train_brigade.brigade_number = new_number
        # меняем значение ключа на новый номер
        self.database["train_brigades"][train_brigade.brigade_number] = self.database["train_brigades"][number]
        # удаляем старый ключ
        del self.database["train_brigades"][number]
        self.save_database()

    def add_ticket_sales_sheet(self, number_of_train, passenger_fullname, passport, number_of_tickets, benefits, price):
        sale_datetime = str(datetime.now().replace(microsecond=0))
        ticket_sales_sheet = TicketSalesSheet(number_of_train, sale_datetime, passenger_fullname, passport,
                                              number_of_tickets, benefits, price)
        self.database["ticket_sales_sheets"][ticket_sales_sheet.sale_datetime] = ticket_sales_sheet
        if ticket_sales_sheet.trip_number.train.number not in self.database["train_timetables"]:
            # если расписания с таким номером ещё нет в базе, то добавляем его
            self.database["train_timetables"][ticket_sales_sheet.trip_number.train.number] = \
                ticket_sales_sheet.trip_number
        if ticket_sales_sheet.trip_number.train.number not in self.database["trains"]:
            # если поезда с таким номером ещё нет в базе, то также добавляем его
            self.database["trains"][ticket_sales_sheet.trip_number.train.number] = ticket_sales_sheet.trip_number.train
        self.save_database()
        return ticket_sales_sheet, self.database["train_timetables"][
            ticket_sales_sheet.trip_number.train.number], self.database["trains"][
            ticket_sales_sheet.trip_number.train.number]

    def delete_ticket_sales_sheet(self, number):
        del self.database["ticket_sales_sheets"][number]
        self.save_database()

    def get_ticket_sales_sheets_by_datetime(self, sale_datetime):
        if sale_datetime not in self.database["ticket_sales_sheets"]:
            return None
        return self.database["ticket_sales_sheets"][sale_datetime]

    def change_number_of_tickets(self, sale_datetime):
        ticket_sales_sheet = self.get_ticket_sales_sheets_by_datetime(sale_datetime)
        if not ticket_sales_sheet:
            raise ValueError('value does not exist')
        new_value = int(input("New number of tickets: "))
        ticket_sales_sheet.number_of_tickets = new_value
        self.save_database()

    def change_number_of_tickets_qt(self, sale_datetime, new_number_of_tickets):
        ticket_sales_sheet = self.get_ticket_sales_sheets_by_datetime(sale_datetime)
        if not ticket_sales_sheet:
            raise ValueError('value does not exist')
        new_value = int(new_number_of_tickets)
        ticket_sales_sheet.number_of_tickets = new_value
        self.save_database()


# def del_sales(self):
#     """Метод очистки ведомостей"""
#     del self.database['ticket_sales_sheets'][list(self.database['ticket_sales_sheets'].keys())[0]]
#     self.save_database()


class Timer:
    """Декоратор - счетчик времени выполнения метода"""

    def __init__(self, func):
        """Инициализирует атрибут func(функция)"""
        self.func = func

    def __call__(self, *args, **kwargs):
        t1 = time.perf_counter()
        return_value = self.func(*args, **kwargs)
        t2 = time.perf_counter()
        print("Время выполнения метода: {0:0.3f} секунд.".format(t2 - t1))
        return return_value

    def __get__(self, instance, owner):
        """Специальный метод, для работы декоратора"""
        import functools
        return functools.partial(self.__call__, instance)


class Count:
    """Декоратор - счетчик вызовов метода"""
    func_counter = {}

    def __init__(self, func):
        """Инициализирует атрибут func(функция)"""
        self.func = func

    def __call__(self, *args, **kwargs):
        self.func_counter.setdefault(self.func.__name__, 0)
        self.func_counter[self.func.__name__] += 1
        return self.func(*args, **kwargs)

    def __get__(self, instance, owner):
        """Специальный метод, для работы декоратора"""
        import functools
        return functools.partial(self.__call__, instance)

    @classmethod
    def get_func_counter(cls):
        return cls.func_counter


class RZDTransaction:
    """Класс для хранения транзакций"""

    def __init__(self, operation):
        """Инициализирует атрибуты when(дата) и operation(операция)"""
        self.when = datetime.today().replace(microsecond=0)
        self.operation = operation

    def __del__(self):
        """Деструктор, сохраняет транзакции в файл при удалении объекта"""
        print("Вызван деструктор класса RZDTransaction")
        with open('transaction.txt', 'a') as f:
            f.write('when {0} : operation {1} \n'.format(self.when, self.operation))


class WorkerRZD:
    """Модель работника ж.д. вокзала"""

    def __init__(self, surname, name, patronymic, year_of_birth, year_of_employment,
                 seniority, position, gender, address, city, phone):
        """Инициализирует приватные атрибуты"""
        self.__surname = surname  # Фамилия
        self.__name = name  # Имя
        self.__patronymic = patronymic  # Отчество
        self.__year_of_birth = year_of_birth  # Год рождения
        self.__year_of_employment = year_of_employment  # Год поступления на работу
        self.__seniority = seniority  # Стаж
        self.__position = position  # Должность (машинист, диспетчер, проводник, ремонтник подвижного состава,
        # ремонтник путей, кассир, работник службы подготовки составов, работник справочной службы и др.)
        self.__gender = gender  # Пол
        self.__address = address  # Адрес
        self.__city = city  # Город
        self.__phone = phone  # Телефон
        self.__queue = []  # Очередь транзакций

    # Свойства
    def name(self, val):
        """Сеттер имени"""
        self.__name = val

    def seniority(self, val):
        """Сеттер стажа, проверяет валидность значения и устанавливает его, иначе вызывает исключение"""
        if not isinstance(val, int):
            print("Произошла генерация исключения!")
            raise InvalidTypeError(val)
        elif val < 0:
            print("Произошла генерация исключения!")
            raise InvalidValueError(val)
        else:
            self.__seniority = val

    surname = property(lambda self: self.__surname)
    name = property(lambda self: self.__name, name)
    patronymic = property(lambda self: self.__patronymic)
    year_of_birth = property(lambda self: self.__year_of_birth)
    year_of_employment = property(lambda self: self.__year_of_employment)
    seniority = property(lambda self: self.__seniority, seniority)
    position = property(lambda self: self.__position)
    gender = property(lambda self: self.__gender)
    address = property(lambda self: self.__address)
    city = property(lambda self: self.__city)
    phone = property(lambda self: self.__phone)
    queue = property(lambda self: self.__queue)

    @Timer
    @Count
    def do_work(self):
        """Отображает начало выполнения служебных обязанностей работником"""
        time.sleep(1)  # Для тестов
        action = f'{self.position} {self.name.title()} сейчас работает!'
        print(action)
        self.queue.append(RZDTransaction(action))

    @Timer
    @Count
    def end_work(self):
        """Отображает конец выполнения служебных обязанностей работником"""
        action = f'{self.position} {self.name.title()} закончил работу!'
        print(action)
        self.queue.append(RZDTransaction(action))

    @Timer
    @Count
    def get_transaction(self):
        """Удаляет из очереди объекта транзакции, способствует вызову деструктора и записи в файл"""
        for i in range(len(self.queue)):
            item = self.queue.pop(0)
            print('when {0} : operation {1}'.format(item.when, item.operation))

    @Timer
    @Count
    def __show_info(self):
        """Приватный метод вывода информации"""
        action = f'Работник {self.name.title()}!'
        print(action)
        self.queue.append(RZDTransaction(action))

    @Timer
    @Count
    def __change_seniority(self):
        """Приватный метод изменения стажа"""
        self.seniority += 1

    def __add__(self, value):
        """Перегрузка оператора сложения"""
        self.seniority += value

    def __sub__(self, value):
        """Перегрузка оператора вычитания"""
        self.seniority -= value

    def __mul__(self, value):
        """Перегрузка оператора умножения"""
        self.seniority *= value

    def __truediv__(self, value):
        """Перегрузка оператора деления"""
        self.seniority //= value

    def __repr__(self):
        """Выдает строковое представление объекта (работника)"""
        return self.name.title()

    def __del__(self):
        """Деструктор класса WorkerRZD"""
        print("Вызван деструктор класса WorkerRZD")


class TrainDriver(WorkerRZD):
    """Класс потомок работника: машинист"""

    def __init__(self, surname, name, patronymic, year_of_birth, year_of_employment,
                 seniority, position, gender, address, city, phone, duties=None, salary=36500):
        """Вызывает конструктор родительского класса и дополняет его, инициализирует атрибуты"""
        super(TrainDriver, self).__init__(surname, name, patronymic, year_of_birth, year_of_employment,
                                          seniority, position, gender, address, city, phone)
        self.duties = duties  # Обязанности
        self.salary = salary  # Зарплата

    @Timer
    @Count
    def set_duties(self, duties):
        """Определяет обязанности"""
        self.duties = duties
        action = f'Обязанности {self.position}а {self.name.title()}а изменены на "{duties}"!'
        print(action)
        self.queue.append(RZDTransaction(action))

    @Timer
    @Count
    def give_paycheck(self):
        """Выдаёт зарплату"""
        action = f'{self.position} {self.name.title()} получил зарплату!'
        print(action)
        self.queue.append(RZDTransaction(action))

    @Timer
    @Count
    def show_info(self):
        """Показывает информацию о работнике"""
        action = "Работник: {0}\t Должность: {1}\t Стаж: {2}\t Зарплата: {3}\t " \
                 "Обязанности: {4}".format(self.name, self.position, self.seniority, self.salary, self.duties)
        print(action)
        self.queue.append(RZDTransaction(action))

    @Timer
    @Count
    def change_seniority(self):
        """Увеличивает стаж на 1 год, и повышает зарплату с учетом коэффициента"""
        self.seniority += 1
        self.salary *= 1.2
        action = f"Стаж {self.position}а {self.name.title()}а увеличен, зарплата повышена!"
        print(action)
        self.queue.append(RZDTransaction(action))


class TrainConductor(WorkerRZD):
    """Класс потомок работника: проводник"""

    def __init__(self, surname, name, patronymic, year_of_birth, year_of_employment,
                 seniority, position, gender, address, city, phone, duties=None, salary=25000):
        """Вызывает конструктор родительского класса и дополняет его, инициализирует атрибуты"""
        super(TrainConductor, self).__init__(surname, name, patronymic, year_of_birth, year_of_employment,
                                             seniority, position, gender, address, city, phone)
        self.duties = duties  # Обязанности
        self.salary = salary  # Зарплата

    @Timer
    @Count
    def set_duties(self, duties):
        """Определяет обязанности"""
        self.duties = duties
        action = f'Обязанности {self.position}а {self.name.title()}а изменены на "{duties}"!'
        print(action)
        self.queue.append(RZDTransaction(action))

    @Timer
    @Count
    def give_paycheck(self):
        """Выдаёт зарплату"""
        action = f'{self.position} {self.name.title()} получил зарплату!'
        print(action)
        self.queue.append(RZDTransaction(action))

    @Timer
    @Count
    def show_info(self):
        """Показывает информацию о работнике"""
        action = "Работник: {0}\t Должность: {1}\t Стаж: {2}\t Зарплата: {3}\t " \
                 "Обязанности: {4}".format(self.name, self.position, self.seniority, self.salary, self.duties)
        print(action)
        self.queue.append(RZDTransaction(action))

    @Timer
    @Count
    def change_seniority(self):
        """Увеличивает стаж на 1 год, и повышает зарплату с учетом коэффициента"""
        self.seniority += 1
        self.salary *= 1.1
        action = f"Стаж {self.position}а {self.name.title()}а увеличен, зарплата повышена!"
        print(action)
        self.queue.append(RZDTransaction(action))


class PersistenceWorkerRZD:
    """Класс для сериализации/десериализации состояния объектов "работник" в/из файл(а)"""

    @staticmethod
    def serialize(workers):
        """Сериализует состояния объектов (работников) в файл"""
        with open('workers.pkl', 'wb') as f:
            pickle.dump(workers, f)

    @staticmethod
    def deserialize():
        """Десериализует состояния объектов (работников) из файла"""
        with open('workers.pkl', 'rb') as f:
            workers = pickle.load(f)
        return workers

    def __del__(self):
        """Деструктор класса PersistenceWorkerRZD"""
        print("Вызван деструктор класса PersistenceWorkerRZD")


class TrainTimetable:
    """Модель расписания движения поездов"""

    def __init__(self, date_of_departure, time_of_departure, place_of_departure,
                 date_of_arrival, time_of_arrival, place_of_arrival, route, ticket_price,
                 number, release_year=None, number_of_carriages=None, type_of_train=None):
        """Инициализирует приватные атрибуты"""
        self.__train = Train(number, release_year, number_of_carriages, type_of_train)  # Поезд
        self.__date_of_departure = date_of_departure  # Дата отправления
        self.__time_of_departure = time_of_departure  # Время отправления
        self.__place_of_departure = place_of_departure  # Место отправления
        self.__date_of_arrival = date_of_arrival  # Дата прибытия
        self.__time_of_arrival = time_of_arrival  # Время прибытия
        self.__place_of_arrival = place_of_arrival  # Место прибытия
        self.__route = route  # Маршрут (начальный и конечный пункты назначения, основные узловые станции)
        self.__ticket_price = ticket_price  # Стоимость билета
        self.__queue = []  # Очередь транзакций

    # Свойства
    def ticket_price(self, val):
        """Сеттер цены билета, проверяет валидность значения и устанавливает его, иначе вызывает исключение"""
        if not isinstance(val, int):
            print("Произошла генерация исключения!")
            raise InvalidTypeError(val)
        elif val < 0:
            print("Произошла генерация исключения!")
            raise InvalidValueError(val)
        else:
            self.__ticket_price = val

    train = property(lambda self: self.__train)
    date_of_departure = property(lambda self: self.__date_of_departure)
    time_of_departure = property(lambda self: self.__time_of_departure)
    place_of_departure = property(lambda self: self.__place_of_departure)
    date_of_arrival = property(lambda self: self.__date_of_arrival)
    time_of_arrival = property(lambda self: self.__time_of_arrival)
    place_of_arrival = property(lambda self: self.__place_of_arrival)
    route = property(lambda self: self.__route)
    ticket_price = property(lambda self: self.__ticket_price, ticket_price)
    queue = property(lambda self: self.__queue)

    @Timer
    @Count
    def show_timetable(self):
        """Показывает расписание поезда"""
        action = "Расписание:\t Поезд: {0}\t Маршрут: {1}\t Отправление: {2} - {3}\t Прибытие: {4} - {5}\t " \
                 "Стоимость билета: {6} руб.".format(self.train, self.route, self.date_of_departure,
                                                     self.time_of_departure, self.date_of_arrival,
                                                     self.time_of_arrival, self.ticket_price)
        print(action)
        self.queue.append(RZDTransaction(action))

    @Timer
    @Count
    def get_transaction(self):
        """Удаляет из очереди объекта транзакции, способствует вызову деструктора и записи в файл"""
        for i in range(len(self.queue)):
            item = self.queue.pop(0)
            print('when {0} : operation {1}'.format(item.when, item.operation))

    def __add__(self, value):
        """Перегрузка оператора сложения"""
        self.ticket_price += value

    def __sub__(self, value):
        """Перегрузка оператора вычитания"""
        self.ticket_price -= value

    def __mul__(self, value):
        """Перегрузка оператора умножения"""
        self.ticket_price *= value

    def __truediv__(self, value):
        """Перегрузка оператора деления"""
        self.ticket_price //= value

    def __repr__(self):
        """Выдает строковое представление объекта (расписания поезда)"""
        return "Расписание {0}".format(self.train)

    def __del__(self):
        """Деструктор класса TrainTimetable"""
        print("Вызван деструктор класса TrainTimetable")


class PersistenceTrainTimetable:
    """Класс для сериализации/десериализации состояния объектов "расписание движения поездов" в/из файл(а)"""

    @staticmethod
    def serialize(train_timetables):
        """Сериализует состояния объектов (расписаний) в файл"""
        with open('train_timetables.pkl', 'wb') as f:
            pickle.dump(train_timetables, f)

    @staticmethod
    def deserialize():
        """Десериализует состояния объектов (расписаний) из файла"""
        with open('train_timetables.pkl', 'rb') as f:
            train_timetables = pickle.load(f)
        return train_timetables

    def __del__(self):
        """Деструктор класса PersistenceTrainTimetable"""
        print("Вызван деструктор класса PersistenceTrainTimetable")


class Train:
    """Модель поезда"""

    def __init__(self, number, release_year, number_of_carriages, type_of_train):
        """Инициализирует приватные атрибуты"""
        self.__number = number  # Номер
        self.__release_year = release_year  # Год выпуска
        self.__number_of_carriages = number_of_carriages  # Кол-во вагонов
        self.__type_of_train = type_of_train  # Тип поезда (общий, скоростной, высокоскоростной)
        self.__queue = []  # Очередь транзакций

    # Свойства
    def number(self, val):
        """Сеттер номера"""
        self.__number = val

    def number_of_carriages(self, val):
        """Сеттер кол-ва вагонов, проверяет валидность значения и устанавливает его, иначе вызывает исключение"""
        if not isinstance(val, int):
            print("Произошла генерация исключения!")
            raise InvalidTypeError(val)
        elif val < 0:
            print("Произошла генерация исключения!")
            raise InvalidValueError(val)
        else:
            self.__number_of_carriages = val

    number = property(lambda self: self.__number, number)
    release_year = property(lambda self: self.__release_year)
    number_of_carriages = property(lambda self: self.__number_of_carriages, number_of_carriages)
    type_of_train = property(lambda self: self.__type_of_train)
    queue = property(lambda self: self.__queue)

    @Timer
    @Count
    def move(self):
        """Отображает начало движения поезда"""
        action = "{0} поезд номер {1} движется!".format(self.type_of_train, self.number)
        print(action)
        self.queue.append(RZDTransaction(action))

    @Timer
    @Count
    def stop(self):
        """Отображает остановку движения поезда"""
        action = "{0} поезд номер {1} стоит!".format(self.type_of_train, self.number)
        print(action)
        self.queue.append(RZDTransaction(action))

    @Timer
    @Count
    def get_transaction(self):
        """Удаляет из очереди объекта транзакции, способствует вызову деструктора и записи в файл"""
        for i in range(len(self.queue)):
            item = self.queue.pop(0)
            print('when {0} : operation {1}'.format(item.when, item.operation))

    def __add__(self, value):
        """Перегрузка оператора сложения"""
        self.number_of_carriages += value

    def __sub__(self, value):
        """Перегрузка оператора вычитания"""
        self.number_of_carriages -= value

    def __mul__(self, value):
        """Перегрузка оператора умножения"""
        self.number_of_carriages *= value

    def __truediv__(self, value):
        """Перегрузка оператора деления"""
        self.number_of_carriages //= value

    def __repr__(self):
        """Выдает строковое представление объекта (поезда)"""
        return "Поезд номер {0}".format(self.number)

    def __del__(self):
        """Деструктор класса Train"""
        print("Вызван деструктор класса Train")


class PersistenceTrain:
    """Класс для сериализации/десериализации состояния объектов "поезд" в/из файл(а)"""

    @staticmethod
    def serialize(trains):
        """Сериализует состояния объектов (поездов) в файл"""
        with open('trains.pkl', 'wb') as f:
            pickle.dump(trains, f)

    @staticmethod
    def deserialize():
        """Десериализует состояния объектов (поездов) из файла"""
        with open('trains.pkl', 'rb') as f:
            trains = pickle.load(f)
        return trains

    def __del__(self):
        """Деструктор класса PersistenceTrain"""
        print("Вызван деструктор класса PersistenceTrain")


class TrainBrigade:
    """Модель бригады поезда"""

    def __init__(self, brigade_number, surname, name, position,
                 number_of_train, release_year=None, number_of_carriages=None, type_of_train=None,
                 patronymic=None, year_of_birth=None, year_of_employment=None,
                 seniority=None, gender=None, address=None, city=None, phone=None):
        """Инициализирует приватные атрибуты"""
        self.__brigade_number = brigade_number  # Номер бригады
        self.__train = Train(number_of_train, release_year, number_of_carriages, type_of_train)  # Поезд
        self.__rzd_workers = [WorkerRZD(surname, name, patronymic, year_of_birth, year_of_employment,
                                        seniority, position, gender, address, city, phone)]  # Работники ж.д. вокзала
        # (машинисты, техники, проводники и обслуживающий персонал)
        self.__queue = []  # Очередь транзакций

    # Свойства
    def brigade_number(self, val):
        """Сеттер номера бригады, проверяет валидность значения и устанавливает его, иначе вызывает исключение"""
        if not isinstance(val, str):
            print("Произошла генерация исключения!")
            raise InvalidTypeError(val)
        elif int(val) < 0:
            print("Произошла генерация исключения!")
            raise InvalidValueError(val)
        else:
            self.__brigade_number = val

    brigade_number = property(lambda self: self.__brigade_number, brigade_number)
    train = property(lambda self: self.__train)
    rzd_workers = property(lambda self: self.__rzd_workers)
    queue = property(lambda self: self.__queue)

    @Timer
    @Count
    def show_brigade_info(self):
        """Отображает информацию о бригаде поезда"""
        action = "Бригада №{0}, обслуживает поезд {1}. " \
                 "Работники: {2}".format(self.brigade_number, self.train, self.rzd_workers)
        print(action)
        self.queue.append(RZDTransaction(action))

    @Timer
    @Count
    def get_transaction(self):
        """Удаляет из очереди объекта транзакции, способствует вызову деструктора и записи в файл"""
        for i in range(len(self.queue)):
            item = self.queue.pop(0)
            print('when {0} : operation {1}'.format(item.when, item.operation))

    def __add__(self, value):
        """Перегрузка оператора сложения"""
        self.brigade_number += value

    def __sub__(self, value):
        """Перегрузка оператора вычитания"""
        self.brigade_number -= value

    def __mul__(self, value):
        """Перегрузка оператора умножения"""
        self.brigade_number *= value

    def __truediv__(self, value):
        """Перегрузка оператора деления"""
        self.brigade_number //= value

    def __repr__(self):
        """Выдает строковое представление объекта (бригады поезда)"""
        return "Бригада номер {0}".format(self.brigade_number)

    def __del__(self):
        """Деструктор класса TrainBrigade"""
        print("Вызван деструктор класса TrainBrigade")


class PersistenceTrainBrigade:
    """Класс для сериализации/десериализации состояния объектов "бригада поезда" в/из файл(а)"""

    @staticmethod
    def serialize(train_brigades):
        """Сериализует состояния объектов (бригады поездов) в файл"""
        with open('train_brigades.pkl', 'wb') as f:
            pickle.dump(train_brigades, f)

    @staticmethod
    def deserialize():
        """Десериализует состояния объектов (бригады поездов) из файла"""
        with open('train_brigades.pkl', 'rb') as f:
            train_brigades = pickle.load(f)
        return train_brigades

    def __del__(self):
        """Деструктор класса PersistenceTrainBrigade"""
        print("Вызван деструктор класса PersistenceTrainBrigade")


class TicketSalesSheet:
    """Модель ведомости продаж билетов"""

    def __init__(self, number_of_train, sale_datetime, passenger_fullname, passport, number_of_tickets, benefits, price,
                 date_of_departure=None, time_of_departure=None, place_of_departure=None,
                 date_of_arrival=None, time_of_arrival=None, place_of_arrival=None, route=None, ticket_price=None,
                 release_year=None, number_of_carriages=None, type_of_train=None):
        """Инициализирует приватные атрибуты"""
        self.__sale_datetime = sale_datetime  # Дата и время продажи
        self.__passenger_fullname = passenger_fullname  # ФИО пассажира
        self.__passport = passport  # Паспортные данные
        self.__trip_number = TrainTimetable(date_of_departure, time_of_departure, place_of_departure,
                                            date_of_arrival, time_of_arrival, place_of_arrival, route, ticket_price,
                                            number_of_train, release_year, number_of_carriages, type_of_train)  # Номер
        self.__number_of_tickets = number_of_tickets  # Кол-во билетов
        self.__benefits = benefits  # Наличие льгот (пенсионеры, дети-сироты и т.д.)
        self.__price = price  # Стоимость
        self.__queue = []  # Очередь транзакций

    # Свойства
    def number_of_tickets(self, val):
        """Сеттер кол-ва билетов, проверяет валидность значения и устанавливает его, иначе вызывает исключение"""
        if not isinstance(val, int):
            print("Произошла генерация исключения!")
            raise InvalidTypeError(val)
        elif val < 0:
            print("Произошла генерация исключения!")
            raise InvalidValueError(val)
        else:
            self.__number_of_tickets = val

    sale_datetime = property(lambda self: self.__sale_datetime)
    passenger_fullname = property(lambda self: self.__passenger_fullname)
    passport = property(lambda self: self.__passport)
    trip_number = property(lambda self: self.__trip_number)
    number_of_tickets = property(lambda self: self.__number_of_tickets, number_of_tickets)
    benefits = property(lambda self: self.__benefits)
    price = property(lambda self: self.__price)
    queue = property(lambda self: self.__queue)

    @Timer
    @Count
    def show_ticket_sales_sheet(self):
        """Отображает ведомость продаж билетов"""
        action = "Дата и время продажи: {0}\t ФИО пассажира: {1}\t Паспортные данные: {2}\t" \
                 "Номер рейса: {3}\t Кол-во билетов: {4}\t Наличие льгот: {5}\t " \
                 "Стоимость: {6} руб.".format(self.sale_datetime, self.passenger_fullname, self.passport,
                                              self.trip_number, self.number_of_tickets, self.benefits, self.price)
        print(action)
        self.queue.append(RZDTransaction(action))

    @Timer
    @Count
    def get_transaction(self):
        """Удаляет из очереди объекта транзакции, способствует вызову деструктора и записи в файл"""
        for i in range(len(self.queue)):
            item = self.queue.pop(0)
            print('when {0} : operation {1}'.format(item.when, item.operation))

    def __add__(self, value):
        """Перегрузка оператора сложения"""
        self.number_of_tickets += value

    def __sub__(self, value):
        """Перегрузка оператора вычитания"""
        self.number_of_tickets -= value

    def __mul__(self, value):
        """Перегрузка оператора умножения"""
        self.number_of_tickets *= value

    def __truediv__(self, value):
        """Перегрузка оператора деления"""
        self.number_of_tickets //= value

    def __repr__(self):
        """Выдает строковое представление объекта (ведомости продаж билетов)"""
        return f"Ведомость {self.sale_datetime}"

    def __del__(self):
        """Деструктор класса TicketSalesSheet"""
        print("Вызван деструктор класса TicketSalesSheet")


class PersistenceTicketSalesSheet:
    """Класс для сериализации/десериализации состояния объектов "ведомость продаж билетов" в/из файл(а)"""

    @staticmethod
    def serialize(ticket_sales_sheets):
        """Сериализует состояния объектов (ведомости продаж билетов) в файл"""
        with open('ticket_sales_sheets.pkl', 'wb') as f:
            pickle.dump(ticket_sales_sheets, f)

    @staticmethod
    def deserialize():
        """Десериализует состояния объектов (ведомости продаж билетов) из файла"""
        with open('ticket_sales_sheets.pkl', 'rb') as f:
            ticket_sales_sheets = pickle.load(f)
        return ticket_sales_sheets

    def __del__(self):
        """Деструктор класса PersistenceTicketSalesSheet"""
        print("Вызван деструктор класса PersistenceTicketSalesSheet")


class InvalidTypeError(Exception):
    """Собственный класс исключения (неверный тип данных)"""

    def __init__(self, value):
        """Инициализирует атрибут"""
        self.value = value

    def __str__(self):
        """Возвращает строковое представление ошибки"""
        return "Значение '{0}' должно быть числом!".format(self.value)


class InvalidValueError(Exception):
    """Собственный класс исключения (неверное значение)"""

    def __init__(self, value):
        """Инициализирует атрибут"""
        self.value = value

    def __str__(self):
        """Возвращает строковое представление ошибки"""
        return "Значение '{0}' должно быть положительным числом!".format(self.value)
