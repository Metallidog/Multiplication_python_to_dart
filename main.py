import os
import random


class MultiplicationSet:
    def __init__(self, a, b, attempts, correct):
        self.a = a
        self.b = b
        self.answer = str(a*b)
        self.attempts = attempts
        self.correct = correct
        if attempts:
            self.proficiency = correct/attempts
        else:
            self.proficiency = 0

    def update(self, is_correct):
        self.attempts += 1
        if is_correct:
            self.correct += 1
        self.proficiency = float(self.correct)/self.attempts


class UserProgress:

    subset_names = [str(a)+str(b) for a in range(2, 16) for b in range(4)]

    def __init__(self, name, subset):
        self.name = name
        self.progress = {}
        self.current_subset = subset
        self.problem_set = []
        self.missed = []
        self.choice_level = 0
        self.sets = {}
        self.create_sets()

    def save_progress(self):
        """
        Creates a text file.
        First line of the text file is the users current_subset
        Every subsequent line is the data used to create each Multiplication Set
        """
        filename = f'{self.name}.txt'
        content = '\n'.join(
            f'{key}:{value.attempts}:{value.correct}:{value.proficiency}'
            for key, value in self.progress.items()
        )
        content = f'{self.current_subset}\n' + content
        with open(filename, 'w') as file:
            file.write(content)

    def create_sets(self):
        """
        This function populates the dictionary self.sets. {subset:[problems]}
        subset: a string (eg: '30') which designates the name of a subset
        problems: a list of problems as strings (eg '3*5')
        """
        groups = ([0, 1, 2, 3,], [4, 5, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15])
        for sub_name in UserProgress.subset_names:
            self.sets[sub_name] = []
            for b in groups[int(sub_name[-1])]:  # subset '20' = index 0 etc.
                self.sets[sub_name].append(f'{sub_name[:-1]}*{b}')

    def update_subset(self):
        pass
        index_subset = UserProgress.subset_names.index(self.current_subset)
        index_subset += 1
        self.current_subset = UserProgress.subset_names[index_subset]



def load_progress(name):
    """
    Returns a UserProgress Object.
    If the file with the name exists, we load the progress Dictionary with the data from the file. Then create
    the UserObject with the name of the file and dump the progress Dictionary into UserProgress.progress.
    If the file does not exist, we create a UserObject with the name. The UserProgress.progress attribute will be empty.
    :param name:
    :return UserProgress Object:
    """
    filename = f'{name}.txt'
    if os.path.exists(filename):
        progress = {}
        with open(filename, 'r') as file:
            subset = file.readline().strip() #first line in the text file
            contents = file.readlines()
            for line in contents:
                parts = line.strip().split(':')
                key = parts[0]
                attempts = int(parts[1])
                correct = int(parts[2])
                parts_split = key.split('*')
                a = int(parts_split[0])
                b = int(parts_split[1])
                progress[key] = MultiplicationSet(a, b, attempts=attempts, correct=correct)
        user_progress = UserProgress(name, subset)
        user_progress.progress = progress
        return user_progress
    else:
        return UserProgress(name, subset='20')


def determine_problem_set(up):
    new_set = []
    for i in range(2):
        random.shuffle(up.problem_set)
        if i == 1 and up.problem_set[0] == new_set[-1]:  # making sure no 2 questions in a row the same
            new_set.reverse()
        new_set += up.problem_set
    return new_set


def determine_choices(up, problem):
    print(f'Choice Level: {up.choice_level}')
    possible_choices = []  # This will hold the multiple choice questions
    num_choices = up.choice_level * 2
    mult = int(up.current_subset[:-1])
    subset_level = int(up.current_subset[-1])
    print("subset level", subset_level)
    if subset_level == 0:
        possible_choices = [f'{mult*x}' for x in range(8)]
    if subset_level == 1:
        possible_choices = [f'{mult*x}' for x in range(12)]
    if subset_level >1:
        possible_choices = [f'{mult*x}' for x in range(4, 16)]
    print("possible choices", possible_choices)
    possible_choices.remove(up.progress[problem].answer)  # removes correct answer from possible choices
    random.shuffle(possible_choices)
    list_of_choices = [up.progress[problem].answer]  # starts the list of choices with the correct answer
    for i in range(num_choices-1):
        list_of_choices.append(possible_choices.pop())
    random.shuffle(list_of_choices)
    return list_of_choices


def answer_problems(up):
    problem_set = determine_problem_set(up)
    for problem in problem_set:
        a, b = problem.split('*')
        if problem not in up.progress:
            up.progress[problem] = MultiplicationSet(int(a), int(b), 0, 0)
        choices = determine_choices(up, problem)
        print()
        for choice in choices:
            print(f"Choice: {choice}")
        if up.current_subset != "20":
            attempt = input(f"What is {a} X {b}:  ")
        else:
            attempt = up.progress[problem].answer
        if attempt == up.progress[problem].answer:
            up.progress[problem].update(True)
            print("That is CORRECT")
        else:
            up.progress[problem].update(False)
            print(f"That is incorrect. {a} X {b} = {up.progress[problem].answer}")
            up.missed.append(problem)
    up.save_progress()


def main_program():
    name = input("Enter your name:  ")
    up = load_progress(name)
    up.problem_set = up.sets[up.current_subset]
    print("problemswet", up.problem_set)
    while up.problem_set:
        answer_problems(up)
        up.problem_set = up.missed[:]
        up.missed = []
        if not up.problem_set and up.choice_level <= 4:  # if problem_set is empty and not ready to go to next set
            up.choice_level += 1
            up.problem_set = up.sets[up.current_subset]
        if up.choice_level>4:
            up.choice_level = 0
            up.update_subset()
            up.problem_set = up.sets[up.current_subset]

main_program()
