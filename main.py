

import argparse
from analyzer import analyze_password
from wordlist_gen import generate_wordlist
def export_wordlist(words, filename="wordlist.txt"):
    """
    Write each entry in `words` (an iterable of strings)
    to `filename`, one per line.
    """
    with open(filename, 'w') as f:
        for word in words:
            f.write(word + '\n')

def main():
    parser = argparse.ArgumentParser(
        description="Password Analyzer + Wordlist Generator"
    )
    parser.add_argument("--password", help="Password to analyze")
    parser.add_argument("--name",     help="User's name")
    parser.add_argument("--dob",      help="Date of birth (YYYY-MM-DD)")
    parser.add_argument("--pet",      help="Pet's name")
    parser.add_argument(
        "--extras",
        nargs="*",
        help="Other related words (space separated)"
    )

    args = parser.parse_args()


    if args.password:
        score, warning, suggestions = analyze_password(args.password)
        print(f"Score: {score}/4")
        print(f"Warning: {Warning}")
        print("Suggestions:")
        for s in suggestions:
            print("  -", s)

   
    if args.name and args.pet:
        words = generate_wordlist(
            args.name,
            args.dob,
            args.pet,
            extras=args.extras or []
        )
        export_wordlist(words)        
        print(f"\nWordlist generated: {len(words)} entries → wordlist.txt")

if __name__ == "__main__":
    main()
