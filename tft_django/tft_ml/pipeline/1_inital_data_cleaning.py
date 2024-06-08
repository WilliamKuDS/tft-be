import pandas as pd

# Load the dataset using pickle, to preserve the dataset types
df = pd.read_pickle('data/tft_games/tft_games_pickled.csv')

# Convert length to length_seconds
def convert_length_to_seconds(length):
    mins, secs = map(int, length.split(':'))
    return mins * 60 + secs

df['length'] = [convert_length_to_seconds(item) for item in df['length']]

# Convert stage-round to rounds
def convert_rounds(round):
    stage, stage_round = map(int, round.split('-'))
    # If its stage one, there are no need to calculate and return the current rounds
    if stage == 1:
        return stage_round
    # Else, convert stage to rounds using this formula:
    # If S>1: T=3+7×(S−2)+R, where S is stage, T is total rounds, and R is rounds
    return 3 + (stage - 2) * 7 + stage_round

df['round'] = [convert_rounds(item) for item in df['round']]

# Flatten the 'units' column
def flatten_units(data):
    return {f'unit_{i + 1}_{key}': val for i, unit in enumerate(data) for key, val in {
        'name': unit['name'],
        'tier': unit['star'],
        'item_1': unit['items'][0] if len(unit['items']) > 0 else None,
        'item_2': unit['items'][1] if len(unit['items']) > 1 else None,
        'item_3': unit['items'][2] if len(unit['items']) > 2 else None
    }.items()}
units_flattened = pd.DataFrame([flatten_units(item) for item in df['units']])

# Flatten the 'traits' column
traits_flattened = pd.DataFrame([
    {f'trait_{i + 1}_{key}': val for i, trait in enumerate(traits) for key, val in trait.items()}
    for traits in df['traits']
])

# Flatten the 'augments' column
augments_flattened = pd.DataFrame([
    {f'augment_{i + 1}': augment for i, augment in enumerate(augments)}
    for augments in df['augments']
])

# Combine the flattened columns with the original dataframe (excluding the original columns being flattened)
df_flattened = pd.concat(
    [df.drop(columns=['traits', 'augments']),  # We're keeping units column for easier time in data_preprocessing
     augments_flattened, traits_flattened, units_flattened], axis=1)

# Save the final flattened dataframe to a CSV file
df_flattened.to_csv('data/tft_games/tft_games_initial_clean.csv', index=False)
df_flattened.to_pickle('data/tft_games/tft_games_initial_clean_pickle.csv')