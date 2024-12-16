from django.shortcuts import render
import matplotlib.pyplot as plt
import io
import base64

# Parse task input (assuming tasks input is in the form of 'arrival_time,execution_time,period,deadline')
def parse_tasks(input_str):
    try:
        tasks = [tuple(map(int, t.strip(" ()").split(","))) for t in input_str.strip().split("),")]
        return tasks
    except Exception as e:
        return []

# FCFS (First-Come, First-Served) Algorithm
def fcfs_algorithm(tasks):
    tasks = sorted(tasks, key=lambda x: x[0])  # Sort by arrival time
    current_time = 0
    schedule = []
    
    for task in tasks:
        arrival_time, execution_time = task
        if current_time < arrival_time:
            current_time = arrival_time
        schedule.append((current_time, execution_time))
        current_time += execution_time

    return schedule

# SJF (Shortest Job First) Algorithm
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

# RM (Rate Monotonic Scheduling) Algorithm
def rm_algorithm(tasks):
    tasks = sorted(tasks, key=lambda x: x[1])  # Sort by period (execution time)
    current_time = 0
    schedule = []

    for task in tasks:
        arrival_time, execution_time, period = task
        if current_time < arrival_time:
            current_time = arrival_time
        schedule.append((current_time, execution_time))
        current_time += execution_time

    return schedule

# DM (Deadline Monotonic Scheduling) Algorithm
def dm_algorithm(tasks):
    tasks = sorted(tasks, key=lambda x: x[2])  # Sort by deadline
    current_time = 0
    schedule = []

    for task in tasks:
        arrival_time, execution_time, deadline = task
        if current_time < arrival_time:
            current_time = arrival_time
        schedule.append((current_time, execution_time))
        current_time += execution_time

    return schedule

# EJB (Earliest Job First) Algorithm
def ejb_algorithm(tasks):
    tasks = sorted(tasks, key=lambda x: x[0])  # Sort by arrival time
    current_time = 0
    schedule = []

    for task in tasks:
        arrival_time, execution_time = task
        if current_time < arrival_time:
            current_time = arrival_time
        schedule.append((current_time, execution_time))
        current_time += execution_time

    return schedule

# LLF (Least Laxity First) Algorithm
def llf_algorithm(tasks):
    tasks = sorted(tasks, key=lambda x: x[0])  # Sort by arrival time
    current_time = 0
    schedule = []

    while tasks:
        min_laxity_task = min(tasks, key=lambda x: x[2] - (current_time - x[0]))  # Least laxity
        arrival_time, execution_time, deadline = min_laxity_task
        tasks.remove(min_laxity_task)

        if current_time < arrival_time:
            current_time = arrival_time
        schedule.append((current_time, execution_time))
        current_time += execution_time

    return schedule

# Plotting function for all algorithms
def plot_schedule(schedule, tasks, algorithm_name):
    fig, ax = plt.subplots(figsize=(10, 6))

    for i, (start_time, execution_time) in enumerate(schedule):
        ax.barh(i, execution_time, left=start_time, height=0.8, label=f"Task {i + 1}")

    ax.set_xlabel("Time Units")
    ax.set_title(f"{algorithm_name} Algorithm")
    ax.set_yticks(range(len(tasks)))
    ax.set_yticklabels([f"Task {i + 1}" for i in range(len(tasks))])

    for i, (start_time, execution_time) in enumerate(schedule):
        ax.text(start_time + execution_time / 2, i, f"T{i + 1}", ha='center', va='center', color='white')

    ax.legend()

    # Convert the plot to base64 string
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    img_str = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()

    return img_str

# View to handle scheduling algorithms
def schedule_view(request):
    algorithm = None
    tasks_input = ""
    img_str = ""

    if request.method == "POST":
        algorithm = request.POST.get("algorithm")
        tasks_input = request.POST.get("tasks_input")

        # Parse input tasks
        tasks = parse_tasks(tasks_input)

        if algorithm == "FCFS":
            schedule = fcfs_algorithm(tasks)
            img_str = plot_schedule(schedule, tasks, "First-Come, First-Served (FCFS)")
        elif algorithm == "SJF":
            schedule = sjf_algorithm(tasks)
            img_str = plot_schedule(schedule, tasks, "Shortest Job First (SJF)")
        elif algorithm == "RM":
            schedule = rm_algorithm(tasks)
            img_str = plot_schedule(schedule, tasks, "Rate Monotonic (RM)")
        elif algorithm == "DM":
            schedule = dm_algorithm(tasks)
            img_str = plot_schedule(schedule, tasks, "Deadline Monotonic (DM)")
        elif algorithm == "EJB":
            schedule = ejb_algorithm(tasks)
            img_str = plot_schedule(schedule, tasks, "Earliest Job First (EJB)")
        elif algorithm == "LLF":
            schedule = llf_algorithm(tasks)
            img_str = plot_schedule(schedule, tasks, "Least Laxity First (LLF)")

    return render(request, 'scheduler/schedule.html', {
        'algorithm': algorithm, 'tasks_input': tasks_input, 'img_str': img_str
    })
