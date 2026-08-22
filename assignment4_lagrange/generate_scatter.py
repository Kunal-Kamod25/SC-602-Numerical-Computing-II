import matplotlib.pyplot as plt
from lagrange_toolkit.data_loader import load_points_from_csv
import os

def main():
    file_path = "dataset/student_academic_stress_interpolation_150.csv"
    x_vals, y_vals, _ = load_points_from_csv(
        file_path, 
        x_column="Study_Hours", 
        y_column="Academic_Stress_Score"
    )
    
    plt.figure(figsize=(10, 6))
    plt.scatter(x_vals, y_vals, color='blue', alpha=0.6, edgecolors='k', label='Dataset Points')
    plt.title('Full 150-Point Dataset Scatter Plot')
    plt.xlabel('Study Hours')
    plt.ylabel('Academic Stress Score')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    
    os.makedirs('outputs', exist_ok=True)
    out_path = 'outputs/full_dataset_scatter.png'
    plt.savefig(out_path, dpi=150, bbox_inches='tight')
    print(f"Scatter plot saved to {out_path}")

if __name__ == '__main__':
    main()
