# main.py
import json
import os
from codev import CodEv
from datetime import datetime
from pathlib import Path

def load_api_key() -> str:
    """Load API key from environment variable or config file."""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
                api_key = config.get('api_key')
        except FileNotFoundError:
            raise ValueError("API key not found in environment variables or config.json")
    return api_key

def save_results(results: dict, output_dir: str = 'results'):
    """Save evaluation results with timestamp."""
    Path(output_dir).mkdir(exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = Path(output_dir) / f'evaluation_results_{timestamp}.json'
    
    with output_file.open('w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    print(f"Results saved to {output_file}")

def main():
    # Initialize CodEv with API key
    try:
        api_key = load_api_key()
        codev = CodEv(api_key)
    except ValueError as e:
        print(f"Error: {e}")
        return

    # Read model solution
    try:
        with open('CricketAnalyticsSolution.java', 'r', encoding='utf-8') as f:
            model_solution = f.read()
    except FileNotFoundError:
        print("Error: Model solution file not found")
        return
    
    # Read and evaluate submissions
    submissions = codev.read_files('OOPS_graded_final_dataset')
    results = {}
    
    print(f"Found {len(submissions)} submissions to evaluate")
    
    for folder_id, submission in submissions.items():
        print(f"\nEvaluating submission {folder_id}...")
        
        result = codev.evaluate_submission(
            code=submission['code'],
            model_solution=model_solution
        )
        
        if result:
            results[folder_id] = result
            print(f"Score: {result['score']}")
            print(f"Comment: {result['comment'][:200]}...")  # Show first 200 chars
    
    # Save results
    save_results(results)

if __name__ == "__main__":
    main()