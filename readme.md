# Cricket Analytics System

## Overview
This Java-based Cricket Analytics System manages and analyzes cricket player statistics. The system implements various functionalities including player data management, team analysis, and performance filtering.

## Project Structure
```
OOPS_graded_final_dataset/
└── 1015/
    └── p1.java         # Main implementation file
```

## Core Components

### 1. Player Class
- Manages individual player data:
  - Player Name
  - Role (BATSMAN, BOWLER, ALL_ROUNDER)
  - Runs Scored
  - Wickets Taken
  - Team Name
- Includes getters/setters and data formatting methods

### 2. CricketDataHandler Class
Implements core data management functionalities:

#### a. File Operations
- `readPlayersFromFile(String fileName)` [9 points]
  - Reads player data from CSV
  - Handles file exceptions
  - Parses player information

- `writePlayersToFile(String fileName, List<Player> players)` [4 points]
  - Writes player data to CSV
  - Includes column headers
  - Formats player information

#### b. Player Management
- `updatePlayerStats(List<Player> players, String playerName, int runs, int wickets)` [5 points]
  - Updates player statistics
  - Validates player existence
  - Throws exception for invalid players

#### c. Team Analysis
- `calculateTeamAverageRuns(List<Player> players, String teamName)` [5 points]
  - Calculates average runs for a team
  - Handles empty team scenarios
  - Returns team batting average

### 3. Filtering Strategies

#### a. TeamFilterStrategy
- Implements `PlayerFilter<String>`
- Filters players by team name
- Returns list of players from specified team

#### b. AllRounderStatsFilter
- Implements `PlayerFilter<int[]>`
- Filters players based on performance criteria
- Minimum runs and wickets thresholds

### 4. Comparators
- `RunsComparator`: Sorts players by runs scored (descending order)

## Evaluation Results

### Automated Grading (Sample: ID 1015)
```
Total Score: 21/35
Component Breakdown:
- compare: 2/2
- readPlayersFromFile: 5/9
- writePlayersToFile: 0/4
- updatePlayerStats: 3/5
- calculateTeamAverageRuns: 3/5
- teamFilter: 3/5
- allRounderFilter: 5/5
```

### Key Features
1. File I/O Operations
2. Player Data Management
3. Team Statistics
4. Performance Filtering
5. Data Sorting

### Usage Example
```java
public static void main(String[] args) {
    CricketDataHandler dataHandler = new CricketDataHandler();
    
    // Read player data
    List<Player> players = dataHandler.readPlayersFromFile("inputCricketData.csv");
    
    // Filter players by team
    PlayerFilter<String> teamFilter = new TeamFilterStrategy();
    List<Player> indianPlayers = teamFilter.filter(players, "India");
    
    // Update player statistics
    dataHandler.updatePlayerStats(players, "Virat Kohli", 82, 0);
    
    // Calculate team averages
    double indiaAvg = dataHandler.calculateTeamAverageRuns(players, "India");
    
    // Filter all-rounders
    int[] criteria = {2000, 100};
    List<Player> goodAllRounders = new AllRounderStatsFilter().filter(players, criteria);
}
```

## Evaluation System
- Uses ensemble evaluation approach
- Multiple evaluations per submission
- Tracks scoring variance
- Provides detailed component scoring

## Dependencies
- Java Standard Library
- File I/O capabilities
- Collection Framework

## Error Handling
- File not found exceptions
- Invalid player exceptions
- Invalid team exceptions
- Data parsing errors