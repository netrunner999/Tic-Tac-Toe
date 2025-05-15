***Внимание!: Данная программа является тестовой версией и разрабатывается исключительно в учебных целях.***

***Название программы: Tic-Tac-Toe (возможно будет изменено на Cyber Tic-Tac-Toe)***

***На данный момент в программе реализовано***

- Игровое поле 3x3
- Игровое поле 9x9 (и соответственно возможность переключаться между полями)
- Возможность выбора игроками имен (ников)
- Вывод результата игры (X wins or O wins or Draw)
- Реализация меню игры в котором игроки смогут вводить свои ники и выбрать тип поля
- Возможность начать новую игру после завершения предыдущей (или прямо в процессе предыдущей игры, если например очевидна ситуация в которой итогом будет ничья)
- Разработан Cyber-дизайн для всех элементов приложения с использованием CSS-свойств
- Создан .exe файл, что упрощает загрузку и запуск программы (был проведен пробный запуск на трех разных компьютерах, на одном из которых не был установлен python)
- Реализован режим мультиплеера для поля 3x3, игроки смогут играть на разных устройствах (требуется одна локальная сеть).

***Процесс установки и запуска программы***

На главной странице проекта нажмите на зеленую кнопку Code, далее в выпадающем меню выберете Download ZIP, в результате в загрузки вашего компьютера скачается .zip архив, архив распакуйте в любой директории (рекомендуется на рабочем столе). Чтобы запустить программу перейдите в распакованную папку Tic-Tac-Toe-dev, далее папка dist, здесь лежит исполняемый файл main.exe и файл логов game, запуск main.exe файла запустит приложение. Во время запуска .exe файла Windows может выдать ошибку "Не удается проверить издателя!", данная ошибка возникает поскольку это open-source проект, просто нажмите Ok в открывшемся окне с ошибкой.

***Режим Мультиплеера***
Внимание: игра в рижиме мультиплеера возможна, только если клиент и хост находятся в одной локальной сети, так как подключение происходит по ip хоста в локальной сети.
Для начала игры один из игроков должен выбрать режим игры Онлайн - Хост (этот игрок будет являться сервером), другой игрок должен выбрать режим Онлайн - Клиент и ввести в поле для ввода ip-аддресса ip хоста (можно вводить просто в формате 111.111.11.11 - программа сама подставит порт). Мультиплеерный режим реализован только для поля 3x3 (другой тип поля невозможно будет выбрать в меню игры при выборе онлайн режима). Для выхода из мультиплеера применяется кнопка Go to main menu или просто закрывается приложение. При нажатии кнопки New Game хостом или клиентом поле обновляется и игра продолжается, соединение не прерывается.

***Attention!: This program is a test version and is being developed solely for educational purposes.***

***Program name: Tic-Tac-Toe (may be changed to Cyber Tic-Tac-Toe)***

***At the moment, the program has implemented***

  - The playing field is 3x3
  - Game result output (X wins or O wins or Draw)
  - The ability to start a new game after completing the previous one (or right during the previous game, if, for example, a situation is obvious in which the result will be a draw)
  - A cyber design has been developed for all application elements using CSS properties.
  - Generated.an exe file, which makes it easier to download and run the program (a trial run was conducted on three different computers, one of which did not have python installed)

***The following elements are expected to be implemented in the future***

 - The playing field is 9x9 (and, accordingly, the ability to switch between fields)
 - The ability for players to choose names (nicknames) (the feature has already been implemented, but due to several critical bugs it was temporarily cut out and will be finalized)
 - The game will be divided into stages of 5 rounds, after which the players will see a table of results for the last 5 rounds (it is assumed that these 5 rounds are played on the same field by the same players, at the end of these 5 rounds, players will be asked to change nicknames and the type of field)
 - Implementation of the game menu in which players can enter their nicknames and select the type of field
 - Implementation of an additional Player vs Bot mode (it will definitely be developed on the 3x3 field, it will be more difficult to develop on the 9x9 field (most likely you will have to use a neural network, possibly through the api of some neural network))

***The process of installing and launching the program***

On the main page of the project, click on the green Code button, then select Download ZIP from the drop-down menu. As a result, it will be downloaded to your computer's downloads.zip archive, unzip the archive in any directory (recommended on the desktop). To run the program, go to the unpacked Tic-Tac-Toe-dev folder, then the output folder, then the main folder, here lies the executable file. main.exe running this file will launch the application. During the launch .The Windows exe file may give the error "Unable to verify the publisher!", this error occurs because it is an open-source project, just click Ok in the error window that opens.
