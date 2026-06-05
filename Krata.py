from math import comb

# dane do testów od AI

dane_testowe = {
    "test_1": {
        "nazwa": "Prosta krata 6x6 przez dwa punkty",
        "krata": (6, 6),
        "punkty": [(1, 1), (5, 5)]
    },
    "test_2": {
        "nazwa": "Krata 10x10 przez trzy punkty",
        "krata": (10, 10),
        "punkty": [(2, 3), (5, 5), (8, 8)]
    },
    "test_3": {
        "nazwa": "Mała krata 4x4 bez punktów pośrednich",
        "krata": (4, 4),
        "punkty": []
    },
    "test_4": {
        "nazwa": "Krata 8x5 przez cztery punkty",
        "krata": (8, 5),
        "punkty": [(1, 1), (3, 2), (5, 3), (7, 4)]
    }
}

# opcje
def licz_drogi(x1, y1, x2, y2):
    """Liczba dróg z punktu (x1, y1) do (x2, y2) - tylko prawo lub dół"""
    dx = x2 - x1
    dy = y2 - y1
    if dx < 0 or dy < 0:
        return 0  # nie można się cofać
    return comb(dx + dy, dx)


def policz_ilosc_mozliwych_przejsc_w_kracie_przez_punkty(krata, punkty, verbose=True):
    """
    Liczba możliwych przejść przez kratę przez wszystkie zadane punkty.
    verbose=True -> wypisuje kroki obliczeń
    """
    n, m = krata
    points = [(0, 0)] + sorted(punkty) + [(n - 1, m - 1)]

    if verbose:
        print(f"\nKrata: {krata}")
        print(f"Punkty do przejścia: {sorted(punkty)}")
        print(f"Pełna ścieżka: {' → '.join([str(p) for p in points])}")
        print("\nObliczenia:")

    ilosc = 1
    for i in range(len(points) - 1):
        p1, p2 = points[i], points[i + 1]
        drogi = licz_drogi(p1[0], p1[1], p2[0], p2[1])
        ilosc *= drogi

        if verbose:
            dx = p2[0] - p1[0]
            dy = p2[1] - p1[1]
            print(f"  {p1} → {p2}: C({dx}+{dy},{dx}) = C({dx + dy},{dx}) = {drogi}")

    if verbose:
        print(f"\nWynik: {ilosc} możliwych przejść")

    return ilosc


def wyswietl_menu():
    """UI"""
    print("\n" + "=" * 60)
    print("LICZENIE ŚCIEŻEK NA KRACIE")
    print("=" * 60)
    print("\n1️ -> Uruchom test 1 (6x6, 2 punkty)")
    print("2️ -> Uruchom test 2 (10x10, 3 punkty)")
    print("3️ -> Uruchom test 3 (4x4, bez punktów)")
    print("4️ -> Uruchom test 4 (8x5, 4 punkty)")
    print("5️ -> Uruchom WSZYSTKIE testy")
    print("6️ -> Własne dane (wpisz ręcznie)")
    print("0️ -> Wyjście")
    print("=" * 60)


def uruchom_test(klucz_testu):
    """Uruchamia wybrany test"""
    if klucz_testu not in dane_testowe:
        print("Test nie istnieje!")
        return

    test = dane_testowe[klucz_testu]
    print(f"\n🧪 {test['nazwa']}")
    policz_ilosc_mozliwych_przejsc_w_kracie_przez_punkty(
        test['krata'],
        test['punkty'],
        verbose=True
    )


def wlasne_dane():
    """Wprowadzenie własnych danych"""
    print("\nWprowadź własne dane:")
    try:
        n = int(input("Szerokość kraty (n): "))
        m = int(input("Wysokość kraty (m): "))

        print("Punkty pośrednie (wpisz 'koniec' aby skończyć):")
        punkty = []
        licznik = 1
        while True:
            try:
                dane = input(f"Punkt {licznik} (x,y) lub 'koniec': ").strip().lower()
                if dane == 'koniec':
                    break
                x, y = map(int, dane.split(','))
                punkty.append((x, y))
                licznik += 1
            except ValueError:
                print("Zły format! formaty przewidywany: x,y")

        policz_ilosc_mozliwych_przejsc_w_kracie_przez_punkty(
            (n, m),
            punkty,
            verbose=True
        )
    except ValueError as e:
        print("Zły format albo inny błąd:", e)

if __name__ == '__main__':
    while True:
        wyswietl_menu()
        wybor = input("\n Wybrane: ").strip()

        if wybor == '1':
            uruchom_test('test_1')
        elif wybor == '2':
            uruchom_test('test_2')
        elif wybor == '3':
            uruchom_test('test_3')
        elif wybor == '4':
            uruchom_test('test_4')
        elif wybor == '5':
            print("\nUruchamianie wszystkich testów...")
            for klucz in sorted(dane_testowe.keys()):
                uruchom_test(klucz)
        elif wybor == '6':
            wlasne_dane()
        elif wybor == '0':
            print("\n !Koniec!")
            break
        else:
            print("Błędna opcja!")
