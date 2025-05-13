from venv import logger
import RHUtils
from eventmanager import Evt
from RHRace import StartBehavior
from Results import RaceClassRankMethod

def register_handlers(args):
    args['register_fn'](
        RaceClassRankMethod(
            "Minidrone - Last Heat Position and lap time",
            rank_heat_pos_and_time,
            None,
            None
        )
    )

def rank_heat_pos_and_time(rhapi, race_class, _args):
    """
    Processes the heats to generate a ranking based on the last heat positions and lap times.

    Args:
        rhapi: The API object for accessing race data.
        race_class: The race class object containing class information.
        _args: Additional arguments (not used).

    Returns:
        tuple: A ranked list of pilots and metadata for the leaderboard.
    """

    logger.debug("Starting ranking process for heats")

    heats = rhapi.db.heats_by_class(race_class.id)
    # Reverse the heats to start from the last heat aka the top pilots
    reversed_heats = list(reversed(heats))

    logger.debug(race_class.name)

    # Initialize the leaderboard
    leaderboard = []

    # Iterate over all heats in reverse order and generate the leaderboard
    for heat in reversed_heats:
        heat_result = rhapi.db.heat_results(heat)
        if not heat_result: # No heat result available as are pending
            logger.debug(f"No heat_result for heat: {heat.display_name}, skipping.")
            continue
        leaderboard_type = heat_result['meta']['primary_leaderboard']
        heat_leaderboard = heat_result[leaderboard_type]

        # Append the heat leaderboard to the consolidated leaderboard
        append_to_leaderboard(leaderboard, heat, heat_leaderboard)

    grouped_leaderboard = group_by_heat(leaderboard)  
    temp_leaderboard = swap_on_grouped_board(grouped_leaderboard)
    
    # Flatten the grouped leaderboard back to a single list
    leaderboard = [item for sublist in temp_leaderboard for item in sublist]

    meta = {
        'rank_fields': [{
            'name': 'heat',
            'label': "Heat"
        }, {
            'name': 'fastest_lap',
            'label': "Fastest Lap"
        },{
            'name': 'laps',
            'label': "Laps"
        },{
            'name': 'heat_rank',
            'label': "Position"
        }]
    }

    logger.debug("Ranking process completed")
    return leaderboard, meta
    
def initialize(rhapi):
    logger.debug("Initializing MINIDRONE plugin")
    rhapi.events.on(Evt.CLASS_RANK_INITIALIZE, register_handlers)

def append_to_leaderboard(leaderboard, heat, heat_leaderboard):
    """
    Appends the pilot data to the leaderboard.

    Args:
        leaderboard (list): The leaderboard to append to.
        heat (object): The heat object containing heat information.
        line (dict): The pilot data to append.

    Returns:
        None
    """
    for line in heat_leaderboard:
        rank_pos = heat_leaderboard.index(line) + 1
        leaderboard.append({
            'pilot_id': line['pilot_id'],
            'callsign': line['callsign'],
            'team_name': line['team_name'],
            'heat': heat.display_name,
            'heat_rank': line['position'],
            'position': rank_pos,
            'fastest_lap': line['fastest_lap'],
            'laps': line['laps'],
        })

def group_by_heat(leaderboard):
    """
    Groups the leaderboard by heat and transforms it into a list of lists.

    Args:
        leaderboard (list): The leaderboard to group.

    Returns:
        list: A list of lists of grouped leaderboard entries.
    """
    grouped = {}

    # Group the leaderboard by heat
    for entry in leaderboard:
        heat_name = entry['heat']
        if heat_name not in grouped:
            grouped[heat_name] = []
        grouped[heat_name].append(entry)

    # Convert grouped dictionary to a list of lists
    result = list(grouped.values())

    return result

def swap_on_grouped_board(grouped_leaderboard):
    """
    Swaps the last pilot of a heat with the first pilot of the next heat based on conditions.

    Args:
        grouped_leaderboard (list): An array of arrays representing grouped leaderboard entries.

    Returns:
        list: The updated grouped leaderboard after performing swaps.
    """
    for i in range(len(grouped_leaderboard) - 1):
        current_heat = grouped_leaderboard[i]
        next_heat = grouped_leaderboard[i + 1]

        # Get the last pilot of the current heat and the first pilot of the next heat
        last_pilot_current_heat = current_heat[-1]
        first_pilot_next_heat = next_heat[0]

        # Compare lap counts
        if last_pilot_current_heat['laps'] == first_pilot_next_heat['laps']:
            # Compare fastest lap times
            if last_pilot_current_heat['fastest_lap'] > first_pilot_next_heat['fastest_lap']:
                # Swap pilots
                current_heat[-1], next_heat[0] = next_heat[0], current_heat[-1]
                logger.debug(f"Swapped pilots due to times: {next_heat[0]['callsign']} with {current_heat[-1]['callsign']}")
        elif last_pilot_current_heat['laps'] < first_pilot_next_heat['laps']:
            # Swap pilots
            current_heat[-1], next_heat[0] = next_heat[0], current_heat[-1]
            logger.debug(f"Swapped pilots due to laps: {next_heat[0]['callsign']} with {current_heat[-1]['callsign']}")

    return grouped_leaderboard
