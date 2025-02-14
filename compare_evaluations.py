import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

def load_data():
    """Load both evaluation datasets."""
    # Load manual grading data
    manual_df = pd.read_csv('Dist_OOPs_80_submission - Dataset-Grader-2.csv')
    
    # Load automated evaluation data
    results_dir = Path('results')
    latest_dir = max(results_dir.iterdir(), key=lambda x: x.stat().st_mtime)
    auto_df = pd.read_csv(latest_dir / 'csv_results' / 'evaluation_summary.csv')
    
    return manual_df, auto_df

def normalize_scores(manual_df, auto_df):
    """Normalize scores to be on the same scale (0-1)."""
    # Manual scores are out of 35
    manual_df['normalized_score'] = manual_df['Score_Grader2'] / 35
    
    # Automated scores are out of 35
    auto_df['normalized_score'] = auto_df['total_score'] / 35
    
    return manual_df, auto_df

def calculate_metrics(manual_df, auto_df):
    """Calculate comparison metrics between manual and automated grading."""
    # Merge datasets on submission ID
    merged_df = pd.merge(
        manual_df[['folder', 'Score_Grader2', 'normalized_score']],
        auto_df[['submission_id', 'total_score', 'normalized_score']],
        left_on='folder',
        right_on='submission_id',
        suffixes=('_manual', '_auto')
    )
    
    # Calculate metrics
    metrics = {
        'pearson_correlation': merged_df['normalized_score_manual'].corr(merged_df['normalized_score_auto']),
        'spearman_correlation': merged_df['normalized_score_manual'].corr(merged_df['normalized_score_auto'], method='spearman'),
        'mean_absolute_error': np.mean(np.abs(merged_df['normalized_score_manual'] - merged_df['normalized_score_auto'])),
        'mean_squared_error': np.mean((merged_df['normalized_score_manual'] - merged_df['normalized_score_auto'])**2),
        'submissions_compared': len(merged_df)
    }
    
    return metrics, merged_df

def generate_visualizations(merged_df, output_dir):
    """Generate visualization plots for the comparison."""
    # Create output directory
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Scatter plot
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=merged_df, x='Score_Grader2', y='total_score')
    plt.plot([0, 35], [0, 35], 'r--')  # Perfect correlation line
    plt.xlabel('Manual Grading Score')
    plt.ylabel('Automated Grading Score')
    plt.title('Manual vs Automated Grading Comparison')
    plt.savefig(output_dir / 'score_comparison_scatter.png')
    plt.close()
    
    # 2. Score distribution comparison
    plt.figure(figsize=(12, 6))
    sns.kdeplot(data=merged_df, x='Score_Grader2', label='Manual Grading')
    sns.kdeplot(data=merged_df, x='total_score', label='Automated Grading')
    plt.xlabel('Score')
    plt.ylabel('Density')
    plt.title('Score Distribution Comparison')
    plt.legend()
    plt.savefig(output_dir / 'score_distributions.png')
    plt.close()
    
    # 3. Difference histogram
    plt.figure(figsize=(10, 6))
    differences = merged_df['Score_Grader2'] - merged_df['total_score']
    sns.histplot(differences, bins=20)
    plt.xlabel('Score Difference (Manual - Automated)')
    plt.ylabel('Count')
    plt.title('Distribution of Grading Differences')
    plt.savefig(output_dir / 'score_differences_hist.png')
    plt.close()

def save_comparison_results(metrics, merged_df, output_dir):
    """Save comparison results to files."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save metrics
    with open(output_dir / 'comparison_metrics.txt', 'w') as f:
        f.write("Grading Comparison Metrics\n")
        f.write("==========================\n\n")
        for metric, value in metrics.items():
            f.write(f"{metric.replace('_', ' ').title()}: {value:.4f}\n")
    
    # Save detailed comparison
    comparison_df = merged_df[['folder', 'Score_Grader2', 'total_score']]
    comparison_df['difference'] = comparison_df['Score_Grader2'] - comparison_df['total_score']
    comparison_df['abs_difference'] = abs(comparison_df['difference'])
    comparison_df = comparison_df.sort_values('abs_difference', ascending=False)
    
    comparison_df.to_csv(output_dir / 'detailed_comparison.csv', index=False)

def main():
    # Load data
    print("Loading evaluation data...")
    manual_df, auto_df = load_data()
    
    # Normalize scores
    print("Normalizing scores...")
    manual_df, auto_df = normalize_scores(manual_df, auto_df)
    
    # Calculate metrics
    print("Calculating comparison metrics...")
    metrics, merged_df = calculate_metrics(manual_df, auto_df)
    
    # Create output directory
    output_dir = Path('comparison_results')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate visualizations
    print("Generating visualizations...")
    generate_visualizations(merged_df, output_dir)
    
    # Save results
    print("Saving comparison results...")
    save_comparison_results(metrics, merged_df, output_dir)
    
    # Print summary
    print("\nComparison Summary:")
    print(f"Number of submissions compared: {metrics['submissions_compared']}")
    print(f"Pearson correlation: {metrics['pearson_correlation']:.4f}")
    print(f"Spearman correlation: {metrics['spearman_correlation']:.4f}")
    print(f"Mean absolute error: {metrics['mean_absolute_error']:.4f}")
    print(f"Mean squared error: {metrics['mean_squared_error']:.4f}")
    print(f"\nDetailed results saved in: {output_dir}")

if __name__ == "__main__":
    main()