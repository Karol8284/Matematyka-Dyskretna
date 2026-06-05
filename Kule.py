# dane do testów od AI
dane_testowe = {
    "test_1": {
        "nazwa": "3 kule w 4 szufladkach, bez ograniczeń",
        "kolory_kul": ['A', 'B', 'C'],  # rozróżnialne KOLORY (opcjonalne)
        "szufladki": 4,
        "kule": 3,
        "warunki": {}
    },
    "test_2": {
        "nazwa": "5 kul w 3 szufladkach, w każdej max 2 kule",
        "kolory_kul": ['X', 'Y', 'Z', 'R', 'G'],
        "szufladki": 3,
        "kule": 5,
        "warunki": {"max_per_bin": 2}
    },
    "test_3": {
        "nazwa": "4 białe kule w 4 szufladkach, min 1 kula w każdej",
        "kolory_kul": ['W'] * 4,
        "szufladki": 4,
        "kule": 4,
        "warunki": {"min_per_bin": 1}
    },
    "test_4": {
        "nazwa": "6 kul (2 kolory) w 3 szufladkach, nie więcej jak 4 w 1 szufladce",
        "kolory_kul": ['A', 'A', 'B', 'B', 'A', 'B'],
        "szufladki": 3,
        "kule": 6,
        "warunki": {"max_per_bin": 4}
    }
}
# opcje

def rozklad_bez_ograniczen(kule, szufladki):
    from math import comb
    return comb(kule + szufladki - 1, szufladki - 1)


def generuj_rozkłady(kule, szufladki, warunki, limit=30):
    res = []

    def gen_rec(start, sofar, left):
        if len(sofar) == szufladki:
            if left == 0:
                if sprawdz_warunki(sofar, warunki):
                    res.append(sofar[:])
            return
        minv = warunki.get("min_per_bin", 0)
        maxv = warunki.get("max_per_bin", kule)
        for i in range(minv, min(maxv, left) + 1):
            sofar.append(i)
            gen_rec(start, sofar, left - i)
            sofar.pop()

    gen_rec(0, [], kule)
    if limit:
        res = res[:limit]
    return res


def sprawdz_warunki(rozkład, warunki):
    minv = warunki.get('min_per_bin', 0)
    maxv = warunki.get('max_per_bin', max(rozkład) + 1)
    for x in rozkład:
        if x < minv or x > maxv:
            return False
    return True


def liczba_rozkładów(kule, szufladki, warunki):
    if not warunki:
        return rozklad_bez_ograniczen(kule, szufladki)
    return len(generuj_rozkłady(kule, szufladki, warunki, limit=None))


def wyswietl_rozkład(rozkład):
    return ' | '.join(str(i) for i in rozkład)


# UI

def wyswietl_menu():
    print("\n" + "=" * 60)
    print("Rozkład KUL w SZUFLADKACH z ograniczeniami")
    print("=" * 60)
    print("1️ -> Test 1: 3 kule w 4 szufladkach, bez ograniczeń")
    print("2️ -> Test 2: 5 kul, 3 szufladki, max 2 kule w 1")
    print("3️ -> Test 3: 4 białe kule, 4 szufladki, min 1 kula na szufladkę")
    print("4️ -> Test 4: 6 kul (2 kolory), 3 szufladki, max 4 kule w 1")
    print("5️ -> Własne dane")
    print("0️ -> Wyjście")
    print("=" * 60)


def uruchom_test(nr):
    klucz = f'test_{nr}'
    if klucz not in dane_testowe:
        print("Test nie istnieje!")
        return
    test = dane_testowe[klucz]
    print(f"\n🧪 {test['nazwa']}")
    print(f"Kule: {test['kule']}  |  Liczba szufladek: {test['szufladki']}")
    if test['warunki']:
        print(f" Warunki: {test['warunki']}")
    else:
        print(" Brak warunków ograniczających")

    ile = liczba_rozkładów(test['kule'], test['szufladki'], test['warunki'])
    print(f"\nLiczba możliwych rozkładów: {ile}")
    przykłady = generuj_rozkłady(test['kule'], test['szufladki'], test['warunki'], limit=20)
    if przykłady:
        print("\nPrzykładowe rozkłady:")
        for i, r in enumerate(przykłady, 1):
            print(f"  {i:2d}. [{wyswietl_rozkład(r)}]")
        if len(przykłady) == 20 and ile > 20:
            print(f"  ...i jeszcze {ile - 20} więcej")


def wlasne_dane():
    print("\n Wprowadzanie własnych danych:")
    try:
        kule = int(input("Ile kul? "))
        szufladki = int(input("Ile szufladek? "))
        warunki = {}
        if input("Ograniczyć minimalną liczbę kul w szufladce? (t/n): ").lower() == 't':
            warunki['min_per_bin'] = int(input("min: "))
        if input("Ograniczyć maksymalną liczbę kul w szufladce? (t/n): ").lower() == 't':
            warunki['max_per_bin'] = int(input("max: "))

        ile = liczba_rozkładów(kule, szufladki, warunki)
        print(f"\nLiczba możliwych rozkładów: {ile}")
        if ile <= 50:
            zrob = True
        else:
            zrob = input(f"Dużo wyników ({ile}), czy pokazać tylko 30 pierwszych? (t/n): ").lower() == 't'
        if zrob:
            przykłady = generuj_rozkłady(kule, szufladki, warunki, limit=30)
            for i, r in enumerate(przykłady, 1):
                print(f"  {i:2d}. [{wyswietl_rozkład(r)}]")
    except Exception as e:
        print("Zły format albo inny błąd:", e)


# Main  kod wykonywalny

if __name__ == "__main__":
    while True:
        wyswietl_menu()
        wybor = input("\n Wybrane: ").strip()
        if wybor in "1234":
            uruchom_test(int(wybor))
        elif wybor == "5":
            wlasne_dane()
        elif wybor == "0":
            print("\n !Koniec!")
            break
        else:
            print("Błędna opcja!")
