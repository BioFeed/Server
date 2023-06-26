from typing import Any, Iterable, Iterator, NamedTuple, Optional
import json
import os

ABS_PATH = os.path.abspath('.')
DATA_PATH = ABS_PATH + '/data/data.json'


class Measure(NamedTuple):
    name: str
    date: int
    photo: Optional[str]
    temperature: Optional[float]
    humidity: Optional[float]
    state: Optional[str]

    @classmethod
    def from_dict(cls, data: Iterable[dict[str, Any]]) -> Iterator['Measure']:
        for x in data:
            yield cls(
                name=x['name'],
                date=x['date'],
                photo=x['photo'],
                temperature=x.get('temperature'),
                humidity=x.get('humidity'),
                state=x.get('state')
            )

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> 'Measure':
        return cls(
            name=data['name'],
            date=data['date'],
            photo=data['photo'],
            temperature=data.get('temperature'),
            humidity=data.get('humidity'),
            state=data.get('state')
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


def get_data() -> dict:
    if not os.path.exists(DATA_PATH):
        with open(DATA_PATH, "w") as file:
            json.dump([], file)
            return dict([])
    else:
        with open(DATA_PATH, 'r') as file:
            data = json.load(file)
            return data


def save_data() -> str:
    with open(DATA_PATH, 'w') as file:
        json.dump(data, file, indent=4)
        return 'Saved data'


def print_data(data) -> None:
    measures = Measure.from_dict(data)
    for measure in measures:
        print(measure)


def data_to_string(data) -> list:
    measures = Measure.from_dict(data)
    return [str(x) for x in measures]


def add_data(x) -> str:
    global data
    data.append(x)
    print('-> Added new data: ' + str(x))
    return 'Add new data'


def clear_data() -> str:
    global data
    data.clear()
    print('-> Cleared data')
    return 'Cleared data'


data = get_data()