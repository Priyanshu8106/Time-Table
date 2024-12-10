import pandas as pd
import random
import math

# Subjects and constraints
theory_subjects = ['Data Structures', 'Algorithms', 'Operating Systems', 'Databases', 'Software Engineering']
lab_subjects = ['DS Lab', 'OS Lab', 'DBMS Lab', 'Software Engineering Lab', 'Algorithms Lab']
time_slots_theory = ['9-10 AM', '10-11 AM', '11-12 PM', '12-1 PM']
time_slots_lab = ['2-3 PM', '3-4 PM', '4-5 PM']

# Weekly schedule structure
schedule = {
    'Day': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
    'Theory Classes': [
        ['Data Structures', 'Algorithms', 'Operating Systems'],
        ['Algorithms', 'Databases', 'Software Engineering'],
        ['Data Structures', 'Operating Systems'],
        ['Databases', 'Software Engineering'],
        ['Algorithms', 'Software Engineering'],
    ],
    'Lab Classes': [
        ['DS Lab'],
        ['OS Lab'],
        ['DBMS Lab'],
        ['Software Engineering Lab'],
        ['Algorithms Lab'],
    ]
}

# Cost calculation
def calculate_cost(timetable):
    cost = 0
    for day in timetable.values():
        day_slots = list(day['Theory Classes'].values()) + list(day['Lab Classes'].values())
        if day_slots.count("No Class") > len(time_slots_theory) + len(time_slots_lab):
            cost += 1
    return cost

# Generate a random timetable
def generate_random_timetable():
    timetable = {day: {'Theory Classes': {}, 'Lab Classes': {}} for day in schedule['Day']}
    for day, theory_classes, lab_classes in zip(schedule['Day'], schedule['Theory Classes'], schedule['Lab Classes']):
        theory_slots = {time: "No Class" for time in time_slots_theory}
        lab_slots = {time: "No Class" for time in time_slots_lab}
        for i, subject in enumerate(theory_classes):
            theory_slots[time_slots_theory[i]] = subject
        for i, subject in enumerate(lab_classes):
            lab_slots[time_slots_lab[i]] = subject
        timetable[day]['Theory Classes'] = theory_slots
        timetable[day]['Lab Classes'] = lab_slots
    return timetable

# Simulated annealing algorithm
def simulated_annealing(max_iterations=1000, initial_temp=100, cooling_rate=0.01):
    current_timetable = generate_random_timetable()
    current_cost = calculate_cost(current_timetable)
    temperature = initial_temp
    
    for iteration in range(max_iterations):
        new_timetable = generate_random_timetable()
        new_cost = calculate_cost(new_timetable)
        if new_cost < current_cost or math.exp((current_cost - new_cost) / temperature) > random.random():
            current_timetable, current_cost = new_timetable, new_cost
        temperature *= (1 - cooling_rate)
        if temperature <= 0:
            break

    return current_timetable

# Generate and format the final timetable
optimized_timetable = simulated_annealing()
df = pd.DataFrame.from_dict(optimized_timetable, orient='index')
print(df.to_markdown())
