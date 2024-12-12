import os
import subprocess

def print_welcome():
    print("""
Welcome to the UNIX 'sed' Command Training Game!
-------------------------------------------------
You'll be given a text and a task to modify it using the 'sed' command.
Type the appropriate 'sed' command to complete each task.

Example:
Input text: "Goodbye Moon"
Task: Replace "Moon" with "Stars"
Your command: sed 's/Moon/Stars/'

Type 'exit' to quit the game at any time.
For each task, you'll also get a quick guide on how to use 'sed' for that type of modification.
Let's get started!
    """)

def generate_task():
    tasks = [
        {
            "input": "Hello World",
            "task": "Replace 'World' with 'UNIX'",
            "solution": "s/World/UNIX/",
            "guide": "Use 's/old/new/' to substitute 'old' with 'new'."
        },
        {
            "input": "apple banana cherry",
            "task": "Replace 'banana' with 'grape'",
            "solution": "s/banana/grape/",
            "guide": "Use 's/old/new/' to substitute 'old' with 'new'."
        },
        {
            "input": "1,2,3,4,5",
            "task": "Delete all commas",
            "solution": "s/,//g",
            "guide": "Use 's/old//g' to globally delete all occurrences of 'old'."
        },
        {
            "input": "red green blue",
            "task": "Change 'green' to 'yellow'",
            "solution": "s/green/yellow/",
            "guide": "Use 's/old/new/' to substitute 'old' with 'new'."
        },
        {
            "input": "foo\nbar\nbaz",
            "task": "Append '-test' to every line",
            "solution": "s/$/-test/",
            "guide": "Use 's/$/new/' to append 'new' to the end of each line."
        },
        {
            "input": "abcd efgh ijkl",
            "task": "Change all spaces to underscores",
            "solution": "s/ /_/g",
            "guide": "Use 's/old/new/g' to globally substitute all occurrences of 'old' with 'new'."
        },
        {
            "input": "line1\nline2\nline3",
            "task": "Insert 'PREFIX-' at the start of every line",
            "solution": "s/^/PREFIX-/",
            "guide": "Use 's/^/new/' to prepend 'new' to the start of each line."
        },
        {
            "input": "name: John, age: 30, city: New York",
            "task": "Remove all occurrences of ': '",
            "solution": "s/: //g",
            "guide": "Use 's/old//g' to globally delete all occurrences of 'old'."
        },
        {
            "input": "hello123world456",
            "task": "Remove all digits",
            "solution": ["s/[0-9]//g", "s/\\d//g"],
            "guide": "Use 's/[pattern]//g' to delete all characters matching the pattern. \nAlternative: Use 's/\\d//g' for matching digits."
        },
        {
            "input": "abc\ndef\nghi",
            "task": "Replace every line with 'LINE'",
            "solution": "s/.*/LINE/",
            "guide": "Use 's/.*/new/' to replace the entire content of each line with 'new'."
        },
        {
            "input": "apple banana apple banana apple",
            "task": "Replace the second occurrence of 'apple' with 'grape'",
            "solution": "s/apple/grape/2",
            "guide": "Use 's/old/new/n' to replace only the nth occurrence of 'old'."
        },
        {
            "input": "line1\nline2",
            "task": "Replace 'line1\nline2' with 'combined'",
            "solution": "N;s/line1\\nline2/combined/",
            "guide": "Use 'N;' before 's/old/new/' to append the next line to the pattern space and apply substitutions across lines."
        },
        {
            "input": "line1\nline2\nskip\nline3",
            "task": "Delete lines containing 'skip'",
            "solution": "/skip/d",
            "guide": "Use '/pattern/d' to delete lines that match the pattern."
        },
        {
            "input": "line1\n\nline2",
            "task": "Replace empty lines with 'EMPTY'",
            "solution": "/^$/s/^$/EMPTY/",
            "guide": "Use '^$' to match empty lines."
        },
    ]
    return tasks

def execute_sed_command(input_text, user_command):
    try:
        # Build a shell command with echo piping into sed
        command = f"echo -e \"{input_text}\" | {user_command}"
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            return None, result.stderr.strip()
        return result.stdout.strip(), None
    except Exception as e:
        return None, str(e)

def main():
    print_welcome()
    tasks = generate_task()
    score = 0

    for i, task in enumerate(tasks):
        print(f"\nTask {i+1}:")
        print(f"Input text: \"{task['input']}\"")
        print(f"Task: {task['task']}")
        print(f"Guide: {task['guide']}")

        while True:
            user_command = input("Your 'sed' command (or type 'skip' to skip): ").strip()

            if user_command.lower() == 'exit':
                print("Thanks for playing! Goodbye!")
                return
            if user_command.lower() == 'skip':
                if isinstance(task['solution'], list):
                    print(f"The correct commands were: {', '.join([f'sed \"{sol}\"' for sol in task['solution']])}")
                else:
                    print(f"The correct command was: sed '{task['solution']}'")
                break

            if not user_command.startswith("sed "):
                print("Please start your command with 'sed'. Try again.")
                continue

            output, error = execute_sed_command(task['input'], user_command)

            if error:
                print(f"Error: {error}")
                continue

            if isinstance(task['solution'], list):
                expected_outputs = [execute_sed_command(task['input'], f"sed '{sol}'")[0] for sol in task['solution']]
                if output in expected_outputs:
                    print("Correct! Well done.")
                    score += 1
                    break
                else:
                    print("Incorrect. Try again.")
            else:
                expected_output, _ = execute_sed_command(task['input'], f"sed '{task['solution']}'")
                if output == expected_output:
                    print("Correct! Well done.")
                    score += 1
                    break
                else:
                    print("Incorrect. Try again.")

    print(f"\nYour final score: {score}/{len(tasks)}")
    print("Thanks for playing! Keep practicing your 'sed' skills!")

if __name__ == "__main__":
    main()