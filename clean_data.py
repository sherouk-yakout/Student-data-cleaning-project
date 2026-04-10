import pandas as pd

def clean_student_data(input_path="students_raw.csv", output_path="students_cleaned.csv"):
    df = pd.read_csv(input_path)

    # Standardize text columns
    text_cols = [
        "student_id",
        "gender",
        "parental_level_of_education",
        "lunch",
        "test_preparation_course",
    ]
    for col in text_cols:
        df[col] = df[col].astype(str).str.strip()

    # Normalize category values
    df["student_id"] = df["student_id"].str.upper()
    df["gender"] = df["gender"].str.lower().replace({
        "female": "female",
        "male": "male"
    })
    df["lunch"] = df["lunch"].str.lower().replace({
        "standard": "standard",
        "free/reduced": "free/reduced"
    })
    df["test_preparation_course"] = df["test_preparation_course"].str.lower().replace({
        "completed": "completed",
        "none": "none"
    })
    df["parental_level_of_education"] = (
        df["parental_level_of_education"]
        .str.lower()
        .replace({
            "high school": "high school",
            "bachelor's degree": "bachelor's degree",
            "master's degree": "master's degree",
            "some college": "some college",
            "associate's degree": "associate's degree",
        })
    )

    # Convert numeric columns safely
    score_cols = ["math_score", "reading_score", "writing_score"]
    for col in score_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Remove duplicates
    df = df.drop_duplicates()

    # Fill missing scores with column medians
    for col in score_cols:
        df[col] = df[col].fillna(df[col].median())

    # Add average score column
    df["average_score"] = df[score_cols].mean(axis=1).round(2)

    # Add performance label
    def performance_label(avg):
        if avg >= 85:
            return "excellent"
        elif avg >= 70:
            return "good"
        elif avg >= 55:
            return "average"
        return "needs improvement"

    df["performance_level"] = df["average_score"].apply(performance_label)

    df.to_csv(output_path, index=False)
    print("Cleaned dataset saved to:", output_path)
    print(df.head())

if __name__ == "__main__":
    clean_student_data()