import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def analyze_student_data(input_path="students_cleaned.csv", output_dir="outputs"):
    df = pd.read_csv(input_path)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    # Summary statistics
    summary = df.describe(include="all")
    summary.to_csv(output_path / "summary_statistics.csv")

    # Insight 1: Distribution of average scores
    plt.figure(figsize=(8, 5))
    df["average_score"].hist(bins=10)
    plt.title("Average Score Distribution")
    plt.xlabel("Average Score")
    plt.ylabel("Number of Students")
    plt.tight_layout()
    plt.savefig(output_path / "average_score_distribution.png")
    plt.close()

    # Insight 2: Reading vs writing relationship
    plt.figure(figsize=(8, 5))
    plt.scatter(df["reading_score"], df["writing_score"])
    plt.title("Reading Score vs Writing Score")
    plt.xlabel("Reading Score")
    plt.ylabel("Writing Score")
    plt.tight_layout()
    plt.savefig(output_path / "reading_vs_writing.png")
    plt.close()

    # Insight 3: Average score by preparation course
    prep_avg = df.groupby("test_preparation_course")["average_score"].mean().sort_values()
    plt.figure(figsize=(8, 5))
    prep_avg.plot(kind="bar")
    plt.title("Average Score by Test Preparation Course")
    plt.xlabel("Test Preparation Course")
    plt.ylabel("Average Score")
    plt.tight_layout()
    plt.savefig(output_path / "prep_course_average_score.png")
    plt.close()

    # Save a small insights text file
    insights = []
    corr = df["reading_score"].corr(df["writing_score"])
    insights.append(f"Reading and writing scores are strongly positively related (correlation = {corr:.2f}).")

    prep_means = df.groupby("test_preparation_course")["average_score"].mean()
    if "completed" in prep_means.index and "none" in prep_means.index:
        diff = prep_means["completed"] - prep_means["none"]
        insights.append(f"Students who completed the preparation course scored about {diff:.2f} points higher on average.")

    top_band = (df["performance_level"] == "excellent").mean() * 100
    insights.append(f"{top_band:.1f}% of students are in the excellent performance band.")

    with open(output_path / "insights.txt", "w", encoding="utf-8") as f:
        for line in insights:
            f.write("- " + line + "\n")

    print("Analysis files saved in:", output_path.resolve())

if __name__ == "__main__":
    analyze_student_data()