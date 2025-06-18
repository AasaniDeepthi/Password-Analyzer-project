import itertools
def export_wordlist(words, filename="wordlist.txt"):
    with open(filename, 'w') as f:
        for word in words:
            f.write(word + '\n')

def leetspeak(word):
    replacements = {'a': '4', 'e': '3', 'i': '1', 'o': '0', 's': '$'}
    return ''.join(replacements.get(c.lower(), c) for c in word)

def generate_wordlist(name, dob, pet, extras=[]):
    parts = [name.lower(), pet.lower()]
    if dob:
        year = dob.split('-')[0]
        parts.append(year)
    combos = set()

    for part in parts + extras:
        combos.update([part, part + '123', part + '!', leetspeak(part)])
        if dob:
            combos.add(part + year)
    
    return sorted(combos)
