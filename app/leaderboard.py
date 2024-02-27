from kaggle import KaggleApi

# Authentication
# NOTE: You need to have a Kaggle account and a Kaggle API token to use this code.
# read the laggle API documentation for more information on how to setup your API token through the following link:
# https://github.com/Kaggle/kaggle-api
api = KaggleApi()
api.authenticate()


def fetch_competition_leaderboard(competition: str):
    """
    Fetch the leaderboard data of a single competition.
    """
    results = api.competition_leaderboard_view(competition=competition)
    result_fields = ["teamId", "teamName", "submissionDate", "score"]

    leaderboard = []

    for i in range(len(results)):
        team = {}
        team["rank"] = i + 1
        for f in result_fields:
            team[f] = str(getattr(results[i], f))
        leaderboard.append(team)

    return leaderboard


def get_all_ranks(team: str, competitions: list):
    """
    Get all ranks of a team in a list of competitions, in a form of a dictionary.
    """
    result = {}
    result["team"] = team
    ranks = {}
    for c in competitions:
        results = fetch_competition_leaderboard(c)
        for r in results:
            if r["teamName"] == team:
                ranks[c] = r["rank"]
                break
        if c not in ranks.keys():
            ranks[c] = len(results) + 1
    result["ranks"] = ranks
    return result


def calculate_global_rank(teams: list, competitions: list, weights: list):
    """
    function to calculate the global rank of a team based on its ranks in a list of competitions
    `NOTE`: this function is specific in our competition's scoring system, you may need to adjust it based on your competition

    """

    # each competition has a weight. the competitions list must have the same length as the weights list
    if len(competitions) != len(weights):
        raise ValueError(
            "The competitions list and the weights list must have the same length."
        )
    # the sum of weights must be equal to 100 (specific to our competition scoring system)
    if sum(weights) != 100:
        raise ValueError("The sum of weights must be equal to 100.")

    # more the weight is high more the competition is important
    # calculating the global score of each team
    global_rank = []
    for t in teams:
        # get all ranks of the team in the competitions
        ranks = get_all_ranks(t, competitions)["ranks"]

        # calculate the score of the team
        score = 0
        for c, w in zip(competitions, weights):
            score += 1 / ranks[c] * w

        # append the team to the global rank
        global_rank.append({"team": t, "score": score, "all_ranks": ranks})

    # sort the global rank based on the score
    global_rank = sorted(global_rank, key=lambda x: x["score"], reverse=True)
    # add ranks to the global rank
    for i, r in enumerate(global_rank):
        global_rank[i]["rank"] = i + 1

    return global_rank
