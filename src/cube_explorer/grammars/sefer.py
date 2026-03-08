MOTHER_OPERATORS = {
    "א": 0,  # Aleph
    "מ": 1,  # Mem
    "ש": 2,  # Shin
}


def apply_sefer_symbol(state, symbol):
    if symbol not in MOTHER_OPERATORS:
        raise ValueError(f"Unknown Sefer symbol: {symbol}")

    bit = MOTHER_OPERATORS[symbol]
    return state ^ (1 << bit)
