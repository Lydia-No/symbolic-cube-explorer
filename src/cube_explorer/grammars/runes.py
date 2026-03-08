RUNE_OPERATORS = {
    "ᚠ": 0,
    "ᚢ": 1,
    "ᚦ": 2,
}


def apply_rune_symbol(state, symbol):
    if symbol not in RUNE_OPERATORS:
        raise ValueError(f"Unknown rune symbol: {symbol}")

    bit = RUNE_OPERATORS[symbol]
    return state ^ (1 << bit)
