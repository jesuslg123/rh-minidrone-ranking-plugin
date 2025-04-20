# RotorHazard Minidrone Plugin

This repository contains the Minidrone Plugin for RotorHazard, a race timing system for FPV drone racing. The plugin introduces a custom ranking method based on the last heat positions and lap times.

## Installation

To install the Minidrone Plugin in RotorHazard, follow these steps:

1. **Clone the Repository**:
   Ensure you have the RotorHazard repository cloned on your system. Navigate to the `plugins` directory within the RotorHazard source folder.

   ```bash
   cd /path/to/RotorHazard/src/server/plugins
   ```

2. **Copy the Plugin**:
   Copy the `minidrone_plugin` folder into the `plugins` directory.

   ```bash
   cp -r /path/to/minidrone_plugin /path/to/RotorHazard/src/server/plugins/
   ```

3. **Restart RotorHazard**:
   Restart the RotorHazard server to load the new plugin.

   ```bash
   cd /path/to/RotorHazard/src/server
   python server.py
   ```

4. **Verify Installation**:
   Check the RotorHazard logs to ensure the plugin is initialized correctly. You should see a log entry similar to:

   ```
   Initializing MINIDRONE plugin
   ```

## Usage

The Minidrone Plugin introduces a custom ranking method called **"Minidrone - Last Heat Position and lap time"**. This ranking method processes heats to generate a leaderboard based on the following logic:

1. **Reverse Heat Order**:
   The heats are processed in reverse order, starting from the last heat (top pilots).

2. **Generate Leaderboard**:
   The plugin consolidates the results of all heats into a single leaderboard.

3. **Group by Heat**:
   The leaderboard is grouped by heat to facilitate comparisons between pilots in adjacent heats.

4. **Pilot Swapping**:
   Pilots are swapped between heats based on the following conditions:
   - If the last pilot of the current heat and the first pilot of the next heat have the same lap count, the pilot with the faster lap time is ranked higher.
   - If the last pilot of the current heat has fewer laps than the first pilot of the next heat, they are swapped.

5. **Flatten Leaderboard**:
   The grouped leaderboard is flattened back into a single list for final ranking.

### Steps to Use the Plugin

1. **Enable the Ranking Method**:
   In the RotorHazard interface, select the race class you want to apply the ranking method to.

2. **Run a Race**:
   Conduct races as usual. The plugin will automatically process the results using the custom ranking method.

3. **View Results**:
   The leaderboard will display the rankings based on the logic described above.

## Updated Logic Overview

The plugin's ranking logic has been updated to include the following steps:

1. **Reverse Heat Order**:
   The heats are processed in reverse order, starting from the last heat (top pilots).

2. **Generate Leaderboard**:
   The plugin consolidates the results of all heats into a single leaderboard.

3. **Group by Heat**:
   The leaderboard is grouped by heat to facilitate comparisons between pilots in adjacent heats.

4. **Pilot Swapping**:
   Pilots are swapped between heats based on the following conditions:
   - If the last pilot of the current heat and the first pilot of the next heat have the same lap count, the pilot with the faster lap time is ranked higher.
   - If the last pilot of the current heat has fewer laps than the first pilot of the next heat, they are swapped.

5. **Detailed Logging**:
   The plugin logs detailed information about the current and next heat results, including the pilots being swapped and the updated heats after swapping.

6. **Flatten Leaderboard**:
   The grouped leaderboard is flattened back into a single list for final ranking.

7. **Return Final Rankings**:
   The final leaderboard and metadata are returned for display in the RotorHazard interface.

### Additional Logging Details

The plugin now logs the following during the ranking process:
- Current and next heat results
- Leaderboard transformations
- Pilot swaps, including callsigns and reasons for swapping
- Updated heats after swapping

## Logging

The plugin logs detailed information during the ranking process, including:
- Heat results
- Leaderboard transformations
- Pilot swaps

Logs can be found in the RotorHazard log files, typically located in the `logs/` directory.

## Contributing

Contributions to the Minidrone Plugin are welcome! Feel free to submit issues or pull requests to improve the functionality or add new features.

## License

This plugin is licensed under the MIT License. See the `LICENSE` file for details.
