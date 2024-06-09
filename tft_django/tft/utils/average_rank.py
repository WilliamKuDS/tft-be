def rank_to_value(rank):
    """
    Convert rank to a numerical value.
    """
    tier, division = rank.split(' ')
    tier_values = {
        'Iron': 0, 'Bronze': 4, 'Silver': 8, 'Gold': 12,
        'Platinum': 16, 'Emerald': 20, 'Diamond': 24,
        'Master': 28, 'Grandmaster': 29, 'Challenger': 30
    }
    division_values = {'IV': 0, 'III': 1, 'II': 2, 'I': 3}

    return tier_values[tier] + (division_values[division] if tier in division_values else 0)


def value_to_rank(value):
    """
    Convert a numerical value back to a rank.
    """
    tiers = [
        'Iron', 'Bronze', 'Silver', 'Gold',
        'Platinum', 'Emerald', 'Diamond',
        'Master', 'Grandmaster', 'Challenger'
    ]
    if value >= 28:
        return tiers[value - 28 + 7]  # For Master, Grandmaster, Challenger
    else:
        tier_index = value // 4
        division_index = value % 4
        divisions = ['IV', 'III', 'II', 'I']
        return f"{tiers[tier_index]} {divisions[division_index]}"


def average_rank(ranks):
    """
    Calculate the average rank from a list of ranks.
    """
    total_value = sum(rank_to_value(rank) for rank in ranks)
    average_value = total_value // len(ranks)
    return value_to_rank(average_value)
