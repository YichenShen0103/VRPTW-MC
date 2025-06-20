from utils.DataLoader import DataLoader
from src.solve import solve

DATA_ROOT: str = "data/"


def main() -> None:
    solve(dataLoader=DataLoader(DATA_ROOT))


if __name__ == "__main__":
    main()
