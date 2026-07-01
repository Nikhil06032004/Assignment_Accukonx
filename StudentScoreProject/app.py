import os
import random
import requests
import matplotlib.pyplot as plt

# ---------------- CONFIGURATION ---------------- #

API_URL = "https://dummyjson.com/users?limit=10"
OUTPUT_FOLDER = "output"
CHART_FILE = os.path.join(OUTPUT_FOLDER, "student_scores.png")


# ---------------- FETCH DATA ---------------- #

def fetch_students():
    response = requests.get(API_URL)
    response.raise_for_status()

    users = response.json()["users"]

    students = []

    for user in users:
        students.append({
            "name": f"{user['firstName']} {user['lastName']}",
            "score": random.randint(60, 100)
        })

    return students


# ---------------- PROCESS DATA ---------------- #

def calculate_average(students):
    total = sum(student["score"] for student in students)
    return total / len(students)


# ---------------- VISUALIZATION ---------------- #

def create_chart(students):
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    names = [student["name"] for student in students]
    scores = [student["score"] for student in students]

    plt.figure(figsize=(12, 6))

    plt.bar(names, scores)

    plt.title("Student Test Scores", fontsize=16)
    plt.xlabel("Students", fontsize=12)
    plt.ylabel("Score", fontsize=12)

    plt.xticks(rotation=30, ha="right")

    plt.grid(axis="y", linestyle="--", alpha=0.5)

    plt.tight_layout()

    plt.savefig(CHART_FILE)
    plt.show()

# ---------------- MAIN ---------------- #

def main():
    print("=" * 50)
    print("Student Score Analysis")
    print("=" * 50)

    students = fetch_students()

    average = calculate_average(students)

    print("\nStudent Scores\n")

    for student in students:
        print(f"{student['name']:<25} {student['score']}")

    print(f"\nAverage Score: {average:.2f}")

    create_chart(students)

    print(f"\nBar chart saved to: {CHART_FILE}")


if __name__ == "__main__":
    main()
