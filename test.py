def trojclenka(x1, y1, x3):
    # Koeficient přímé úměrnosti
    a = y1 / x1

    # Dopočítáme hodnotu y3
    y3 = a * x3

    # Vrátíme dopočítanou hodnotu y3
    return y3

# Příklad použití
x1, y1 = 15, 3
x3 = 29

vysledek = trojclenka(x1, y1, x3)
print(f'Hodnota pro x3={x3}: {vysledek}')
