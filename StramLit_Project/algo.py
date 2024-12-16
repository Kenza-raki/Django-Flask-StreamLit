import streamlit as st
import matplotlib.pyplot as plt

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

def plot_fcfs_schedule(schedule, tasks):
    fig, ax = plt.subplots(figsize=(10, 6))

    for i, (start_time, execution_time) in enumerate(schedule):
        ax.barh(i, execution_time, left=start_time, height=0.8, label=f"Task {i + 1}")

    ax.set_xlabel("Time Units")
    ax.set_title("First-Come, First-Served (FCFS) Algorithm")
    ax.set_yticks(range(len(tasks)))
    ax.set_yticklabels([f"Task {i+1}" for i in range(len(tasks))])

    for i, (start_time, execution_time) in enumerate(schedule):
        ax.text(start_time + execution_time / 2, i, f"T{i + 1}", ha='center', va='center', color='white')

    ax.legend()
    st.pyplot(fig)

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

def plot_sjf_schedule(schedule, tasks):
    fig, ax = plt.subplots(figsize=(10, 6))

    for i, (start_time, execution_time) in enumerate(schedule):
        ax.barh(i, execution_time, left=start_time, height=0.8, label=f"Task {i + 1}")

    ax.set_xlabel("Time Units")
    ax.set_title("Shortest Job First (SJF) Algorithm")
    ax.set_yticks(range(len(tasks)))
    ax.set_yticklabels([f"Task {i+1}" for i in range(len(tasks))])

    for i, (start_time, execution_time) in enumerate(schedule):
        ax.text(start_time + execution_time / 2, i, f"T{i + 1}", ha='center', va='center', color='white')

    ax.legend()
    st.pyplot(fig)

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

def plot_llf_schedule(schedule, tasks):
    fig, ax = plt.subplots(figsize=(10, 6))

    for i, (start_time, execution_time) in enumerate(schedule):
        ax.barh(i, execution_time, left=start_time, height=0.8, label=f"Task {i + 1}")

    ax.set_xlabel("Time Units")
    ax.set_title("Least Laxity First (LLF) Algorithm")
    ax.set_yticks(range(len(tasks)))
    ax.set_yticklabels([f"Task {i+1}" for i in range(len(tasks))])

    for i, (start_time, execution_time) in enumerate(schedule):
        ax.text(start_time + execution_time / 2, i, f"T{i + 1}", ha='center', va='center', color='white')

    ax.legend()
    st.pyplot(fig)

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

def plot_rm_schedule(schedule, tasks):
    fig, ax = plt.subplots(figsize=(10, 6))

    for i, (start_time, execution_time) in enumerate(schedule):
        ax.barh(i, execution_time, left=start_time, height=0.8, label=f"Task {i + 1}")

    ax.set_xlabel("Time Units")
    ax.set_title("Rate Monotonic (RM) Algorithm")
    ax.set_yticks(range(len(tasks)))
    ax.set_yticklabels([f"Task {i+1}" for i in range(len(tasks))])

    for i, (start_time, execution_time) in enumerate(schedule):
        ax.text(start_time + execution_time / 2, i, f"T{i + 1}", ha='center', va='center', color='white')

    ax.legend()
    st.pyplot(fig)

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

def plot_dm_schedule(schedule, tasks):
    fig, ax = plt.subplots(figsize=(10, 6))

    for i, (start_time, execution_time) in enumerate(schedule):
        ax.barh(i, execution_time, left=start_time, height=0.8, label=f"Task {i + 1}")

    ax.set_xlabel("Time Units")
    ax.set_title("Deadline Monotonic (DM) Algorithm")
    ax.set_yticks(range(len(tasks)))
    ax.set_yticklabels([f"Task {i+1}" for i in range(len(tasks))])

    for i, (start_time, execution_time) in enumerate(schedule):
        ax.text(start_time + execution_time / 2, i, f"T{i + 1}", ha='center', va='center', color='white')

    ax.legend()
    st.pyplot(fig)

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

def plot_edf_schedule(schedule, tasks):
    fig, ax = plt.subplots(figsize=(10, 6))

    for i, (start_time, execution_time) in enumerate(schedule):
        ax.barh(i, execution_time, left=start_time, height=0.8, label=f"Task {i + 1}")

    ax.set_xlabel("Time Units")
    ax.set_title("Earliest Deadline First (EDF) Algorithm")
    ax.set_yticks(range(len(tasks)))
    ax.set_yticklabels([f"Task {i+1}" for i in range(len(tasks))])

    for i, (start_time, execution_time) in enumerate(schedule):
        ax.text(start_time + execution_time / 2, i, f"T{i + 1}", ha='center', va='center', color='white')

    ax.legend()
    st.pyplot(fig)

# Streamlit Interface
st.title("Task Scheduling Algorithms")
algorithm = st.sidebar.selectbox("Choose a Scheduling Algorithm", 
    ["FCFS", "SJF", "LLF", "RM", "DM", "EDF"])

tasks_input = st.text_area(
    "Enter Tasks", 
    value="(0, 3), (2, 5), (4, 2), (6, 4)",
    height=100
)

def parse_tasks(input_str):
    try:
        # Remove unnecessary whitespace and split the input properly
        tasks = [tuple(map(int, t.strip(" ()").split(","))) for t in input_str.strip().split("),")]
        return tasks
    except Exception as e:
        st.error(f"Error parsing tasks: {e}")
        return []


tasks = parse_tasks(tasks_input)

if st.button(f"Run {algorithm}"):
    if tasks:
        if algorithm == "FCFS":
            schedule = fcfs_algorithm(tasks)
            plot_fcfs_schedule(schedule, tasks)
        elif algorithm == "SJF":
            schedule = sjf_algorithm(tasks)
            plot_sjf_schedule(schedule, tasks)
        elif algorithm == "LLF":
            schedule = llf_algorithm(tasks)
            plot_llf_schedule(schedule, tasks)
        elif algorithm == "RM":
            schedule = rm_algorithm(tasks)
            plot_rm_schedule(schedule, tasks)
        elif algorithm == "DM":
            schedule = dm_algorithm(tasks)
            plot_dm_schedule(schedule, tasks)
        elif algorithm == "EDF":
            schedule = edf_algorithm(tasks)
            plot_edf_schedule(schedule, tasks)
    else:
        st.error("Please enter valid tasks.")
