
SAMPLE = [
    # ---------------- Html ----------------
    {'category': 'Html', 'text': 'The <p> tag is used for paragraphs.', 'answer': True},
    {'category': 'Html', 'text': 'The <head> tag contains the main content of the page.', 'answer': False},
    {'category': 'Html', 'text': 'The <a> tag is used to create links.', 'answer': True},
    {'category': 'Html', 'text': 'The <img> tag needs a closing </img>.', 'answer': False},
    {'category': 'Html', 'text': 'HTML stands for Hyper Text Markup Language.', 'answer': True},

    # ---------------- Css ----------------
    {'category': 'Css', 'text': 'CSS changes the look of HTML elements.', 'answer': True},
    {'category': 'Css', 'text': 'The "color" property changes text color.', 'answer': True},
    {'category': 'Css', 'text': 'The "background-color" property changes the background.', 'answer': True},
    {'category': 'Css', 'text': 'CSS can only change font size in pixels.', 'answer': False},
    {'category': 'Css', 'text': 'Flexbox helps to align items.', 'answer': True},

    # ---------------- Javascript ----------------
    {'category': 'Javascript', 'text': 'JavaScript runs in the browser.', 'answer': True},
    {'category': 'Javascript', 'text': 'The "let" keyword creates a variable.', 'answer': True},
    {'category': 'Javascript', 'text': 'The "var" keyword cannot create variables.', 'answer': False},
    {'category': 'Javascript', 'text': 'Functions can return values.', 'answer': True},
    {'category': 'Javascript', 'text': 'Arrays start at index 1 in JavaScript.', 'answer': False},

    # ---------------- Science ----------------
    {'category': 'Science', 'text': 'Water boils at 100°C.', 'answer': True},
    {'category': 'Science', 'text': 'The Earth revolves around the Sun.', 'answer': True},
    {'category': 'Science', 'text': 'Humans have 205 bones.', 'answer': False},
    {'category': 'Science', 'text': 'The Sun is a star.', 'answer': True},
    {'category': 'Science', 'text': 'Sound travels faster than light.', 'answer': False},

    # ---------------- Geography ----------------
    {'category': 'Geography', 'text': 'Mount Everest is the highest mountain.', 'answer': True},
    {'category': 'Geography', 'text': 'The Nile is the longest river.', 'answer': True},
    {'category': 'Geography', 'text': 'Australia is both a country and a continent.', 'answer': True},
    {'category': 'Geography', 'text': 'Africa is the largest continent.', 'answer': False},
    {'category': 'Geography', 'text': 'Paris is the capital of France.', 'answer': True},

    # ---------------- Animals ----------------
    {'category': 'Animals', 'text': 'Elephants are the largest land animals.', 'answer': True},
    {'category': 'Animals', 'text': 'Sharks are mammals.', 'answer': False},
    {'category': 'Animals', 'text': 'Dolphins are mammals.', 'answer': True},
    {'category': 'Animals', 'text': 'Bats are blind.', 'answer': False},
    {'category': 'Animals', 'text': 'A group of crows is called a murder.', 'answer': True},

    # ---------------- Sports ----------------
    {'category': 'Sports', 'text': 'Basketball was invented in 1891.', 'answer': True},
    {'category': 'Sports', 'text': 'A touchdown in American football is worth 6 points.', 'answer': True},
    {'category': 'Sports', 'text': 'The FIFA World Cup is held every year.', 'answer': False},
    {'category': 'Sports', 'text': 'Golf is won by the lowest score.', 'answer': True},
    {'category': 'Sports', 'text': 'A hat-trick means scoring 3 goals.', 'answer': True},
]



def seed_data(db, Question):
    for q in SAMPLE:
        question = Question(
            category=q['category'],
            text=q['text'],
            answer=q['answer'],
            explanation=q.get('explanation', '')
        )
        db.session.add(question)
    db.session.commit()
    print("Database seeded with questions!")