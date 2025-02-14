/**********************************************************
* PROVIDE THE FOLLOWING INFORMATION
* ID Number:
* Name:
* Lab Number:
* System Number:
***********************************************************/
package labtest;

import java.io.*;
import java.util.*;
import java.util.Comparator;

class Player {
    private String playerName;
    private Role role;
    private int runsScored;
    private int wicketsTaken;
    private String teamName;

    public Player(String playerName, Role role, int runsScored, int wicketsTaken, String teamName) {
        this.playerName = playerName;
        this.role = role;
        this.runsScored = runsScored;
        this.wicketsTaken = wicketsTaken;
        this.teamName = teamName;
    }

    public String getPlayerName() {
        return playerName;
    }

    public void setPlayerName(String playerName) {
        this.playerName = playerName;
    }

    public Role getRole() {
        return role;
    }

    public void setRole(Role role) {
        this.role = role;
    }

    public int getRunsScored() {
        return runsScored;
    }

    public void setRunsScored(int runsScored) {
        this.runsScored = runsScored;
    }

    public int getWicketsTaken() {
        return wicketsTaken;
    }

    public void setWicketsTaken(int wicketsTaken) {
        this.wicketsTaken = wicketsTaken;
    }

    public String getTeamName() {
        return teamName;
    }

    public void setTeamName(String teamName) {
        this.teamName = teamName;
    }

    @Override
    public String toString() {
        return "Player{" +
               "playerName='" + playerName + '\'' +
               ", role=" + role +
               ", runsScored=" + runsScored +
               ", wicketsTaken=" + wicketsTaken +
               ", teamName='" + teamName + '\'' +
               '}';
    }

    public String toCsvFormat() {
        return String.format("%s,%s,%d,%d,%s",
                playerName, role, runsScored, wicketsTaken, teamName);
    }
}

enum Role {
    BATSMAN, BOWLER, ALL_ROUNDER;

    public static Role fromString(String role) {
        switch (role.toUpperCase().replace("-", "_")) {
            case "BATSMAN":
                return BATSMAN;
            case "BOWLER":
                return BOWLER;
            case "ALL_ROUNDER":
                return ALL_ROUNDER;
            default:
                throw new IllegalArgumentException("Unknown role: " + role);
        }
    }
}

class RunsComparator implements Comparator<Player> {
	/************************** Q.1 WRITE CODE FOR THIS METHOD *********************************/
    public int compare(Player p1, Player p2) {
        // Question 1: Write code for comparing/sorting runs in descending order [Total: 2 marks]
        // Return a negative value if the first player has more runs, 
        // a positive value if the second player has more runs, or zero if they have the same number of runs.
    	if (p1.getRunsScored() > p2.getRunsScored()) {
    		return -1;
    	}
    	else if (p1.getRunsScored() < p2.getRunsScored()){
    		return 1;
    	}
    	else {
    		return 0;
    	}
    }
}

class CricketDataHandler {
    
	private static final Exception IllegalArgumentException = null;

	/************************** Q.2 WRITE CODE FOR THIS METHOD *********************************/
	public List<Player> readPlayersFromFile(String fileName) throws IOException {
        // Question 2: Write code for reading players from a file [Total: 9 marks]
        // Step 1: Create an empty list to store player details. [1 mark]
        // Step 2: Open the specified file for reading data. [1 mark]
        // Step 3: Ignore the first line since it contains the column names. [1 mark]
        // Step 4: Read each line one by one until reaching the end of the file. [1 mark]
        // Step 5: Split the line into different pieces of information. [1 mark]
        // Step 6: Create a new player using this information. [1 mark]
        // Step 7: Add the new player to the list. [1 mark]
        // Step 8: Close the file after reading all data. [1 mark]
        // Step 9: Return the complete list of players. [1 mark]
		
		List<Player> pllist = new ArrayList<>();
		Scanner src = null;
		try {
		src = new Scanner( new FileInputStream(fileName));
		} catch(FileNotFoundException e) {
			System.out.println("File Not Found!");
			System.exit(0);
		}
		
		
		src.nextLine();
		for(int i=0;src.hasNext();++i) {
			String next = src.nextLine();
			String[] lineData = next.split(",");
			String pName = lineData[0];
			Role pRole = Role.fromString(lineData[1]);
			int runs = Integer.parseInt(lineData[2]);
			int wkts = Integer.parseInt(lineData[3]);
			String tname = lineData[4];
			Player p = new Player(pName, pRole, runs, wkts, tname);
			pllist.add(p);
		}
		
		src.close();
		return pllist;
		
		
    }

	/************************** Q.3 WRITE CODE FOR THIS METHOD *********************************/
    public void writePlayersToFile(String fileName, List<Player> players) throws IOException {
        // Question 3: Write code for writing players to a file [Total: 4 marks]
        // Step 1: Prepare to write data into the specified file. [1 mark]
        // Step 2: Write the column names as the first line of the file. [1 mark]
        // Step 3: For each player in the list, convert their details to the desired format. [1 mark]
        // Step 4: Write each player's information to the file. [1 mark]
    	
    	PrintWriter outputStream = null;
    	
    	try {
    		outputStream = new PrintWriter(new FileOutputStream(fileName));
    		
    	} catch(FileNotFoundException e) {
			System.out.println("File Not Found!");
			System.exit(0);
    	}
    	
    	outputStream.println("PlayerName,Role,RunsScored,WicketsTaken,TeamName");
    	
    	for (Player p : players) {
    		String name = p.getPlayerName();
    		Role pRole = p.getRole();
    		int pRuns = p.getRunsScored();
    		int pWkts = p.getWicketsTaken();
    		String tname = p.getTeamName();
    		
    		outputStream.println(name+","+pRole.toString()+","+pRuns+","+pWkts+","+tname);
    		
    	}
    	
    	outputStream.close();
    }
    
	/************************** Q.4 WRITE CODE FOR THIS METHOD 
	 * @throws Exception *********************************/
    public void updatePlayerStats(List<Player> players, String playerName, int runs, int wickets) {
        // Question 4: Write code for updating player stats [Total: 5 marks]
        // Step 1: Go through each player in the list. [1 mark]
        // Step 2: Check if the current player's name matches the given name. [1 mark]
        // Step 3: If it matches, update the player's runs with the new value. Updated value will be the sum of the old runs and the argument runs. [1 mark]
        // Step 4: Similarly, update the player's wickets with the new value. Updated value will be the sum of the old wickets and the argument wickets. [1 mark]
        // Step 5: If no player matches the given name, throw an IllegalArgumentException exception. [1 mark]
    	boolean flag = false;

    	for (Player p : players) {
    		
    		
    		if(p.getPlayerName().equalsIgnoreCase(playerName)) {
    			int pruns = p.getRunsScored();
    			int pwkts = p.getWicketsTaken();
    			int sum_runs = pruns + runs;
    			int sum_wkts = pwkts + wickets;
    			p.setRunsScored(sum_runs);
    			p.setWicketsTaken(sum_wkts);
   
    			flag = true;
    		} 
    		
    		
    	}
    	
    	
    }

	/************************** Q.5 WRITE CODE FOR THIS METHOD 
	 * @throws Exception *********************************/
    public double calculateTeamAverageRuns(List<Player> players, String teamName){
        // Question 5: Write code for calculating team average runs [Total: 5 marks]
        // Step 1: Filter players belonging to the specified team. [2 marks]
        // Step 2: If no players from the specified team are found, throw an IllegalArgumentException exception. [1 mark]
        // Step 3: Calculate the total runs scored by all players from this team. [1 mark]
        // Step 4: Compute and return the average runs scored. [1 mark]
    	
    	List<Player> pfil = new ArrayList<>();
    	for (Player p : players) {
    		if (p.getTeamName().equalsIgnoreCase(teamName)) {
    			pfil.add(p);
    		}
    	}
    	 
    	
    	double sum = 0;
    	int total_players = pfil.size();
    	   	
    	
    	for (Player p: pfil) {
    		sum += p.getRunsScored();
    	}
    	
    	double mean = sum/total_players;
    	return mean;
    
    }
}

@FunctionalInterface
interface PlayerFilter<T> {
    List<Player> filter(List<Player> players, T value);
}

class TeamFilterStrategy implements PlayerFilter<String> {
    
	/************************** Q.6 WRITE CODE FOR THIS METHOD *********************************/
    public List<Player> filter(List<Player> players, String teamName) {
        // Question 6: Write code for filtering players by team [Total: 5 marks]
        // Step 1: Create an empty list for players matching the criteria. [1 mark]
        // Step 2: Go through each player in the players list. [1 mark]
        // Step 3: If the player's team matches the given name, add them to the list. [2 marks]
        // Step 4: Return the list containing all matching players. [1 mark]
    	
    	List<Player> pfil = new ArrayList<>();
    	for (Player p : players) {
    		if (p.getTeamName().equalsIgnoreCase(teamName)) {
    			pfil.add(p);
    		}
    	}
    	
    	return pfil;
    }
}

class AllRounderStatsFilter implements PlayerFilter<int[]> {
    
	/************************** Q.7 WRITE CODE FOR THIS METHOD *********************************/
    public List<Player> filter(List<Player> players, int[] criteria) {
        // Question 7: Write code for filtering all-rounders by stats [Total: 5 marks]
        // criteria[0] = minimum runs, criteria[1] = minimum wickets
        // Step 1: Create an empty list for players matching the criteria. [1 mark]
        // Step 2: Go through each player in the list. [1 mark]
        // Step 3: If the player is an all-rounder and meets the given criteria for both runs and wickets, add them to the list. [2 marks]
        // Step 4: Return the list containing all matching players. [1 mark]
    	List<Player> pfil = new ArrayList<>();
    	
    	for (Player p : players) {
    		if (p.getRunsScored() > criteria[0] | p.getRunsScored() == criteria[0]) {
    			if (p.getWicketsTaken() > criteria[1] | p.getWicketsTaken() == criteria[1]) {
    				pfil.add(p);
    			}
    		}
    	}
    	
    	return pfil;
    }
}

public class P2022B4A70920_P1 {
    private static void printPlayers(String header, List<Player> players) {
        System.out.println("\n--- " + header + " ---");
        for (Player player : players) {
            System.out.println(player);
        }
    }

    public static void main(String[] args) {
        CricketDataHandler dataHandler = new CricketDataHandler();
        List<Player> players = new ArrayList<>();

        try {
            // Read data from file
            players = dataHandler.readPlayersFromFile("C:\\Users\\user\\Desktop\\2022B4A70920P\\CBT\\src\\labtest\\inputCricketData.csv");
        } catch (FileNotFoundException e) {
            System.out.println("Error: File not found.");
            return;
        } catch (IOException e) {
            System.out.println("Error: Unable to read file.");
            return;
        }

        // Perform a series of cricket analytics operations

        // Search players by team
        PlayerFilter<String> teamFilter = new TeamFilterStrategy();
        List<Player> indianPlayers = teamFilter.filter(players, "India");
        printPlayers("Players from India", indianPlayers);

        List<Player> australianPlayers = teamFilter.filter(players, "Australia");
        printPlayers("Players from Australia", australianPlayers);

        // Update stats for some players
        System.out.println("\n--- Updating Player Statistics ---");
        dataHandler.updatePlayerStats(players, "Virat Kohli", 82, 0);
        dataHandler.updatePlayerStats(players, "Jasprit Bumrah", 2, 3);
        dataHandler.updatePlayerStats(players, "Steve Smith", 144, 0);
        dataHandler.updatePlayerStats(players, "Pat Cummins", 12, 4);

        // Sort and display by runs
        players.sort(new RunsComparator());
        printPlayers("Players Sorted by Runs", players);

        // Calculate team averages
        System.out.println("\n--- Team Averages ---");
        double indiaAvg = dataHandler.calculateTeamAverageRuns(players, "India");
        System.out.println("Average Runs for Team India: " + indiaAvg);

        double ausAvg = dataHandler.calculateTeamAverageRuns(players, "Australia");
        System.out.println("Average Runs for Team Australia: " + ausAvg);

        double engAvg = dataHandler.calculateTeamAverageRuns(players, "England");
        System.out.println("Average Runs for Team England: " + engAvg);

        // Filter and print all-rounders
        int[] criteria = {2000, 100}; // minimum runs and wickets
        List<Player> goodAllRounders = new AllRounderStatsFilter().filter(players, criteria);
        printPlayers("All-rounders with good stats (>2000 runs and >100 wickets)", goodAllRounders);

        try {
            // Save updated data to file
            dataHandler.writePlayersToFile("outputCricketData.csv", players);
        } catch (IOException e) {
            System.out.println("Error: Unable to write to file.");
        }
    }
}