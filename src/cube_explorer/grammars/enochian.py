ENOCHIAN_OPERATORS = {
    "Pa": 0,
    "Veh": 1,
    "Ged": 2,
}


def apply_enochian_symbol(state, symbol):
    if symbol not in ENOCHIAN_OPERATORS:
        raise ValueError(f"Unknown Enochian symbol: {symbol}")

    bit = ENOCHIAN_OPERATORS[symbol]
    return state ^ (1 << bit)
