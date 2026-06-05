from itertools import permutations, combinations_with_replacement, product
from collections import Counter

# dane do testów od AI
dane_testowe = {
    "test_1": {
        "nazwa": "Ciąg długości 4 z zbioru {a,b,c,d} bez ograniczeń",
        "elementy": ['a', 'b', 'c', 'd'],
        "dlugosc": 4,
        "warunki": {}
    },
    "test_2": {
        "nazwa": "Ciąg długości 5 z {a,b,c,d}, gdzie c nie może > 2 razy",
        "elementy": ['a', 'b', 'c', 'd'],
        "dlugosc": 5,
        "warunki": {
            "max_count": {'c': 2}  # c może być max 2 razy
        }
    },
    "test_3": {
        "nazwa": "Ciąg długości 6 z {a,b,c,d}, b na indeksach 1 i 3 (0-indexed)",
        "elementy": ['a', 'b', 'c', 'd'],
        "dlugosc": 6,
        "warunki": {
            "fixed_positions": {1: 'b', 3: 'b'}  # b na pozycjach 1 i 3
        }
    },
    "test_4": {
        "nazwa": "Ciąg długości 7 z {a,b,c,d}: lustrzane odbicie (palindrom)",
        "elementy": ['a', 'b', 'c', 'd'],
        "dlugosc": 7,
        "warunki": {
            "palindrom": True  # ciąg musi być symetryczny
        }
    },
    "test_5": {
        "nazwa": "Ciąg długości 5: b min 1 raz, c max 2 razy, d na pozycji 4",
        "elementy": ['a', 'b', 'c', 'd'],
        "dlugosc": 5,
        "warunki": {
            "min_count": {'b': 1},  # b co najmniej 1 raz
            "max_count": {'c': 2},  # c maksymalnie 2 razy
            "fixed_positions": {4: 'd'}  # d na pozycji 4
        }
    }
}

# opcje
def sprawdz_warunki(ciag, warunki):
    if "max_count" in warunki:
        counter = Counter(ciag)
        for elem, max_ile in warunki["max_count"].items():
            if counter[elem] > max_ile:
                return False

    if "min_count" in warunki:
        counter = Counter(ciag)
        for elem, min_ile in warunki["min_count"].items():
            if counter[elem] < min_ile:
                return False

    if "fixed_positions" in warunki:
        for idx, elem in warunki["fixed_positions"].items():
            if ciag[idx] != elem:
                return False

    if warunki.get("palindrom", False):
        if ciag != ciag[::-1]:
            return False
    return True

def generuj_ciagi_z_warunkami(elementy, dlugosc, warunki, limit=None):
    cyjanskie_ciagi = []

    for ciag in product(elementy, repeat=dlugosc):
        if sprawdz_warunki(ciag, warunki):
            cyjanskie_ciagi.append(''.join(ciag))

    if limit:
        cyjanskie_ciagi = cyjanskie_ciagi[:limit]

    return cyjanskie_ciagi

def licz_ciagi_z_warunkami(elementy, dlugosc, warunki):
    count = 0
    for ciag in product(elementy, repeat=dlugosc):
        if sprawdz_warunki(ciag, warunki):
            count += 1
    return count

#UI
def wyswietl_menu():
    print("\n" + "=" * 70)
    print("GENEROWANIE CIĄGÓW Z OGRANICZENIAMI")
    print("=" * 70)
    print("\n1️ -> Test 1: Ciąg bez ograniczeń (4 elem, 4 pozycje)")
    print("2️ -> Test 2: Maksymalnie 2x 'c' (5 pozycji)")
    print("3️ -> Test 3: 'b' na pozycjach 1 i 3 (6 pozycji)")
    print("4️ -> Test 4: Palindrom (7 pozycji)")
    print("5️ -> Test 5: Złożone warunki (5 pozycji)")
    print("6️ -> Własne dane (wpisz ręcznie)")
    print("0️ -> Wyjście")
    print("=" * 70)

def uruchom_test(klucz_testu):
    if klucz_testu not in dane_testowe:
        print("Test nie istnieje!")
        return

    test = dane_testowe[klucz_testu]
    print(f"\n{test['nazwa']}")
    print(f"   Elementy: {test['elementy']}")
    print(f"   Długość ciągu: {test['dlugosc']}")
    print(f"   Warunki: {test['warunki'] if test['warunki'] else 'brak'}")

    ilosc = licz_ciagi_z_warunkami(test['elementy'], test['dlugosc'], test['warunki'])
    print(f"\nLiczba spełniających ciągów: {ilosc}")

    if ilosc > 0:
        ciagi = generuj_ciagi_z_warunkami(test['elementy'], test['dlugosc'], test['warunki'], limit=20)
        print(f"\nPrzykłady (max 20):") # MAX 20
        for i, ciag in enumerate(ciagi, 1):
            print(f"   {i:2d}. {ciag}")
        if ilosc > 20:
            print(f"   ... i jeszcze {ilosc - 20} więcej")


def wlasne_dane():
    print("\nWprowadź własne dane:")
    try:
        elementy_str = input("Elementy (oddzielone przecinkami, np. a,b,c,d): ")
        elementy = [e.strip() for e in elementy_str.split(',')]

        dlugosc = int(input("Długość ciągu: "))

        print("\n Wybierz warunki (wpisz 't' -> tak lub 'n' -> nie):")
        warunki = {}

        if input("Czy zastosować limit maksymalnych powtórzeń? (t/n): ").lower() == 't':
            max_count = {}
            while True:
                elem = input("Element (lub 'koniec'): ").strip()
                if elem.lower() == 'koniec':
                    break
                max_ile = int(input(f"Max powtórzeń {elem}: "))
                max_count[elem] = max_ile
            warunki["max_count"] = max_count

        # Min count
        if input("Czy zastosować minimalną ilość powtórzeń? (t/n): ").lower() == 't':
            min_count = {}
            while True:
                elem = input("Element (lub 'koniec'): ").strip()
                if elem.lower() == 'koniec':
                    break
                min_ile = int(input(f"Min powtórzeń {elem}: "))
                min_count[elem] = min_ile
            warunki["min_count"] = min_count

        # Fixed positions
        if input("Czy ustalić elementy na konkretnych pozycjach? (t/n): ").lower() == 't':
            fixed_pos = {}
            while True:
                pos_str = input("Pozycja (0-indexed) lub 'koniec': ").strip()
                if pos_str.lower() == 'koniec':
                    break
                pos = int(pos_str)
                elem = input(f"Element na pozycji {pos}: ").strip()
                fixed_pos[pos] = elem
            warunki["fixed_positions"] = fixed_pos

        # Palindrom
        if input("Czy ciąg musi być palindromem? (t/n): ").lower() == 't':
            warunki["palindrom"] = True

        # Uruchamienie
        ilosc = licz_ciagi_z_warunkami(elementy, dlugosc, warunki)
        print(f"\n📈 Liczba spełniających ciągów: {ilosc}")

        if ilosc > 0 and ilosc <= 100:
            pokaz = input("Wyświetlić wszystkie ciągi? (t/n): ").lower() == 't'
            if pokaz:
                ciagi = generuj_ciagi_z_warunkami(elementy, dlugosc, warunki)
                for i, ciag in enumerate(ciagi, 1):
                    print(f"   {i:2d}. {ciag}")
        elif ilosc > 100:
            pokaz = input(f"Wiele ciągów ({ilosc}). Wyświetlić pierwsze 50? (t/n): ").lower() == 't'
            if pokaz:
                ciagi = generuj_ciagi_z_warunkami(elementy, dlugosc, warunki, limit=50)
                for i, ciag in enumerate(ciagi, 1):
                    print(f"   {i:2d}. {ciag}")

    except ValueError:
        print("Zły format albo inny błąd:")


# Main  kod wykonywalny
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
            uruchom_test('test_5')
        elif wybor == '6':
            wlasne_dane()
        elif wybor == '0':
            print("\n !Koniec!")
            break
        else:
            print("Błędna opcja!")
