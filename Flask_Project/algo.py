from flask import Flask, render_template, request, jsonify, redirect, url_for
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

# FCFS Algorithm
def fcfs_algorithm(tasks):
    tasks = sorted(tasks, key=lambda x: x[0])  # Sort by arrival time
    schedule = []
    current_time = 0

    for task in tasks:
        arrival_time, execution_time = task
        if current_time < arrival_time:
            current_time = arrival_time
        schedule.append((current_time, execution_time))
        current_time += execution_time

    return schedule

# SJF Algorithm
def sjf_algorithm(tasks):
    tasks = sorted(tasks, key=lambda x: x[1])  # Sort by execution time
    current_time = 0
    schedule = []

    for task in tasks:
        arrival_time, execution_time = task
        if current_time < arrival_time:
            current_time = arrival_time
        schedule.append((current_time, execution_time))
        current_time += execution_time

    return schedule

# LLF Algorithm
def llf_algorithm(tasks):
    tasks = sorted(tasks, key=lambda x: x[2])  # Sort by deadline
    current_time = 0
    schedule = []

    for task in tasks:
        execution_time, deadline, _ = task
        schedule.append((current_time, execution_time))
        current_time += execution_time

    return schedule

# RM Algorithm
def rm_algorithm(tasks):
    tasks = sorted(tasks, key=lambda x: x[1])  # Sort by period
    schedule = []
    time = 0

    while time < 100:
        for task in tasks:
            execution_time, period, _ = task
            if time % period == 0:
                schedule.append((time, execution_time))
                time += execution_time
                break
        else:
            time += 1

    return schedule

# DM Algorithm
def dm_algorithm(tasks):
    tasks = sorted(tasks, key=lambda x: x[2])  # Sort by deadline
    current_time = 0
    schedule = []

    for task in tasks:
        execution_time, _, deadline = task
        schedule.append((current_time, execution_time))
        current_time += execution_time

    return schedule

# EDF Algorithm
def edf_algorithm(tasks):
    tasks = sorted(tasks, key=lambda x: x[2])  # Sort by absolute deadline
    current_time = 0
    schedule = []

    for task in tasks:
        execution_time, _, deadline = task
        schedule.append((current_time, execution_time))
        current_time += execution_time

    return schedule

# Function to generate and encode the plot as base64
def plot_schedule(schedule, tasks, algorithm_name):
    fig, ax = plt.subplots(figsize=(10, 6))

    for i, (start_time, execution_time) in enumerate(schedule):
        ax.barh(i, execution_time, left=start_time, height=0.8, label=f"Task {i + 1}")

    ax.set_xlabel("Time Units")
    ax.set_title(f"{algorithm_name} Algorithm")
    ax.set_yticks(range(len(tasks)))
    ax.set_yticklabels([f"Task {i+1}" for i in range(len(tasks))])

    for i, (start_time, execution_time) in enumerate(schedule):
        ax.text(start_time + execution_time / 2, i, f"T{i + 1}", ha='center', va='center', color='white')

    ax.legend()

    # Save the plot to a BytesIO object and encode as base64
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    img_str = base64.b64encode(buf.getvalue()).decode("utf-8")
    buf.close()

    return img_str

# Route to render the form and receive input
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        tasks_input = request.form.get("tasks_input")
        algorithm = request.form.get("algorithm")

        tasks = parse_tasks(tasks_input)
        if not tasks:
            return render_template("index.html", error="Invalid task input format")

        if algorithm == "FCFS":
            schedule = fcfs_algorithm(tasks)
            img_str = plot_schedule(schedule, tasks, "First-Come, First-Served")
        elif algorithm == "SJF":
            schedule = sjf_algorithm(tasks)
            img_str = plot_schedule(schedule, tasks, "Shortest Job First")
        elif algorithm == "LLF":
            schedule = llf_algorithm(tasks)
            img_str = plot_schedule(schedule, tasks, "Least Laxity First")
        elif algorithm == "RM":
            schedule = rm_algorithm(tasks)
            img_str = plot_schedule(schedule, tasks, "Rate Monotonic")
        elif algorithm == "DM":
            schedule = dm_algorithm(tasks)
            img_str = plot_schedule(schedule, tasks, "Deadline Monotonic")
        elif algorithm == "EDF":
            schedule = edf_algorithm(tasks)
            img_str = plot_schedule(schedule, tasks, "Earliest Deadline First")

        return render_template("index.html", img_str=img_str, tasks_input=tasks_input, algorithm=algorithm)

    return render_template("index.html", img_str=None)

# Function to parse the task input
def parse_tasks(input_str):
    try:
        tasks = [tuple(map(int, t.strip(" ()").split(","))) for t in input_str.strip().split("),")]
        return tasks
    except Exception as e:
        return []

if __name__ == "__main__":
    app.run(debug=True)
