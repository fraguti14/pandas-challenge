import pandas as pd
from pathlib import Path

# Paths
school_data_to_load = Path("Resources/schools_complete.csv")
student_data_to_load = Path("Resources/students_complete.csv")

# Read School & create df's
school_data = pd.read_csv(school_data_to_load)
student_data = pd.read_csv(student_data_to_load)

# Combine into 1 df
school_data_complete = pd.merge(student_data, school_data, how="left", on=["school_name", "school_name"])
school_data_complete.head()

# District key metrics
total_schools = school_data_complete["school_name"].nunique()
total_students = school_data_complete["Student ID"].nunique()
total_budget = school_data["budget"].sum()
average_math_score = school_data_complete["math_score"].mean()
average_reading_score = school_data_complete["reading_score"].mean()

# Percentages passing math|reading|overall
passing_math = (school_data_complete["math_score"] >= 70).mean() * 100
passing_reading = (school_data_complete["reading_score"] >= 70).mean() * 100
overall_passing = ((school_data_complete["math_score"] >= 70) & (school_data_complete["reading_score"] >= 70)).mean() * 100
# Creating dictionary
district_summary = {
    "Total Schools": [total_schools],
    "Total Students": [total_students],
    "Total Budget": [total_budget],
    "Average Math Score": [average_math_score],
    "Average Reading Score": [average_reading_score],
    "% Passing Math": [passing_math],
    "% Passing Reading": [passing_reading],
    "% Overall Passing": [overall_passing]
}

# Create df
district_summary = pd.DataFrame(district_summary)

# Display df
district_summary

# Group data by school
by_school = school_data_complete.groupby("school_name")
# School key metrics
school_types = school_data.set_index("school_name")["type"]
total_students_per_school = by_school["Student ID"].count()
total_school_budget = school_data.set_index("school_name")["budget"]
per_student_budget = total_school_budget / total_students_per_school
average_math_score_per_school = by_school["math_score"].mean()
average_reading_score_per_school = by_school["reading_score"].mean()

# Percentages passing math|reading|overall
passing_math_per_school = (school_data_complete[school_data_complete["math_score"] >= 70]
                           .groupby("school_name")["Student ID"].count() / total_students_per_school) * 100

passing_reading_per_school = (school_data_complete[school_data_complete["reading_score"] >= 70]
                              .groupby("school_name")["Student ID"].count() / total_students_per_school) * 100

overall_passing_per_school = (school_data_complete[(school_data_complete["math_score"] >= 70)
                                                   & (school_data_complete["reading_score"] >= 70)]
                             .groupby("school_name")["Student ID"].count() / total_students_per_school) * 100
# Creating dictionary
school_summary = {
    "School Type": school_types,
    "Total Students": total_students_per_school,
    "Total School Budget": total_school_budget,
    "Per Student Budget": per_student_budget,
    "Average Math Score": average_math_score_per_school,
    "Average Reading Score": average_reading_score_per_school,
    "% Passing Math": passing_math_per_school,
    "% Passing Reading": passing_reading_per_school,
    "% Overall Passing": overall_passing_per_school
}

# Create df
school_summary = pd.DataFrame(school_summary)

# Display df
school_summary

# Sorting schools by % overall passing - Get top 5, descending, sort_values
top_schools = school_summary.sort_values("% Overall Passing", ascending=False).head(5)

# Display df
top_schools

# Sorting schools by % overall passing - Get bottom 5, ascending, sort_values
bottom_schools = school_summary.sort_values("% Overall Passing", ascending=True).head(5)

# Display df
bottom_schools

# Avg math scores by grade level - pivot_table
math_scores_by_grade = pd.pivot_table(student_data, values='math_score',
                                      index='school_name', columns='grade', aggfunc='mean',
                                      fill_value=0, dropna=False)
# Reordering columns
math_scores_by_grade = math_scores_by_grade[['9th', '10th', '11th', '12th']]

# Display df
math_scores_by_grade

# Avg reading scores by grade level - pivot_table
reading_scores_by_grade = pd.pivot_table(student_data, values='reading_score',
                                         index='school_name', columns='grade', aggfunc='mean',
                                         fill_value=0, dropna=False)
# Reordering columns
reading_scores_by_grade = reading_scores_by_grade[['9th', '10th', '11th', '12th']]

# Display df
reading_scores_by_grade

# Create bins and labels for spending ranges
spending_bins = [0, 585, 630, 645, 680]
labels = ["<$585", "$585-630", "$630-645", "$645-680"]

# Categorize spending based on the bins - .cut
school_summary["Spending Ranges (Per Student)"] = pd.cut(school_summary["Per Student Budget"], spending_bins, labels=labels)

# Mean scores per spending range
spending_math_scores = school_summary.groupby(["Spending Ranges (Per Student)"])["Average Math Score"].mean()
spending_reading_scores = school_summary.groupby(["Spending Ranges (Per Student)"])["Average Reading Score"].mean()
spending_passing_math = school_summary.groupby(["Spending Ranges (Per Student)"])["% Passing Math"].mean()
spending_passing_reading = school_summary.groupby(["Spending Ranges (Per Student)"])["% Passing Reading"].mean()
overall_passing_spending = school_summary.groupby(["Spending Ranges (Per Student)"])["% Overall Passing"].mean()

# Creating dictionary
spending_summary = {
    "Average Math Score": spending_math_scores,
    "Average Reading Score": spending_reading_scores,
    "% Passing Math": spending_passing_math,
    "% Passing Reading": spending_passing_reading,
    "% Overall Passing": overall_passing_spending
}

# Create df
spending_summary = pd.DataFrame(spending_summary)

# Display df
spending_summary

# Create bins and labels for school size ranges
size_bins = [0, 1000, 2000, 5000]
size_labels = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]

# Categorize school size based on the bins - .cut
school_summary["School Size"] = pd.cut(school_summary["Total Students"], size_bins, labels=size_labels)

# Mean scores per school size range
size_math_scores = school_summary.groupby(["School Size"])["Average Math Score"].mean()
size_reading_scores = school_summary.groupby(["School Size"])["Average Reading Score"].mean()
size_passing_math = school_summary.groupby(["School Size"])["% Passing Math"].mean()
size_passing_reading = school_summary.groupby(["School Size"])["% Passing Reading"].mean()
overall_passing_size = school_summary.groupby(["School Size"])["% Overall Passing"].mean()

# Creating dictionary
size_summary = {
    "Average Math Score": size_math_scores,
    "Average Reading Score": size_reading_scores,
    "% Passing Math": size_passing_math,
    "% Passing Reading": size_passing_reading,
    "% Overall Passing": overall_passing_size
}

# Create df
size_summary = pd.DataFrame(size_summary)

# Display df
size_summary

# Mean for school performance based on school type
type_math_scores = school_summary.groupby("School Type")["Average Math Score"].mean()
type_reading_scores = school_summary.groupby("School Type")["Average Reading Score"].mean()
type_passing_math = school_summary.groupby("School Type")["% Passing Math"].mean()
type_passing_reading = school_summary.groupby("School Type")["% Passing Reading"].mean()
overall_passing_type = school_summary.groupby("School Type")["% Overall Passing"].mean()

# Create dictionary
type_summary = {
    "Average Math Score": type_math_scores,
    "Average Reading Score": type_reading_scores,
    "% Passing Math": type_passing_math,
    "% Passing Reading": type_passing_reading,
    "% Overall Passing": overall_passing_type
}

# Create df
type_summary = pd.DataFrame(type_summary)

# Display df
type_summary
