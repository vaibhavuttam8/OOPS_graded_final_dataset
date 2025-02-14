import yaml
import json
from typing import Dict, List, Any, Tuple
import os
import re
from dataclasses import dataclass
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import pingouin as pg

@dataclass
class EvaluationCriteria:
    functionality: float
    readability: float
    efficiency: float
    documentation: float

class CodEvFramework:
    def __init__(self):
        self.functions_to_evaluate = [
            "RunsComparator.compare",
            "CricketDataHandler.readPlayersFromFile",
            "CricketDataHandler.writePlayersToFile",
            "CricketDataHandler.updatePlayerStats",
            "CricketDataHandler.calculateTeamAverageRuns",
            "TeamFilterStrategy.filter",
            "AllRounderStatsFilter.filter"
        ]
        
        # Grading criteria with detailed rubric as mentioned in the paper
        self.grading_criteria = {
            "RunsComparator.compare": {
                "total_marks": 2,
                "criteria": EvaluationCriteria(0.4, 0.2, 0.2, 0.2)
            },
            "CricketDataHandler.readPlayersFromFile": {
                "total_marks": 9,
                "criteria": EvaluationCriteria(0.5, 0.2, 0.2, 0.1)
            },
            "CricketDataHandler.writePlayersToFile": {
                "total_marks": 4,
                "criteria": EvaluationCriteria(0.4, 0.2, 0.3, 0.1)
            },
            "CricketDataHandler.updatePlayerStats": {
                "total_marks": 5,
                "criteria": EvaluationCriteria(0.5, 0.2, 0.2, 0.1)
            },
            "CricketDataHandler.calculateTeamAverageRuns": {
                "total_marks": 5,
                "criteria": EvaluationCriteria(0.4, 0.2, 0.3, 0.1)
            },
            "TeamFilterStrategy.filter": {
                "total_marks": 5,
                "criteria": EvaluationCriteria(0.4, 0.2, 0.3, 0.1)
            },
            "AllRounderStatsFilter.filter": {
                "total_marks": 5,
                "criteria": EvaluationCriteria(0.4, 0.2, 0.3, 0.1)
            }
        }
        
        self.vectorizer = TfidfVectorizer(token_pattern=r'[A-Za-z_][A-Za-z0-9_]*')

    def read_file_content(self, file_path: str) -> str:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def calculate_code_similarity(self, code1: str, code2: str) -> float:
        # Preprocess code to focus on logic rather than formatting
        def preprocess_code(code: str) -> str:
            code = re.sub(r'//.*?\n|/\*.*?\*/', '', code, flags=re.DOTALL)  # Remove comments
            code = re.sub(r'\s+', ' ', code)  # Normalize whitespace
            return code.strip()

        code1_processed = preprocess_code(code1)
        code2_processed = preprocess_code(code2)
        
        # Calculate TF-IDF vectors and cosine similarity
        try:
            tfidf_matrix = self.vectorizer.fit_transform([code1_processed, code2_processed])
            return cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        except:
            return 0.0

    def evaluate_functionality(self, student_impl: str, solution_impl: str, feedback: str) -> float:
        # Evaluate functionality based on code similarity and feedback
        code_similarity = self.calculate_code_similarity(student_impl, solution_impl)
        
        # Check for critical errors in feedback
        error_indicators = ["incorrect", "error", "not implemented", "missing"]
        error_penalty = sum(0.2 for indicator in error_indicators if indicator in feedback.lower())
        
        return max(0.0, code_similarity - error_penalty)

    def evaluate_readability(self, code: str) -> float:
        # Evaluate code readability based on various metrics
        if not code.strip():
            return 0.0
            
        metrics = {
            'indentation': len(re.findall(r'^\s+', code, re.MULTILINE)) / len(code.splitlines()),
            'naming': len(re.findall(r'[A-Za-z_][A-Za-z0-9_]*', code)) / len(code.splitlines()),
            'comments': len(re.findall(r'//.*?$|/\*.*?\*/', code, re.MULTILINE | re.DOTALL)) / len(code.splitlines())
        }
        
        return sum(metrics.values()) / len(metrics)

    def evaluate_efficiency(self, code: str, feedback: str) -> float:
        # Evaluate code efficiency based on complexity indicators
        if not code.strip():
            return 0.0
            
        # Check for nested loops and complexity
        nested_loops = len(re.findall(r'for.*?for|while.*?while', code, re.DOTALL))
        conditional_complexity = len(re.findall(r'if|else|switch|case', code))
        
        # Normalize metrics
        efficiency_score = 1.0 - (nested_loops * 0.1 + conditional_complexity * 0.05)
        
        # Consider feedback
        if "inefficient" in feedback.lower() or "could be simplified" in feedback.lower():
            efficiency_score *= 0.8
            
        return max(0.0, efficiency_score)

    def evaluate_documentation(self, code: str) -> float:
        # Evaluate documentation quality
        if not code.strip():
            return 0.0
            
        # Count meaningful comments and documentation
        doc_lines = len(re.findall(r'/\*\*.*?\*/|//.*?$', code, re.MULTILINE | re.DOTALL))
        total_lines = len(code.splitlines())
        
        return min(1.0, doc_lines / (total_lines * 0.2))  # Expect ~20% documentation

    def extract_function(self, code: str, function_name: str) -> str:
        class_name, method_name = function_name.split('.')
        
        # Find class
        class_match = re.search(f'class\\s+{class_name}\\s*{{.*?}}', code, re.DOTALL)
        if not class_match:
            return ""
        
        class_code = class_match.group(0)
        
        # Find method within class
        method_pattern = f'(public|private|protected)?\\s*.*?\\s+{method_name}\\s*\\([^)]*\\)\\s*{{.*?}}'
        method_match = re.search(method_pattern, class_code, re.DOTALL)
        
        return method_match.group(0) if method_match else ""

    def extract_function_feedback(self, feedback: str, function_name: str) -> str:
        class_name, method_name = function_name.split('.')
        feedback_lines = feedback.split('\n')
        
        relevant_feedback = []
        for i, line in enumerate(feedback_lines):
            if method_name.lower() in line.lower() or class_name.lower() in line.lower():
                relevant_feedback.append(line.strip())
                # Include context (next line)
                if i + 1 < len(feedback_lines):
                    relevant_feedback.append(feedback_lines[i + 1].strip())
                    
        return ' '.join(relevant_feedback) if relevant_feedback else "No specific feedback found."

    def calculate_score(self, student_impl: str, solution_impl: str, feedback: str, 
                       total_marks: int, criteria: EvaluationCriteria) -> Tuple[float, Dict[str, float]]:
        if not student_impl:
            return 0.0, {
                "functionality": 0.0,
                "readability": 0.0,
                "efficiency": 0.0,
                "documentation": 0.0
            }
        
        # Calculate individual scores
        functionality_score = self.evaluate_functionality(student_impl, solution_impl, feedback)
        readability_score = self.evaluate_readability(student_impl)
        efficiency_score = self.evaluate_efficiency(student_impl, feedback)
        documentation_score = self.evaluate_documentation(student_impl)
        
        # Weight the scores according to criteria
        weighted_scores = {
            "functionality": functionality_score * criteria.functionality,
            "readability": readability_score * criteria.readability,
            "efficiency": efficiency_score * criteria.efficiency,
            "documentation": documentation_score * criteria.documentation
        }
        
        # Calculate final score
        final_score = sum(weighted_scores.values()) * total_marks
        
        return final_score, weighted_scores

    def evaluate_function(self, student_code: str, solution_code: str, feedback: str, function_name: str) -> Dict[str, Any]:
        student_impl = self.extract_function(student_code, function_name)
        solution_impl = self.extract_function(solution_code, function_name)
        function_feedback = self.extract_function_feedback(feedback, function_name)
        
        total_marks = self.grading_criteria[function_name]["total_marks"]
        criteria = self.grading_criteria[function_name]["criteria"]
        
        score, component_scores = self.calculate_score(
            student_impl, solution_impl, function_feedback, total_marks, criteria
        )
        
        return {
            "function_name": function_name,
            "score": score,
            "total_marks": total_marks,
            "feedback": function_feedback,
            "component_scores": component_scores,
            "correctness": (score / total_marks) * 100
        }

    def calculate_icc(self, scores: List[float], total_marks: List[float]) -> float:
        # Calculate Intraclass Correlation Coefficient for reliability
        if len(scores) < 2:
            return 0.0
            
        data = {'scores': scores, 'total': total_marks}
        icc = pg.intraclass_corr(data=data, targets='scores', raters='total', ratings='scores')
        return icc['ICC'][0]

    def evaluate_submission(self, student_file: str, solution_file: str, feedback_file: str) -> Dict[str, Any]:
        student_code = self.read_file_content(student_file)
        solution_code = self.read_file_content(solution_file)
        feedback = self.read_file_content(feedback_file)
        
        evaluation_results = []
        scores = []
        total_marks_list = []
        total_score = 0
        total_possible = 0
        
        for function_name in self.functions_to_evaluate:
            result = self.evaluate_function(student_code, solution_code, feedback, function_name)
            evaluation_results.append(result)
            scores.append(result["score"])
            total_marks_list.append(result["total_marks"])
            total_score += result["score"]
            total_possible += result["total_marks"]
        
        # Calculate reliability using ICC
        reliability_score = self.calculate_icc(scores, total_marks_list)
        
        overall_results = {
            "student_id": "2021B5A82799P",
            "total_score": total_score,
            "total_possible": total_possible,
            "percentage": (total_score / total_possible) * 100,
            "reliability_score": reliability_score,
            "function_evaluations": evaluation_results
        }
        
        return overall_results

    def save_results_to_yaml(self, results: Dict[str, Any], output_file: str):
        with open(output_file, 'w', encoding='utf-8') as file:
            yaml.dump(results, file, default_flow_style=False, sort_keys=False)

def main():
    evaluator = CodEvFramework()
    
    # File paths
    student_file = "OOPS_graded_final_dataset/1015/p1.java"
    solution_file = "CricketAnalyticsSolution.java"
    feedback_file = "OOPS_graded_final_dataset/1015/appraise.txt"
    output_file = "evaluation_results.yaml"
    
    # Evaluate submission
    results = evaluator.evaluate_submission(student_file, solution_file, feedback_file)
    
    # Save results to YAML file
    evaluator.save_results_to_yaml(results, output_file)
    print(f"Evaluation completed. Results saved to {output_file}")

if __name__ == "__main__":
    main() 