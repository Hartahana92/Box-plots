from pathlib import Path

TMP_DIR = Path(__file__).parents[1] / ".tmp"

if __name__ == "__main__":
    print(TMP_DIR.absolute())