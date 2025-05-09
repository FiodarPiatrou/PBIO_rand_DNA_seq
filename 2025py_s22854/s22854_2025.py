import random
import os
#Cel programu: wygenerowanie losowej sekwencji nukleotydów i zapis tej sekwencji w raz z statystykami do pliku fasta,
#dodatko jest jeszcze wstawiane imie podane pzez użytkownika
#Kontekst: Bioinformatyka - nukleotydy sekwencji DNA.

def generate_dna_sequence(length, name):
    #Defenicja naszej listy możliwych do wyboru nukleotydów
    nucleotides = ['A', 'C', 'G', 'T']
    #generowanie sekwencji za pomocą list comprehension
    sequence = [random.choice(nucleotides) for _ in range(length)]

    # Jeśli imie było podane
    if name:
        #Losowa pozycja w sekwencji
        insert_pos = random.randint(0, len(sequence))
        #Wklejanie do tej losowej pozycji imia za pomocą slicingu list
        sequence[insert_pos:insert_pos] = list(name)
        #ORIGINAL:
    #return ''.join(sequence)
        #MODIFIED(musimy zwrócić posycję żeby zadziałał kod w calculate_statystics
        #Zwrót sekwencji w postaci string oraz pozycji dodania imienia
        return ''.join(sequence), insert_pos
    # Zwrót sekwencji w postaci string oraz -1 który oznacza że imienia nie było
    return ''.join(sequence) ,-1

#metoda wyliczenia statystyk
def calculate_statistics(sequence, name, insert_pos):
    #Tworzymy kopie sekwencji
    clean_sequence = sequence
    #ORIGINAL:
    # if name:
    #     clean_sequence = sequence.replace(name, '')
    #MODIFIED(nie uwzględnia przypadku, gdy imie jest podobne do sekwencji nukleotydów):
    #Sprawdzamy że imie jest i jest pozycja imienia
    if name and insert_pos != -1:
        #usuwamy imie ze wstawianej pozycjy korzystając z list slicing
        clean_sequence = sequence[:insert_pos] + sequence[insert_pos + len(name):]
    #Liczymy ilość wsystkich nukleotydów w sekwencji czystej
    total = len(clean_sequence)
    #Słownik dla statystyk
    stats = {
        'A': clean_sequence.count('A') / total * 100,
        'C': clean_sequence.count('C') / total * 100,
        'G': clean_sequence.count('G') / total * 100,
        'T': clean_sequence.count('T') / total * 100,
    }
    #Liczymy ilość C i G wzgłedem A i G
    cg = stats['C'] + stats['G']
    #ORIGINAL:
    #at = stats['A'] + stats['T']
    #MODIFIED(nie jest potrzebna bo i tak już policzyliśmy procent cg wzgledem innych):
    #Dodajemy do słownika statystykę %CG
    stats['CG_ratio'] = cg
    #Zwrót słownika statystyk
    return stats

#Funkcja main
def main():
    #Nagłowek
    print("Generator sekwencji DNA w formacie FASTA")

    # Pobierz dane od użytkownika
    try:
        #Dane o długości
        length = int(input("Podaj długość sekwencji: "))
        #Jeśli długość <=0 to podnosimy błąd
        if length <= 0:
            raise ValueError("Długość musi być dodatnia")
    #Łapimy błąd i wypisujemy sformatowanym tekstem
    except ValueError as e:
        print(f"Błąd: {e}")
        return
    #Pobieramy id Sekwencji
    seq_id = input("Podaj ID sekwencji: ").strip()
    #Jeśli nie ma id to wyświetlamy komunikat
    if not seq_id:
        print("Błąd: ID sekwencji nie może być puste")
        return

    description = input("Podaj opis sekwencji: ").strip()
    name = input("Podaj imię: ").strip()

    # Generuj sekwencję
    #ORIGINAL:
    #sequence = generate_dna_sequence(length, name)
    #stats = calculate_statistics(sequence, name)
    #MODIFIED(musimy pobrać oba argumenty naraz)
    # Generuj sekwencję
    sequence, insert_pos = generate_dna_sequence(length, name)
    # Obliczenie statystyki
    stats = calculate_statistics(sequence, name, insert_pos)

    # Zapis do pliku FASTA
    filename = f"{seq_id}.fasta"
    with open(filename, 'w') as f:
        f.write(f">{seq_id} {description}\n")
        f.write(sequence + "\n")

    print(f"\nSekwencja została zapisana do pliku {filename}")
    print("Statystyki sekwencji:")
    print(f"A: {stats['A']:.1f}%")
    print(f"C: {stats['C']:.1f}%")
    print(f"G: {stats['G']:.1f}%")
    print(f"T: {stats['T']:.1f}%")
    print(f"%CG: {stats['CG_ratio']:.1f}")


if __name__ == "__main__":
    main()