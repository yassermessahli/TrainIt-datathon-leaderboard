from django.shortcuts import render
from .leaderboard import calculate_global_rank, get_all_ranks

# Create your views here.


def leaderboard_view(request):
    """
    View function for the leaderboard page.
    """

    teams = [
        "kurtosis",
        "Megatron",
        "PentechAI",
        "CrusAIders",
        "Vgaith",
        "K-beans",
        "Data Rizzlers",
        "samir-boumahdi-estin",
    ]  # Replace with actual team names
    competitions = [
        "instadeep-challenge-soai",
        "iiot-cyber-security-challenge-haick-2022",
        "jumia-purchase-prediction",
        "lcbm-challenge-haick-2022",
    ]  # Replace with actual competition IDs
    weights = [25, 30, 20, 25]  # Replace with actual weights

    # get the global rank of the teams
    global_rank = calculate_global_rank(teams, competitions, weights)

    # create the context
    context = {
        "global_rank": global_rank,
        "competitions": competitions,
    }
    return render(request, template_name="leaderboard.html", context=context)
