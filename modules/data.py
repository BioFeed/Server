from typing import Any, Iterable, Iterator, NamedTuple, Optional


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