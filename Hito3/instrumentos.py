# instrumentos.py

INSTRUMENTOS_VALIDOS = {
    "Piano",
    "Electric piano",
    "Organ",
    "Synthesizer",
    "Guitar",
    "Electric guitar",
    "Bass guitar",
    "Acoustic guitar",
    "Violin, fiddle",
    "Cello",
    "Double bass",
    "Harp",
    "Trumpet",
    "Trombone",
    "French horn",
    "Tuba",
    "Saxophone",
    "Flute",
    "Clarinet",
    "Drum kit",
    "Drum",
    "Snare drum",
    "Timpani",
    "Hi-hat",
    "Tambourine",
    "Maraca",
    "Xylophone",
    "Steel drum",
    "Gong",
    "Accordion",
    "Banjo",
    "Mandolin",
    "Ukulele",
    # ...puedes agregar más aquí si lo deseas
}

def es_instrumento(nombre):
    return nombre in INSTRUMENTOS_VALIDOS
