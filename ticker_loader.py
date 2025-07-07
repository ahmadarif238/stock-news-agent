def load_tickers_from_file(filename="tickers.txt"):
    with open(filename, "r") as f:
        return [line.strip().upper() for line in f if line.strip()]
