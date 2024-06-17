import json

from tft.models import match_summoner, patch
from openai import OpenAI
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
client = OpenAI(
  api_key=os.environ["OPEN_AI_API_KEY"],
)

def analyzePerformance(puuid):
    # Fetch recent matches for the given player
    recent_matches = match_summoner.objects.filter(puuid=puuid).order_by('-match_id__game_creation')[:5]

    if not recent_matches.exists():
        return {'analysis': 'No match data available.'}

    augment_keys = ['display_name']
    trait_keys = ['display_name', 'num_units']
    unit_keys = ['display_name', 'cost', 'tier', 'items']

    prompt = f"""
    In 250 words or less,
    Analyze my last {len(recent_matches)} Teamfight Tactics matches and provide a detailed overall analysis.
    Include comparisons with other players in the same matches

    Matches:
    """
    for match in recent_matches:
        prompt += f"""
        Match {match.match_id}:
        
        - Placement: {match.placement}
        - Last Round: {match.last_round}
        - Level: {match.level}
        - Players Eliminated: {match.players_eliminated}
        - Time Eliminated: {match.time_eliminated}s
        - Damage to Players: {match.total_damage_to_players}
        - Augments: {[{key: d.get(key) for key in augment_keys} for d in match.augments]}
        - Traits: {[{key: d.get(key) for key in trait_keys} for d in match.traits]}
        - Units: {[
            {key: (d.get(key) if key != 'items' else [item['display_name'] for item in d.get(key, [])])
             for key in unit_keys}
            for d in match.units
        ]}
        
        """
    prompt += """
    Please provide an analysis including but not limited to the following points:
    Overall performance evaluation over the last 20 matches,
    Patterns or trends in key decisions and their impact on match outcomes,
    Consistent strengths and weaknesses observed from the matches,
    Comparisons with other players' performance in the same matches,
    Recommendations for improvement based on the analysis, and
    Notable moments or turning points in any of the matches.
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        # model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a Teamfight Tactics coach, helping a player improve and get better at the game"},
            {"role": "user", "content": prompt}
        ]
    )
    analysis = response.choices[0].message.content.strip()
    # response = "Based on the provided game performance data, here are some insights:\n\n1. **Placement Consistency**:\n    - The player placed in the top 3 in 3 out of the 5 matches, indicating consistent high performance.\n    - Specifically, the placements of 2nd and 3rd in three matches and 1st in one match show strong competitive play.\n\n2. **Round Reached**:\n    - The player consistently reaches the later stages of the game, with rounds 33 or higher in all matches.\n    - The longest match went up to round 42, which resulted in a 1st place finish, suggesting strong end-game performance.\n\n3. **Damage Dealt**:\n    - The damage dealt varies between matches but generally trends higher when placements are better. For example, the highest damage of 232 corresponds with the 1st place finish, whereas lower damage of 86 is associated with a 5th place finish.\n    - Damage dealt in the placements of 2 ranged from 133 to 140.\n\n4. **Resource Management**:\n    - Gold management is varied, with the highest gold left being 39 in the match with a 1st place finish, indicating efficient resource use and perhaps investment strategies.\n    - In other matches, gold left is minimal (0, 1, 1, 3), which may be a result of spending towards the game's end to maintain competitive advantages.\n\n5. **Player Elimination**:\n    - Player elimination performance is inconsistent. There are matches where no players were eliminated (e.g., the 2nd place finish with no eliminations in one match), but also matches with higher eliminations (3 eliminations in another 2nd place finish and 2 in a 3rd place finish).\n    - This suggests that while the player can perform well without focusing on eliminations, there are times when eliminations significantly contribute to their performance.\n\n### Actionable Insights\n\n- **Focus on Damage Output**:\n    - Improvement in damage output could contribute to more consistent top placements. Analyzing strategies from the higher damage/death matches could offer valuable practices to maintain or replicate.\n\n- **Gold Utilization**:\n    - Efficient gold utilization is exemplified in the match with a 1st place finish, where 39 gold was left. Understanding how gold was utilized in that match could help devise strategies for better resource management in other matches.\n\n- **Elimination Strategy**:\n    - Balancing between elimination-focused and survival-centric strategies could potentially enhance placement consistency. The player should determine situational benefits of aggressive versus conservative approaches, depending on game dynamics.\n\nBy focusing on these areas, the player could potentially refine their gameplay to achieve more frequent high placements and a stronger overall performance."
    # analysis = response.strip()
    return {'analysis': analysis}


def matchRecommendation(puuid):
    # Fetch recent matches for the given player
    latest_patch = patch.objects.filter(date_end__isnull=True).first()
    recent_matches_latest_patch = match_summoner.objects.filter(puuid=puuid, match_id__patch=latest_patch.patch_id).order_by('-match_id__game_creation')[:5]

    if not recent_matches_latest_patch.exists():
        recent_matches_latest_patch = match_summoner.objects.filter(match_id__patch=latest_patch.patch_id).order_by('-match_id__game_creation')[:9]
        augment_keys = ['display_name']
        trait_keys = ['display_name', 'num_units']
        unit_keys = ['display_name', 'cost', 'tier', 'items']

        prompt = f"""
        Recommend one composition consisting of units a player should try out in their next match that could give them a placement of fourth or higher.
        You could also suggested item builds for key units, and/or
        any specific augments or traits to prioritize.
        Format and organize the response so it is easy to read and understand.
        
        Utilize the following match data to help understand the meta:
        
        """
        for match in recent_matches_latest_patch:
            prompt += f"""
            Match {match.match_id}:
            """
            participant_match_data = match_summoner.objects.filter(match_id=match.match_id)
            for other_players in participant_match_data:
                if other_players.puuid != match.puuid:
                    prompt += f"""
                    - Player PUUID: {other_players.puuid}
                    - Placement: {other_players.placement}
                    - Last Round: {other_players.last_round}
                    - Level: {other_players.level}
                    - Players Eliminated: {other_players.players_eliminated}
                    - Time Eliminated: {other_players.time_eliminated}s
                    - Damage to Players: {other_players.total_damage_to_players}
                    - Augments: {[{key: d.get(key) for key in augment_keys} for d in other_players.augments]}
                    - Traits: {[{key: d.get(key) for key in trait_keys} for d in other_players.traits]}
                    - Units: {[
                        {key: (d.get(key) if key != 'items' else [item['display_name'] for item in d.get(key, [])])
                         for key in unit_keys}
                        for d in other_players.units
                    ]}

                    """
        content = "You are a Teamfight Tactics analyst that is explaining the meta to another player"
        return openAIGPT4o(prompt, content)

    else:
        augment_keys = ['display_name']
        trait_keys = ['display_name', 'num_units']
        unit_keys = ['display_name', 'cost', 'tier', 'items']

        prompt = f"""
        Analyze the following match data for a player in Teamfight Tactics and provide strategy suggestions for their next matches. 
        Suggest playstyles and/or compositions that could improve their performance based on the analysis of their last {len(latest_patch)} matches.
    
        Match Details:
        """
        for match in recent_matches_latest_patch:
            prompt += f"""
            Match {match.match_id}:
            
            - Player PUUID: {match.puuid}
            - Placement: {match.placement}
            - Last Round: {match.last_round}
            - Level: {match.level}
            - Players Eliminated: {match.players_eliminated}
            - Time Eliminated: {match.time_eliminated}s
            - Damage to Players: {match.total_damage_to_players}
            - Augments: {[{key: d.get(key) for key in augment_keys} for d in match.augments]}
            - Traits: {[{key: d.get(key) for key in trait_keys} for d in match.traits]}
            - Units: {[
                {key: (d.get(key) if key != 'items' else [item['display_name'] for item in d.get(key, [])])
                 for key in unit_keys}
                for d in match.units
            ]}
    
            """
            participant_match_data = match_summoner.objects.filter(match_id=match.match_id)
            for other_players in participant_match_data:
                if other_players.puuid != match.puuid:
                    prompt += f"""
                    - Player PUUID: {other_players.puuid}
                    - Placement: {other_players.placement}
                    - Last Round: {other_players.last_round}
                    - Level: {other_players.level}
                    - Players Eliminated: {other_players.players_eliminated}
                    - Time Eliminated: {other_players.time_eliminated}s
                    - Damage to Players: {other_players.total_damage_to_players}
                    - Augments: {[{key: d.get(key) for key in augment_keys} for d in other_players.augments]}
                    - Traits: {[{key: d.get(key) for key in trait_keys} for d in other_players.traits]}
                    - Units: {[
                        {key: (d.get(key) if key != 'items' else [item['display_name'] for item in d.get(key, [])])
                         for key in unit_keys}
                        for d in other_players.units
                    ]}
    
                    """
        prompt += """
        Based on this data, please provide strategy suggestions including but not limited to the following points:
        1. Recommended playstyles for the next matches.
        2. Optimal team compositions to try out.
        3. Suggested item builds for key units.
        4. Positioning strategies to improve performance.
        5. Any specific augments or traits to prioritize.
        6. General tips and tricks based on observed patterns.
    
        """
        content = "You are a Teamfight Tactics coach, helping a player improve and get better at the game"
        return openAIGPT4o(prompt, content)

def openAIGPT4o(prompt, content):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system",
             "content": content},
            {"role": "user", "content": prompt}
        ]
    )
    analysis = response.choices[0].message.content.strip()
    return {'analysis': analysis}

def openAIGPT3T(prompt, content):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": content},
            {"role": "user", "content": prompt}
        ]
    )
    analysis = response.choices[0].message.content.strip()
    return {'analysis': analysis}

