
def calculate_rating(rating_winner, rating_loser):
    k_factor = 32  # You can adjust this value based on your needs

    expected_winner = 1 / (1 + 10 ** ((rating_loser - rating_winner) / 400))
    expected_loser = 1 / (1 + 10 ** ((rating_winner - rating_loser) / 400))

    new_rating_winner = rating_winner + k_factor * (1 - expected_winner)
    new_rating_loser = rating_loser + k_factor * (0 - expected_loser)

    return new_rating_winner, new_rating_loser


def update_ratings(players, match_history, winner, loser):
    winner_rating = players[winner]["rating"]
    loser_rating = players[loser]["rating"]

    new_winner_rating, new_loser_rating = calculate_rating(winner_rating, loser_rating)

    players[winner]["rating"] = new_winner_rating
    players[loser]["rating"] = new_loser_rating

    players[winner]["games_played"] += 1
    players[loser]["games_played"] += 1

    match_history.append({"winner": winner, "loser": loser})


def print_ratings(players):
    sorted_players = sorted(players.items(), key=lambda x: x[1]["rating"], reverse=True)
    for player, data in sorted_players:
        print(
            f"{player}: Rating - {data['rating']}, Games Played - {data['games_played']}"
        )


def print_match_history(match_history):
    for idx, match in enumerate(match_history, start=1):
        print(f"Match {idx}: {match['winner']} vs {match['loser']}")
        
        
def process_match_history(players, match_history):
    for match in match_history:
        winner = match['winner']
        loser = match['loser']
        update_ratings(players, match_history, winner, loser)
        
        

def remove_specific_matchup(match_history, player1, player2):
    return [
        match for match in match_history
        if not ((match['winner'] == player1 and match['loser'] == player2) or
                (match['winner'] == player2 and match['loser'] == player1))
    ]

        
        
def simulate_matches(players, remaining_matches):
    scenarios = []
    initial_ratings = {player: players[player]["rating"] for player in players}
    initial_games_played = {player: players[player]["games_played"] for player in players}

    def generate_scenarios(matches, current_scenario):
        if not matches:
            scenarios.append(current_scenario.copy())
            return

        match = matches[0]
        for outcome in [(match[0], match[1]), (match[1], match[0])]:
            update_ratings(players, [], outcome[0], outcome[1])
            current_scenario.append(outcome)
            generate_scenarios(matches[1:], current_scenario)
            current_scenario.pop()

            # Reset players' ratings and games played after each iteration
            for player in players:
                players[player]["rating"] = initial_ratings[player]
                players[player]["games_played"] = initial_games_played[player]

    generate_scenarios(remaining_matches, [])
    return scenarios

def highest_rating(players):
    # Function to get the player with the highest rating
    highest_rating_player = max(players, key=lambda x: players[x]['rating'])
    return highest_rating_player



def simulate_match_ww(player_a, player_b, winrates, default_winrate = 0.5):
    """
    Simulate a match between player_a and player_b using predefined winrates.
    If no winrate is specified, use the default winrate of 0.5 (50% chance for either player).
    """
    # Get the winrate for player_a against player_b (or default to 0.5 if not specified)
    winrate_a = winrates.get((player_a, player_b), default_winrate)
    
    # Simulate the match based on the winrate
    if random.random() < winrate_a:
        return player_a  # Player A wins
    else:
        return player_b  # Player B wins



def simulate_match_with_winrates(player_a, player_b, winrates):
    import random
    """
    Simulate a match between player_a and player_b using predefined winrates.
    Use random chance to determine the winner based on the winrate.
    """
    # Get the winrate for player_a beating player_b, default to 50% if not specified
    winrate = winrates.get((player_a, player_b), 0.5)
    
    # Generate a random number between 0 and 1, and compare it to the winrate
    if random.random() < winrate:
        return player_a  # Player A wins
    else:
        return player_b  # Player B wins

    
