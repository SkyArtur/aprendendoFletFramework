# Aprendendo Flet - Python

Conhecendo o framework [Flet](https://flet.dev/) para criação de aplicações multi plataformas.

## Conexão com o banco de dados

### Classe Connector:
É a classe base abstrata que define a interface para conectar e executar operações nos diferentes bancos de dados 
(SQLite, MySQL, PostgreSQL). Usa o padrão Singleton para garantir que apenas uma instância da conexão seja criada.

- **Método __execute**: É responsável por executar consultas no banco de dados, podendo realizar operações de fetch (busca) 
ou commit (salvamento). Ele gerencia exceções específicas de diferentes tipos de banco de dados e garante que os 
cursores e conexões sejam fechados corretamente no final.

```python
import sqlite3
import psycopg2
import mysql.connector
from abc import abstractmethod


class Connector:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(Connector, cls).__new__(cls)
        return cls.__instance


    def __init__(self, **kwargs):
        self.params = kwargs
        self.__cursor = None
        self.__connection = None
        self.__response = None

    @abstractmethod
    def connect(self):
        ...

    def __execute(self, query: str, data: tuple = None, fetch: bool = False, commit: bool = False) -> list[tuple] | None:
        try:
            self.__connection = self.connect()
            self.__cursor = self.__connection.cursor()
            self.__cursor.execute(query, data) if data else self.__cursor.execute(query)
        except (psycopg2.Error, mysql.connector.Error, sqlite3.Error, Exception) as error:
            return error
        else:
            if fetch:
                self.__response = self.__cursor.fetchall()
            if commit:
                self.__connection.commit()
            return self.__response
        finally:
            try:
                self.__cursor.close()
                self.__connection.close()
            except (psycopg2.Error, mysql.connector.Error, sqlite3.Error, Exception) as error:
                return error

    def create(self, query: str):
        self.__execute(query, commit=True)

    def save(self, query: str, data: tuple):
        return self.__execute(query, data, commit=True, fetch=True)

    def fetch(self, query: str, data: tuple = None):
        return self.__execute(query, data, fetch=True)
```

### Subclasses SQLiteConnector, MySQLConnector, PostgreSQLConnector: 
São subclasses da classe Connector que implementam o método abstrato connect para fornecer conexões específicas aos 
bancos de dados correspondentes.
```python
from ._singleton import *


class SQLiteConnector(Connector):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def connect(self) -> sqlite3.connect:
        return sqlite3.connect(**self.params)


class MySQLConnector(Connector):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def connect(self) -> mysql.connector.connect:
        return mysql.connector.connect(**self.params)


class PostgreSQLConnector(Connector):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def connect(self) -> psycopg2.connect:
        return psycopg2.connect(**self.params)
```
### Classe Database: 
Também segue o padrão Singleton e seleciona o conector adequado com base no driver fornecido (sqlite, mysql ou postgres).

```python
from typing import Literal
from ._objects import SQLiteConnector, MySQLConnector, PostgreSQLConnector


class Database:
    __instance = None

    def __new__(cls, __driver: Literal['sqlite', 'mysql','postgres'], *args, **kwargs):
        if cls.__instance is None:
            match __driver:
                case 'sqlite':
                    cls.__instance = SQLiteConnector(**kwargs)
                case 'mysql':
                    cls.__instance = MySQLConnector(**kwargs)
                case 'postgres':
                    cls.__instance = PostgreSQLConnector(**kwargs)
                case _:
                    raise ValueError(f'Unsupported database driver: {__driver}')
        return cls.__instance
```

## Validações de dados

### decorator_validators(function: Callable) -> Callable

Essa função é um decorador que adiciona uma camada de validação e tratamento de exceções a outras funções. A ideia é 
interceptar chamadas a essas funções, capturar possíveis erros e exibir mensagens de erro adequadas por meio de um 
componente de notificação chamado snack_bar. Todas as funções de validação compartilham essa funcionalidade adicional.
O uso do decorador centraliza o tratamento de exceções e notifica o usuário de forma amigável. Isso mantém o código 
limpo e fácil de manter, já que o tratamento de erros não precisa ser repetido em cada função.

```python
from typing import Callable
from components import snack_bar, Page


def decorator_validators(function: Callable) -> Callable:
    def _wrapper(page: Page, *args, **kwargs):
        try:
            _input = function(page, *args, **kwargs)
        except Exception as e:
            snack_bar(page, f'{e}.', function)
        else:
            return _input
    return _wrapper
```

### validator_fields(page: Page, *args: TextField) -> bool | None
Essa função verifica se todos os campos fornecidos (TextField) têm valores válidos (não nulos ou vazios). 
Se algum campo estiver vazio, ela lança uma exceção.

```python
from components import  Page, TextField
from ._decorator import decorator_validators


@decorator_validators
def validator_fields(page: Page, *args: TextField) -> bool | None:
    for text_field in args:
        if text_field.value is None or text_field.value == '':
            raise ValueError(f'Field "{text_field.label}" cannot be null')
    return True
```

### validate_name(page: Page, _name: TextField) -> str | None
Essa função valida se o nome fornecido é uma string alfanumérica. Nomes com caracteres especiais ou números não são permitidos.

```python
from components import  Page, TextField
from ._decorator import decorator_validators


@decorator_validators
def validate_name(page: Page, _name: TextField) -> str | None:
    if not isinstance(_name.value, str) or not _name.value.replace(' ', '').isalnum():
        raise ValueError(f'Value entered in the {_name.label} field is not valid')
    return _name.value
```

### validate_username(page: Page, _username: TextField) -> str | None
Verifica se o nome de usuário fornecido já existe no banco de dados. Se existir, lança uma exceção. Isso 
acrescenta uma camada extra para garantir que o nome de usuário inserido no campo username_field seja único no banco de dados.

```python
from database import dbDev
from components import  Page, TextField
from ._decorator import decorator_validators


@decorator_validators
def validate_username(page: Page, _username: TextField) -> str | None:
    if dbDev.fetch('SELECT id FROM users WHERE username = %s;', (_username.value,)):
        raise ValueError('Username already exists')
    return _username.value
```

### validate_password(page: Page, _password: TextField, _confirm: TextField) -> str | None
Valida uma senha fornecida, garantindo que ela tenha pelo menos 6 caracteres e que a confirmação da senha corresponda à 
senha original. Se as validações passarem, a função retorna a senha criptografada.

```python
from passlib.hash import pbkdf2_sha256 as pbk
from components import  Page, TextField
from ._decorator import decorator_validators



@decorator_validators
def validate_password(page: Page, _password: TextField, _confirm: TextField) -> str | None:
    if len(_password.value) < 6:
        raise ValueError('Password must be at least 6 characters')
    elif _password.value != _confirm.value:
        raise ValueError('Confirm password must equal password')
    else:
        return pbk.hash(_password.value)

```

### validate_email(page: Page, _email: TextField) -> str | None
Valida o formato de um endereço de e-mail e verifica se o e-mail já está registrado no banco de dados.

```python
import re
from database import dbDev
from components import  Page, TextField
from ._decorator import decorator_validators


@decorator_validators
def validate_email(page: Page, _email: TextField) -> str | None:
    try:
        email = re.search(r'^[a-z0-9_.+-]+@([a-z0-9-]+\.)+[a-z]{2,}$', _email.value).string
        if dbDev.fetch('SELECT id FROM users WHERE email = ?;', (email,)):
            raise ValueError('Email already registered!')
    except (TypeError, ValueError, AttributeError) as error:
        if isinstance(error, AttributeError):
            error = Exception('Value is not valid for a email')
        raise error
    else:
        return email
```

### validate_date(page: Page, _date: TextField, _format: Literal['UK', 'US', 'ISO'] = 'UK') -> datetime.date
Valida uma data de acordo com o formato especificado (UK, US ou ISO) e retorna a data em um objeto datetime.date.

```python
import re
import datetime
from typing import Literal
from components import  Page, TextField
from ._decorator import decorator_validators


@decorator_validators
def validate_date(page: Page, _date: TextField, _format: Literal['UK', 'US', 'ISO'] = 'UK') -> datetime.date:
    try:
        date = [int(i) for i in re.search(r'^([0-9]{2,4})[/-]?([0-9]{2})[/-]?([0-9]{2,4})$', _date.value).groups()]
        match _format:
            case 'UK':
                return datetime.date(day=date[0], month=date[1], year=date[2])
            case 'US':
                return datetime.date(day=date[1], month=date[0], year=date[2])
            case 'ISO':
                return datetime.date(day=date[2], month=date[1], year=date[0])
            case _:
                raise ValueError('Invalid date format')
    except (ValueError, AttributeError) as error:
        if isinstance(error, AttributeError):
            raise Exception(f'Invalid date string')
        else:
            raise error
```

### validate_biometric(page: Page, _field: TextField, _biometric: Literal['weight', 'height']) -> float
A função validate_biometric é usada para validar campos de formulário que correspondem a dados biométricos, 
como peso (weight) ou altura (height). Dependendo do tipo de dado biométrico especificado, a função verifica se o valor 
está dentro de um intervalo aceitável. Se o valor não estiver dentro desse intervalo, ela lança um erro.

```python
from typing import Literal
from components import Page, TextField
from ._decorator import decorator_validators


@decorator_validators
def validate_biometric(page: Page, _field: TextField, _biometric: Literal['weight', 'height']) -> float:
    value = float(_field.value.replace(',', '.'))
    match _biometric:
        case 'weight':
            if value < 0 or value > 300:
                raise ValueError(f'Value {value} must be between 0 and 300')
        case 'height':
            if value < 0 or value > 3:
                raise ValueError(f'Value {value} must be between 0 and 3')
        case _:
            raise ValueError(f'Invalid value for {_field}')
    return value
```

O conjunto de funções apresentadas faz parte de um sistema de validação de dados voltado para uma interface de usuário 
que irá lidar com formulários. Cada função de validação garante que os dados inseridos pelo usuário estejam no formato 
correto antes de serem processados, o que ajuda a evitar erros no banco de dados e melhora a experiência do usuário final.
