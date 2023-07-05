from typing import Any, Iterable, Iterator, NamedTuple, Optional
import json
import os

ABS_PATH = os.path.dirname(__file__)
DATA_PATH = ABS_PATH + '/../data/data.json'
BACKUP_PATH = ABS_PATH + '/../backups'
REQUEST_BATCH_LENGTH = 10
DATA_SIZE_MAX = 40


class Measure(NamedTuple):
    name: str
    date: int
    photo: Optional[str]
    temperature: Optional[float]
    humidity: Optional[float]
    state: Optional[str]

    @classmethod
    def from_dict(cls, d: Iterable[dict[str, Any]]) -> Iterator['Measure']:
        for x in d:
            yield cls(
                name=x['name'],
                date=x['date'],
                photo=x['photo'],
                temperature=x.get('temperature'),
                humidity=x.get('humidity'),
                state=x.get('state')
            )

    @classmethod
    def from_json(cls, d: dict[str, Any]) -> 'Measure':
        return cls(
            name=d['name'],
            date=d['date'],
            photo=d['photo'],
            temperature=d.get('temperature'),
            humidity=d.get('humidity'),
            state=d.get('state')
        )

    # Il n'y a pas la photo
    @property
    def to_list(self) -> list:
        return [self.name, self.date, self.temperature, self.humidity, self.state]

    # Il n'y a pas la photo
    def __str__(self) -> str:
        return (
            f'{self.date} : '
            f'{self.name} | '
            f'temperature : {self.temperature} | '
            f'humidity : {self.humidity} | '
            f'state : {self.state}'
        )


def get_data() -> list:
    if not os.path.exists(DATA_PATH):
        with open(DATA_PATH, "w") as file:
            json.dump([], file)
            return []
    else:
        with open(DATA_PATH, 'r') as file:
            d = json.load(file)
            return d


def save_data() -> str:
    global data
    with open(DATA_PATH, 'w') as file:
        json.dump(data, file, indent=4)
        return 'Saved data'


def backup_data() -> None:
    global data
    n = len(os.listdir(BACKUP_PATH))       # On regarde le nombre de fichiers dans backups/
    with open(BACKUP_PATH + f'/backup_{n}.json', 'a') as file:
        json.dump(data, file, indent=4)
        data.clear()


def print_data(x: dict) -> None:
    measures = Measure.from_dict(x)
    for measure in measures:
        print(measure)


def data_to_string(x: dict) -> list:
    measures = Measure.from_dict(x)
    return [str(x) for x in measures]


def add_data(x: dict) -> str:
    global data
    global requests
    data.append(x)
    requests += 1
    if requests % REQUEST_BATCH_LENGTH == 0:
        save_data()
    if requests % DATA_SIZE_MAX == 0:
        backup_data()
    print('-> Added new data: ' + str(x))
    return 'Add new data'


def clear_data() -> str:
    global data
    data.clear()
    print('-> Cleared data')
    return 'Cleared data'


data = get_data()
requests = 0
