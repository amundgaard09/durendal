
import random
from awpc.src.types.color_dtypes import xColorText as color_text

# Funksjon for å gjøre om tall til superscript
def til_superscript(tall):
    superscript_map = {
        "0": "⁰", 
        "1": "¹", 
        "2": "²", 
        "3": "³",
        "4": "⁴", 
        "5": "⁵", 
        "6": "⁶",
        "7": "⁷", 
        "8": "⁸", 
        "9": "⁹"
    }
    return "".join(superscript_map[siffer] for siffer in str(tall))

# Lager liste med alle oppgaver
alle_oppgaver = []

# Lager alle oppgaver
for i in range(2, 11):
    alle_oppgaver.append((2, i))
for i in range(2, 7):
    alle_oppgaver.append((3, i))
for i in range(2, 6):
    alle_oppgaver.append((4, i))
for i in range(2, 5):
    alle_oppgaver.append((5, i))
for i in range(2, 5):
    alle_oppgaver.append((6, i))
for i in range(2, 4):
    alle_oppgaver.append((7, i))
for i in range(2, 4):
    alle_oppgaver.append((8, i))
for i in range(2, 4):
    alle_oppgaver.append((9, i))

# Nye oppgaver: 11² t/m 20²
for i in range(11, 21):
    alle_oppgaver.append((i, 2))

# Aktive oppgaver (de som fortsatt kan bli spurt)
aktive_oppgaver = alle_oppgaver[:]

# Teller for feil per oppgave
feil_teller = {oppgave: 0 for oppgave in alle_oppgaver}

riktige_paa_rad = 0
forrige_oppgave = None

print("Start øvelsen! Skriv svaret på potensen.\n")

while True:
    # Bygg vektet liste kun av aktive oppgaver
    vektet_liste = []

    for oppg in aktive_oppgaver:
        feil = feil_teller[oppg]

        # Vekting: feil gir høyere sjanse
        vekt = 1 + feil * 3
        vektet_liste.extend([oppg] * vekt)

    if not vektet_liste:
        print("Ingen flere oppgaver tilgjengelig.")
        break

    # Velg oppgave (ikke samme som forrige)
    while True:
        base, eksponent = random.choice(vektet_liste)
        if (base, eksponent) != forrige_oppgave:
            break

    riktig_svar = base ** eksponent
    eksponent_sup = til_superscript(eksponent)

    try:
        svar = int(input(f"Hva er {base}{eksponent_sup}? "))
    except ValueError:
        print("Ugyldig input. Vennligst skriv et helt tall.\n")
        continue

    if svar == riktig_svar:
        riktige_paa_rad += 1
        print(f"{color_text('Riktig!', 'green')} Antall riktige på rad: {riktige_paa_rad}\n")

        # Fjern oppgaven helt etter riktig svar
        aktive_oppgaver.remove((base, eksponent))

    else:
        print(f"{color_text('Feil.', 'red')} Riktig svar er {riktig_svar}.")
        riktige_paa_rad -= 2
        if riktige_paa_rad < 0:
            riktige_paa_rad = 0
        print(f"Ny teller: {riktige_paa_rad}\n")

        feil_teller[(base, eksponent)] += 1

        # Fjern hvis maks feil nådd
        if feil_teller[(base, eksponent)] >= 2:
            aktive_oppgaver.remove((base, eksponent))

    forrige_oppgave = (base, eksponent)

    if riktige_paa_rad >= 25:
        print(f"{color_text('Gratulerer! Du har oppnådd 25 riktige!', 'gold')}")
        break