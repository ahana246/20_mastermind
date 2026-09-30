def feedback(code, guess):
    """
    Returns:
        exact: Number of symbols in the correct position.
        partial: Number of correct symbols in the wrong position.

    Each occurrence in the code can contribute to the feedback
    at most once.
    """

    exact = 0

    # Track which positions have already been matched.
    code_used = [False] * len(code)
    guess_used = [False] * len(guess)

    # Resolve exact matches first.
    for i in range(len(code)):
        if code[i] == guess[i]:
            exact += 1
            code_used[i] = True
            guess_used[i] = True

    # Find partial matches among unmatched symbols.
    partial = 0

    for i in range(len(guess)):
        if guess_used[i]:
            continue

        for j in range(len(code)):
            if code_used[j]:
                continue

            if guess[i] == code[j]:
                partial += 1
                code_used[j] = True
                guess_used[i] = True
                break

    return exact, partial