# codev.py
from openai import OpenAI
import json
import os
import statistics
from typing import List, Dict, Any
from pathlib import Path
import time

class CodEv:
    def __init__(self, api_key: str):
        """Initialize CodEv with OpenAI API key."""
        self.client = OpenAI(api_key=api_key)
        
    def get_single_evaluation(self, code: str) -> Dict[str, Any]:
        """Get a single evaluation from the model."""
        try:
            prompt = """You are evaluating a Java code submission for a Cricket Analytics System.
            Provide your evaluation in VALID JSON format only.
            
            Evaluate these 7 functions:
            1. compare(Player p1, Player p2) [2 points]
            2. readPlayersFromFile(String fileName) [9 points]
            3. writePlayersToFile(String fileName, List<Player> players) [4 points]
            4. updatePlayerStats(List<Player> players, String playerName, int runs, int wickets) [5 points]
            5. calculateTeamAverageRuns(List<Player> players, String teamName) [5 points]
            6. TeamFilterStrategy.filter(List<Player> players, String teamName) [5 points]
            7. AllRounderStatsFilter.filter(List<Player> players, int[] criteria) [5 points]

            Student Code:
            ```java
            {code}
            ```

            Respond ONLY with a JSON object in this exact format:
            {{
                "function_scores": {{
                    "compare": {{"score": 0, "max_score": 2, "feedback": "feedback here"}},
                    "readPlayersFromFile": {{"score": 0, "max_score": 9, "feedback": "feedback here"}},
                    "writePlayersToFile": {{"score": 0, "max_score": 4, "feedback": "feedback here"}},
                    "updatePlayerStats": {{"score": 0, "max_score": 5, "feedback": "feedback here"}},
                    "calculateTeamAverageRuns": {{"score": 0, "max_score": 5, "feedback": "feedback here"}},
                    "teamFilter": {{"score": 0, "max_score": 5, "feedback": "feedback here"}},
                    "allRounderFilter": {{"score": 0, "max_score": 5, "feedback": "feedback here"}}
                }},
                "total_score": 0,
                "overall_feedback": "overall feedback here"
            }}"""

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a code evaluator that ONLY responds with valid JSON. No other text or explanation."
                    },
                    {
                        "role": "user",
                        "content": prompt.format(code=code)
                    }
                ],
                temperature=0.1
            )

            response_text = response.choices[0].message.content.strip()
            return json.loads(response_text)

        except Exception as e:
            print(f"Error in single evaluation: {str(e)}")
            return None

    def evaluate_submission(self, code: str, model_solution: str, ensemble_size: int = 5) -> Dict[str, Any]:
        """Evaluate a single submission using ensemble approach."""
        print(f"\nStarting ensemble evaluation with {ensemble_size} models...")
        
        evaluations = []
        for i in range(ensemble_size):
            print(f"Running evaluation {i+1}/{ensemble_size}...")
            result = self.get_single_evaluation(code)
            if result:
                evaluations.append(result)

        if not evaluations:
            print("All evaluation attempts failed")
            return None

        # Ensemble processing
        try:
            # Get all scores for each function
            function_scores = {
                func_name: [eval['function_scores'][func_name]['score'] 
                           for eval in evaluations]
                for func_name in evaluations[0]['function_scores'].keys()
            }

            # Calculate mode scores for each function
            final_scores = {
                func_name: statistics.mode(scores)
                for func_name, scores in function_scores.items()
            }

            # Get total scores
            total_scores = [eval['total_score'] for eval in evaluations]
            final_total = statistics.mode(total_scores)

            # Select the evaluation whose total score is closest to the final total
            best_eval_index = min(range(len(evaluations)), 
                                key=lambda i: abs(evaluations[i]['total_score'] - final_total))
            best_evaluation = evaluations[best_eval_index]

            # Create final result with mode scores and feedback from best evaluation
            final_result = {
                "function_scores": {
                    func_name: {
                        "score": final_scores[func_name],
                        "max_score": best_evaluation['function_scores'][func_name]['max_score'],
                        "feedback": best_evaluation['function_scores'][func_name]['feedback']
                    }
                    for func_name in final_scores.keys()
                },
                "total_score": final_total,
                "overall_feedback": best_evaluation['overall_feedback'],
                "ensemble_statistics": {
                    "evaluations_count": len(evaluations),
                    "score_variance": {
                        func_name: statistics.variance(scores) if len(scores) > 1 else 0
                        for func_name, scores in function_scores.items()
                    },
                    "total_score_variance": statistics.variance(total_scores) if len(total_scores) > 1 else 0
                }
            }

            print(f"Ensemble evaluation complete. Final score: {final_total}")
            return final_result

        except Exception as e:
            print(f"Error in ensemble processing: {str(e)}")
            return None