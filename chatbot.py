import random


def generate_message(result):
    # Tokenize the outcome into individual words
    outcome_tokens = result.create_outcome.split()

    # Tokenize the command into individual words
    command_tokens = result.command.split()

    if not command_tokens:
        return "You didn't enter any command."

    created_command = ["use", "combine", "hero", "lockpick", "cell", "lock", "nonsense"]
    verbs = ["use", "combine"]
    no_verbs = [word for word in created_command if word not in verbs]

    start_phrases = [
        "You tried to",
        "Attempting to",
        "You look determined to",
        "You convey  a strong will to",
    ]
    end_phrases = [
        "but it doesn't work in this situation.",
        "with no success.",
        "without any luck.",
        ", however, it's not suitable in this context.",
        ", nonetheless, it's unsuitable for this circumstance.",
    ]
    general_phrases = [
        "I shudder at the thought of you being in that situation and thinking like that.",
        "Do not lose mind-control . Think about what else can help you at this stage.",
        "Hey, it is not the end of the world. There are yet some chances left to escape.",
        "Choose once your next movement. You are in trouble and you have to make a serious decision."
    ]
    question_phrases = [
        "Are you trying to",
        "Are you willing of"
    ]

    def starting_string():
        return random.choice(start_phrases)

    def ending_string():
        return random.choice(end_phrases)

    def general_string():
        return random.choice(general_phrases)

    def question_string():
        return random.choice(question_phrases)

    syntax_rules = {
        ("verb",): starting_string() + " {verb} " + ending_string() + ".",
        ("verb", "noun"): starting_string() + " {verb} the {noun}, " + ending_string() + ".",
        ("verb",
         "verb"): question_string() + " {verb} ??And then to {verb}? How exactly are you thinking of doing this?",
        ("noun",): starting_string() + " {noun}, " + ending_string() + ".",
        ("noun", "verb"): starting_string() + " {verb} the {noun}, " + ending_string() + ".",
        ("noun", "noun"): question_string() + " {noun}? Become more specific.",
        ("verb", "noun", "noun"): starting_string() + " {verb} the {noun} with no success.",
        ("verb", "noun", "verb"): starting_string() + " {verb} the {noun} or {combine} it? Make a decision.",
        ("verb", "verb",
         "verb"): "Choose once your next movement. You are in trouble and you have to make a serious decision.",
        ("verb", "verb",
         "noun"): "It's not clear if you want to {verb}, or {verb} the {noun}. It's crucial not to spend your time with wrong decisions.",
        ("noun", "verb",
         "noun"): "Don't forget that you are the hero, and you have to {verb} the {noun}. Make it clear what you are planning.",
        ("noun", "verb",
         "verb"): "You are the hero, and you can {verb} or {verb}. Think carefully in this situation." + general_string(),
        ("noun", "noun", "verb"): "I'm not sure if you want to {verb} the {noun} or the {noun}." + general_string(),
        ("noun", "noun", "noun"): "You described all this, but you are not intending to use them. Provide more details."
    }

    default_message = "Invalid command."

    if all(token in verbs or token in no_verbs for token in command_tokens):
        # Create a command pattern based on the input tokens
        command_pattern = tuple("verb" if token in verbs else "noun" for token in command_tokens)

        # Check if the command pattern is in the syntax_rules
        if command_pattern in syntax_rules:
            # Randomly choose start and close phrases
            start_phrase = random.choice(start_phrases)
            close_phrase = random.choice(end_phrases)
            # Replace placeholders in the description with actual words
            description = syntax_rules[command_pattern].format(
                start_phrase=start_phrase,
                verb=next((token for token in command_tokens if token in verbs), ""),
                noun=next((token for token in command_tokens if token in no_verbs), ""),
                close_phrase=close_phrase
            )
        else:
            description = default_message
    else:
        description = "I am not in what you mean. Take a correct decision and don't lose your mind. "

    first_two_outcome_tokens = outcome_tokens[:2]
    if first_two_outcome_tokens in [
        ['invalid', 'command'],
        ['can\'t', 'use'],
        ['invalid', 'item'],
        ['invalid', 'item(s)'],
        ['can\'t', 'combine'],
        ['lock', 'unlocked'],
        ['lock', 'already'],
    ]:
        return description
    else:
        return "Outcome filter not met."
