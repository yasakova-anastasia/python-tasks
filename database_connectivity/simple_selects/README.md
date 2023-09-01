## Simple Selects

`sql` `orm` `query builder` `database`

### Условие

Нужно реализовать класс, который инкапуслирует общение с БД.
Потребуется релизовать три метода, которые запрашивают данные из базы.
Инструменты не регламентируются: можно ставить что угодно с помощью
задания зависимостей через setup.py.
Можно как писать сырой SQL, так и прикручивать любимую ORM.

Методы __init__, teardown даны для того, чтобы не приходилось для каждого теста открывать
отдельное соединение, а также чтобы в конце закрыть его. Пока что это не проверяется тестами, но на разборе буду
ругаться, если коннект открывается в каждом запросе или не закрывается в teardown (внутрь фреймворков лезть
не нужно: считаем что ормка не злоупотребляет коннектами).

Описание того, что нужно вернуть, указано в докстринге к каждому из методов заглушки.
В качестве базы используется тестовая база из [туториала по sqlite3](https://www.sqlitetutorial.net/sqlite-sample-database/).
Пдфку с ее схемой можно найти там же где и сам файл или в [репо с лекциями](https://gitlab.manytask.org/py-tasks/lectures-2020-fall/-/tree/master/12.2.ExtensionsAndSerialization)


### Пререквы 

Предполагается, что SQL на базовом уровне уже известен, но на всякий случай в
докстрингах даны подсказки что пояндексить.