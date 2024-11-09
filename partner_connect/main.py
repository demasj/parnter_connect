import tkinter as tk
import json
import random
import os

DISPLAYED_QUESTIONS_FILE = 'displayed_questions.json'

def load_questions(filename):
    """
    Load questions from a JSON file.

    Args:
        filename (str): The path to the JSON file containing questions.

    Returns:
        list: A list of questions, where each question is a dictionary.
    """
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_displayed_questions(displayed_questions):
    """
    Save the set of displayed question IDs to a JSON file.

    Args:
        displayed_questions (set): A set of question IDs that have been displayed.
    """
    with open(DISPLAYED_QUESTIONS_FILE, 'w', encoding='utf-8') as file:
        json.dump(list(displayed_questions), file)

def load_displayed_questions():
    """
    Load the set of displayed question IDs from a JSON file.

    Returns:
        set: A set of question IDs that have been displayed.
    """
    if os.path.exists(DISPLAYED_QUESTIONS_FILE):
        with open(DISPLAYED_QUESTIONS_FILE, 'r', encoding='utf-8') as file:
            try:
                return set(json.load(file))
            except json.JSONDecodeError:
                return set()
    return set()

def display_random_question():
    """
    Display a random question from the available questions.

    This function selects a random question from the list of questions that have
    not yet been displayed. If all questions have been displayed, it updates the
    UI to indicate completion. The selected question is added to the set of
    displayed questions, which is then saved to a file. The question and its
    category are displayed on the UI.
    """
    global questions, displayed_questions, category_value_label, question_value_label

    # Filter questions that have an 'id' key and are not in displayed_questions
    available_questions = [q for q in questions if 'id' in q and q['id'] not in displayed_questions]

    if not available_questions:
        question_value_label.config(text="Goed gedaan! Jullie hebben alle vragen besproken."         
        "Jullie zijn nu beter met elkaar verbonden. Hou dit vast en breng het geleerde in de praktijk!"
        " ❤ ❤ ❤ ")
        category_value_label.config(text="")

        # Check if the file exists
        if os.path.exists(DISPLAYED_QUESTIONS_FILE):
            # Empty the file if it exists
            with open(DISPLAYED_QUESTIONS_FILE, 'w') as file:
                pass  # Opening in 'w' mode truncates the file to zero length
        return

    question = random.choice(available_questions)
    displayed_questions.add(question['id'])
    save_displayed_questions(displayed_questions)

    category_value_label.config(text=question.get('categorie', ''))
    question_value_label.config(text=question.get('vraag', ''))


def setup_gui():
    """
    Set up the GUI for displaying random questions.

    This function initializes the GUI components for the Partner Connect application,
    loading questions and displayed questions from their respective JSON files. It
    ensures that the displayed questions are reset if all questions have been shown.
    """
    global questions, displayed_questions, category_value_label, question_value_label

    questions = load_questions('partner_connect/vragen.json')
    displayed_questions = load_displayed_questions()

    # Reset displayed questions if all have been taken
    if len(displayed_questions) == len(questions):
        displayed_questions.clear()
        save_displayed_questions(displayed_questions)

    root = tk.Tk()
    root.title("Partner Connect - Random vragen")
    root.geometry("800x600")

    large_font = ("Arial", 14)
    large_font_bold = ("Arial", 14, "bold")

    frame = tk.Frame(root)
    frame.pack(pady=20, fill=tk.BOTH, expand=True)
    frame.grid_columnconfigure(0, weight=1)

    category_label = tk.Label(frame, font=large_font)
    category_label.grid(row=0, column=0, sticky="nsew")

    category_value_label = tk.Label(frame, font=large_font_bold)
    category_value_label.grid(row=1, column=0, sticky="nsew")

    question_label = tk.Label(frame, font=large_font)
    question_label.grid(row=3, column=0, sticky="nsew")

    question_value_label = tk.Label(frame, wraplength=480, justify="center", font=large_font)
    question_value_label.grid(row=4, column=0, sticky="nsew")

    take_question_button = tk.Button(root, text="Pak een vraag", command=display_random_question, font=large_font)
    take_question_button.pack(side=tk.BOTTOM, padx=5, pady=(0,50))

    root.mainloop()

def main():
    """
    Main function to start the application.
    """
    setup_gui()

if __name__ == "__main__":
    main()