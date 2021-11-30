import logging

logging.basicConfig(filename="logfile.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(funcName)s: "
                                                                       "%(lineno)d - %(message)s")
log = logging.getLogger()


def check_color(x1, y1, x2, y2):  # Функция опредения цвета поля
    logging.info("Равны ли остатки от деления на 2 суммы ( %s и %s ) и суммы ( %s и %s ) " % (x1, y1, x2, y2))
    if (x1 + y1) % 2 != 0:
        print("Первая фигура находится на черном поле")
    else:
        print("Первая фигура находится на белом поле")
    if (x2 + y2) % 2 != 0:
        print("Вторая фигура находится на черном поле")
    else:
        print("Вторая фигура находится на белом поле")
    if (x1 + y1) % 2 != (x2 + y2) % 2:
        print("Фигуры стоят на полях разного цвета")
        logging.info("Остатки от деления на 2 - %s и %s, они не равны " % ((x1 + y1) % 2, (x2 + y2) % 2))
    else:
        print("Фигуры стоят на полях одинакового цвета")
        logging.info("Остатки от деления на 2 - %s и %s, они равны " % ((x1 + y1) % 2, (x2 + y2) % 2))


class ChessMan(object):  # Родительский класс шахматных фигур
    IMG = None

    def __init__(self, color):
        self.color = color

    def __repr__(self):
        return self.IMG[self.color]


class Pawn(ChessMan):  # Пешка
    IMG = ('♙', '♟')


class Queen(ChessMan):  # Ферзь
    IMG = ('♕', '♛')


class Rook(ChessMan):  # Ладья
    IMG = ('♖', '♜')


class Bishop(ChessMan):  # Слон
    IMG = ('♗', '♝')


class Knight(ChessMan):  # Конь
    IMG = ('♘', '♞')


try:
    # Ввод данных
    print(
        "Первое число — номер вертикали (при счете слева направо), второе — номер горизонтали (при счете снизу вверх)")
    k, l = map(int, input("Введите через пробел номер вертикали и горизонтали для первой фигуры: ").split())
    if k > 8 or k < 1 or l > 8 or l < 1:
        logging.error("Ошибка! %s или %s вне диапазона от 1 до 8" % (k, l))
        quit("Ошибка! Нужно ввести число от 1 до 8! Перезапустите программу!")
    chessman_n = int(
        input("\nВведите номер для определение типа первой фигуры\n1. Ферзь\n2. Ладья\n3. Слон\n4. Конь\n"))
    if chessman_n > 4 or chessman_n < 1:
        logging.error("Ошибка! %s вне диапазона от 1 до 4" % chessman_n)
        quit("Ошибка! Нужно ввести число от 1 до 4! Перезапустите программу!")
    m, n = map(int, input("Введите через пробел номер вертикали и горизонтали для второй фигуры: ").split())
    if m > 8 or m < 1 or n > 8 or n < 1:
        logging.error("Ошибка! %s или %s вне диапазона от 1 до 8" % (m, n))
        quit("Ошибка! Нужно ввести число от 1 до 8! Перезапустите программу!")
    # Массивы координат фигур для второго хода
    k_new = []
    l_new = []


    class Board(object):  # Класс шахматной доски
        def __init__(self):
            self.board = [[' '] * 8 for i in range(8)]  # Создание шахматной доски
            self.board[(l - 8) * -1][k - 1] = (Queen(1), Rook(1), Bishop(1), Knight(1))[chessman_n - 1]
            self.board[(n - 8) * -1][m - 1] = Pawn(1)

        def __repr__(self):
            res = ''
            for i in range(8):
                res += ''.join(map(str, self.board[i])) + "\n"
            return res

        def __str__(self):  # Вывод шахматного поля и фигур на нём
            colors = [40, 0]
            res = ''
            i = 0
            for y in range(8):
                for x in range(8):
                    res += set_color(colors[i]) + str(self.board[y][x]) + ' '
                    i = 1 - i
                i = 1 - i
                res += set_color(0) + '\n'
            return res


    def set_color(color):  # Определение цвета для полей шахматной доски
        return '\033[%sm' % color


    def Queen_move(k, l, m, n):  # Проверка для ходов ферзя
        if k == m or l == n or (abs(k - m) == abs(l - n)):
            print("Ферзь угрожает пешке")
            logging.info("%s = %s или %s = %s или %s = %s" % (k, m, l, n, abs(k - m), abs(l - n)))
            logging.info("Так как ферзь находится на одной диагонали или вертикали или горизонтали - он угрожает пешке")
        else:
            print("Ферзь не угрожает пешке")
            print("Клетки чтобы уничтожить пешку со второго хода")
            logging.info("%s ≠ %s или %s ≠ %s или %s ≠ %s" % (k, m, l, n, abs(k - m), abs(l - n)))
            logging.info("Так как ферзь не находится на одной диагонали или вертикали или горизонтали - он не "
                         "угрожает пешке")
            k_new.append(k)
            k_new.append(m)
            l_new.append(n)
            l_new.append(l)
            k2 = k3 = k4 = k5 = k
            l2 = l3 = l4 = l5 = l
            while k2 < 8 and l2 < 8:
                k2 += 1
                l2 += 1
                if abs(k2 - m) == abs(l2 - n) or k2 == m or l2 == n:
                    k_new.append(k2)
                    l_new.append(l2)
            while k3 < 9 and l3 > 1:
                k3 += 1
                l3 -= 1
                if abs(k3 - m) == abs(l3 - n) or k3 == m or l3 == n:
                    k_new.append(k3)
                    l_new.append(l3)
            while k4 > 1 and l4 < 8:
                k4 -= 1
                l4 += 1
                if abs(k4 - m) == abs(l4 - n) or k4 == m or l4 == n:
                    k_new.append(k4)
                    l_new.append(l4)
            while k5 > 1 and l5 > 1:
                k5 -= 1
                l5 -= 1
                if abs(k5 - m) == abs(l5 - n) or k5 == m or l5 == n:
                    k_new.append(k5)
                    l_new.append(l5)


    def Rook_move(k, l, m, n):  # Проверка для ходов ладьи
        if k == m or l == n:
            print("Ладья угрожает пешке")
            logging.info("%s = %s или %s = %s" % (k, m, l, n))
            logging.info("Так как ладья находится на одной вертикали или горизонтали - она угрожает пешке")
        else:
            print("Ладья не угрожает пешке")
            logging.info("%s ≠ %s или %s ≠ %s" % (k, m, l, n))
            logging.info("Так как ладья не находится на одной вертикали или горизонтали - она не угрожает пешке")
            k_new.append(k)
            k_new.append(m)
            l_new.append(n)
            l_new.append(l)
            print("Клетки чтобы уничтожить пешку со второго хода")


    def Bishop_move(k, l, m, n):  # Проверка для ходов слона
        if abs(k - m) == abs(l - n):
            print("Слон угрожает пешке")
            logging.info("%s = %s " % (abs(k - m), abs(l - n)))
            logging.info("Так как слон находится на одной диагонали - он угрожает пешке")
        else:
            print("Слон не угрожает пешке")
            print("Клетки чтобы уничтожить пешку со второго хода")
            logging.info("%s ≠ %s " % (abs(k - m), abs(l - n)))
            logging.info("Так как слон не находится на одной диагонали - он не угрожает пешке")
            k2 = k3 = k4 = k5 = k
            l2 = l3 = l4 = l5 = l
            while k2 < 8 and l2 < 8:
                k2 += 1
                l2 += 1
                if abs(k2 - m) == abs(l2 - n):
                    k_new.append(k2)
                    l_new.append(l2)
            while k3 < 9 and l3 > 1:
                k3 += 1
                l3 -= 1
                if abs(k3 - m) == abs(l3 - n):
                    k_new.append(k3)
                    l_new.append(l3)
            while k4 > 0 and l4 < 8:
                k4 -= 1
                l4 += 1
                if abs(k4 - m) == abs(l4 - n):
                    k_new.append(k4)
                    l_new.append(l4)
            while k5 > 0 and l5 > 1:
                k5 -= 1
                l5 -= 1
                if abs(k5 - m) == abs(l5 - n):
                    k_new.append(k5)
                    l_new.append(l5)


    def Knight_move(k, l, m, n):  # Проверка для ходов коня
        if ((abs(k - m) == 1) and (abs(l - n) == 2)) or ((abs(k - m) == 2) and (abs(l - n) == 1)):
            print("Конь угрожает пешке")
            logging.info("(%s = 1 и %s = 2) или (%s = 2 и %s = 1)" % (abs(k - m), abs(l - n), abs(k - m), abs(l - n)))
            logging.info("Конь угрожает пешке")
        else:
            print("Конь не угрожает пешке")
            logging.info("(%s ≠ 1 и %s ≠ 2) или (%s ≠ 2 и %s ≠ 1)" % (abs(k - m), abs(l - n), abs(k - m), abs(l - n)))
            logging.info("Конь не угрожает пешке")
            k2 = k
            l2 = l
            k_knight = [2, 1, 1, 2, -1, -2, -2, -1]
            l_knight = [-1, -2, 2, 1, 2, 1, -1, -2]
            for i in range(8):
                k2 += k_knight[i]
                l2 += l_knight[i]
                if ((abs(k2 - m) == 1) and (abs(l2 - n) == 2)) or ((abs(k2 - m) == 2) and (abs(l2 - n) == 1)):
                    if k2 < 8 and k2 > 1 and l2 < 8 and l2 > 1:
                        k_new.append(k2)
                        l_new.append(l2)
                k2 = k
                l2 = l


    # Тело программы
    w = Board()
    check_color(k, l, m, n)
    if chessman_n == 1:
        print(w)
        Queen_move(k, l, m, n)
        for i in range(len(k_new)):
            print(k_new[i], l_new[i])
            w.board[(l_new[i] - 8) * -1][k_new[i] - 1] = '·'
        print(w)
    if chessman_n == 2:
        print(w)
        Rook_move(k, l, m, n)
        for i in range(len(k_new)):
            print(k_new[i], l_new[i])
            w.board[(l_new[i] - 8) * -1][k_new[i] - 1] = '·'
        print(w)
    if chessman_n == 3:
        print(w)
        Bishop_move(k, l, m, n)
        for i in range(len(k_new)):
            print(k_new[i], l_new[i])
            w.board[(l_new[i] - 8) * -1][k_new[i] - 1] = '·'
        print(w)
    if chessman_n == 4:
        print(w)
        Knight_move(k, l, m, n)
        for i in range(len(k_new)):
            print(k_new[i], l_new[i])
            w.board[(l_new[i] - 8) * -1][k_new[i] - 1] = '·'
        print(w)
except ValueError:
    log.exception("Ошибка неверного типа данных!")
    quit("Ошибка! Введено не число! Перезапустите программу!")
