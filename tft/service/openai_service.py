import json

from tft.models import match_summoner
from openai import OpenAI
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
client = OpenAI(
  api_key=os.environ["OPEN_AI_API_KEY"],
)

def analyze_performance(puuid):
    # Fetch recent matches for the given player
    recent_matches = match_summoner.objects.filter(puuid=puuid).order_by('-id')[:5]

    if not recent_matches.exists():
        return {'analysis': 'No match data available.'}

    prompt = f"""
    Analyze the following match data for a player in Teamfight Tactics and provide a comprehensive analysis based on the last 20 matches.
    Please limit the analysis within 200 words
    Recent Matches:
    """
    for match in recent_matches:
        prompt += f"""
            Match {match.match_id}:
            - Placement: {match.placement}
            - Gold Left: {match.gold_left}
            - Last Round: {match.last_round}
            - Level: {match.level}
            - Players Eliminated: {match.players_eliminated}
            - Time Eliminated: {match.time_eliminated} seconds
            - Total Damage to Players: {match.total_damage_to_players}
            
            Augments Used:
            {json.dumps(match.augments, indent=2)}
        
            Traits Activated:
            {json.dumps(match.traits, indent=2)}
        
            Units Deployed:
            {json.dumps(match.units, indent=2)}
        
            Please provide an analysis including the following points:
            1. Overall performance evaluation over the last 20 matches.
            2. Patterns or trends in key decisions and their impact on match outcomes.
            3. Consistent strengths and weaknesses observed from the matches.
            4. Recommendations for improvement based on the analysis.
            5. Notable moments or turning points in any of the matches.
        """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    analysis = response.choices[0].message.content.strip()
    # response = "Based on the provided game performance data, here are some insights:\n\n1. **Placement Consistency**:\n    - The player placed in the top 3 in 3 out of the 5 matches, indicating consistent high performance.\n    - Specifically, the placements of 2nd and 3rd in three matches and 1st in one match show strong competitive play.\n\n2. **Round Reached**:\n    - The player consistently reaches the later stages of the game, with rounds 33 or higher in all matches.\n    - The longest match went up to round 42, which resulted in a 1st place finish, suggesting strong end-game performance.\n\n3. **Damage Dealt**:\n    - The damage dealt varies between matches but generally trends higher when placements are better. For example, the highest damage of 232 corresponds with the 1st place finish, whereas lower damage of 86 is associated with a 5th place finish.\n    - Damage dealt in the placements of 2 ranged from 133 to 140.\n\n4. **Resource Management**:\n    - Gold management is varied, with the highest gold left being 39 in the match with a 1st place finish, indicating efficient resource use and perhaps investment strategies.\n    - In other matches, gold left is minimal (0, 1, 1, 3), which may be a result of spending towards the game's end to maintain competitive advantages.\n\n5. **Player Elimination**:\n    - Player elimination performance is inconsistent. There are matches where no players were eliminated (e.g., the 2nd place finish with no eliminations in one match), but also matches with higher eliminations (3 eliminations in another 2nd place finish and 2 in a 3rd place finish).\n    - This suggests that while the player can perform well without focusing on eliminations, there are times when eliminations significantly contribute to their performance.\n\n### Actionable Insights\n\n- **Focus on Damage Output**:\n    - Improvement in damage output could contribute to more consistent top placements. Analyzing strategies from the higher damage/death matches could offer valuable practices to maintain or replicate.\n\n- **Gold Utilization**:\n    - Efficient gold utilization is exemplified in the match with a 1st place finish, where 39 gold was left. Understanding how gold was utilized in that match could help devise strategies for better resource management in other matches.\n\n- **Elimination Strategy**:\n    - Balancing between elimination-focused and survival-centric strategies could potentially enhance placement consistency. The player should determine situational benefits of aggressive versus conservative approaches, depending on game dynamics.\n\nBy focusing on these areas, the player could potentially refine their gameplay to achieve more frequent high placements and a stronger overall performance."
    # analysis = response.strip()
    return {'analysis': analysis}
