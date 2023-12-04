import random as rand

from outcomes import *
from room import Room

all_verb_cases = {
    'lock': {
        'SUCCESS': [
            'That\'s great. {desc}.',
            'That\'s a great movement. {desc}. Now think your next step.',
            '{desc}. If you don\'t need anymore the {primary} just leave.'
        ],
        'FAIL': [
            '{desc}. Sorry but can\'t help you.',
            'Sorry but there is a problem. {desc}.',
            '{desc}. Think something else to get out of this situation.',
        ],
        'TRANSFORMED': [
            "{desc}. Well done"
        ]
    },
    'unlock': {
        'SUCCESS': [
            'You successfully unlocked the {primary} using the {secondary}.',
            'The {primary} is now unlocked! Go on!',
            'You managed to unlock the {primary}. Well done!.',
            'Finally, you managed to unlock the {primary} with the {secondary}. Think your next step!',
            '{desc}. Think your next step'
        ],
        'FAIL': [
            '{desc}. I think you are a a little bit confused.',
            'You can\'t be serious! Check if the {primary} is lockable and if yes use the correct tool to unlock',
            'How exactly would you unlock the {primary}. No way!',
            '{desc}. Think more carefully'
        ]
    },
    'take': {
        'SUCCESS': [
            'The {primary} is now yours. Maybe you can find a use for it.',
            'You {verb} the {primary} successfully.',
            "You {verb} the {primary} and add it to your inventory."
        ],
        'FAIL': [
            'You cannot do this. {desc}.',
            'Are you serious? {desc}. Be a little more observant.',
            'Be careful. {desc}. So, think again...'
        ]
    },
    'drop': {
        'SUCCESS': [
            'You successfully {verb} the {primary}.',
            "You casually {verb} the {primary} onto the ground.",
            'You decide that this item is no longer necessary for your quest and you {verb} it.'
        ],
        'FAIL': [
            "You cannot {verb} the {primary}. It is not in your possession.",
            "'How exactly to {verb} the {primary} if you don't own it?'",
            "Listen: {desc}.",
            "Looks like there's no {primary} in your inventory to {verb}.",
            "You're not carrying any {primary} to {verb}."
        ]
    },
    'open': {
        'SUCCESS': [
            'You successfully opened the {primary}.',
            'The {primary} is now opened! Go on!',
            'You managed to open the {primary}. Well done!.',
            'Finally, you managed to open the {primary}. Think your next step!'
        ],
        'FAIL': [
            'You cannot open the {primary}. Check if it is openable or is located somewhere else.',
            '{desc}. Think something else',
            'How exactly would you open the {primary}? No way!',
            'Listen: "{desc}", so plan your next movement'
        ]
    },
    'use': {
        'SUCCESS': [
            '{primary}. What\'s your next movement?.',
            'You used the {primary} with success. Figure out what\'s next..',
            'That\'s great! {desc}. Go on....'
        ],
        'FAIL': [
            'You cannot use this item. If you own it it just not usable',
            'You cannot use something you don\'t own or is not usable.'
        ]
    },
    'close': {
        'SUCCESS': [
            'You managed to close the {primary} successfully!',
            'That\'s great. Now the {primary} is closed.',
            'Well done! {desc}. Think what\'s next..',
            'Great! You closed the {primary} successfully! Keep thinking that way...'
        ],
        'FAIL': [
            '{desc}. Think something else',
            'Listen: "{desc}". So, think again what will be your next movement..',
            'Don\'t you see that this is impossible? {desc}. Come on, you can do it!'
        ]
    },
    'go': {
        'FAIL': [
            'Come on! {desc}. Think something else .',
            '{desc}. Come on! It\'s not worth considering..',
            '{desc}. It\'s seems that our instincts don\'t always guide you right...',
            'Are you serious? {desc}. Come οn, don\'t be so impulsive.. '
        ]
    },
    'examine': {
        'FAIL': [
            "I don't see any {primary} around to {verb}.",
            "There doesn't seem to be a {primary} in sight for closer inspection.",
            "You scan the room, but there's no sign of a {primary} to {verb}."
        ],
    },
    'exit': {
        'TRANSFORMED': [
            'You successfully exit the item.',
        ],
        'FAIL': [
            'You cannot exit the {primary}. Think something else..',
            'This doesn\'t make any sense at all! Exit the {primary} is not worth considering...',
            'Do you really want to "exit the {primary}"? Come on, don\'t say bullshit'
        ]
    },
    'wait': {
        'NEUTRAL': [
            'Ok, take your time to think..',
            'I am standing right here doing nothing.',
            'It\'s a good idea to wait for a while... '
            'Ok, i am waiting until you decide what to do'
        ]
    }
}

verbs_with_room_primary = {
    'take': {
        'FAIL': [
            'The {primary} is a location. You cannot {verb} it.',
            'Are you serious? It is not possible at all to {verb} the {primary}! It\'s a location, not an item.',
            'You probably make a mistake! You cannot {verb} the whole room!'
        ]
    },
    'drop': {
        'FAIL': [
            'You cannot drop the {primary} because it is a location, not an item.',
            'Wake up! The {primary} is a location. It doesn\'t make any sense at all!',
            'Are you serious? How exactly you will drop this? It\'s a location, not an item!'
        ]
    },
    'open': {
        'FAIL': [
            'You cannot open the {primary} because "{primary}" is a location.',
            'Listen: "{desc}"! Obviously, you can\'t open a location. It\'s not make any sense',
            'How exactly would you open the {primary}? It\'s a place don\'t forget that!'
        ]
    },
    'use': {
        'FAIL': [
            'You cannot {verb} the {primary}. It is a location, not an item.'
        ]
    },
    'close': {
        'SUCCESS': [
            'You successfully went to the {primary}.',
            'Well done! Now you are in the {primary}.',
            'You are in the {primary} now. try to find out what\'s going on here! .'
        ],
        'FAIL': [
            '{desc}. It\'s a room not a "door"..',
            'Are you serious? Closing the {primary} is absolutely impossible. It\'s a location not a "door".. ',
            '{desc}. Come on, be a little more realistic..!.'
        ]
    },
    'go': {
        'SUCCESS': [
            'Your thinking is very good. Your curiosity leads you down new paths',
            'You successfully went to the {primary}.',
            'Well done! Now you are in the {primary}.',
            'You are in the {primary} now. Try to find out what\'s going on here! .'
        ],
        'FAIL': [
            'Come on! {desc}. Think something else .',
            '{desc}. Come on! It\'s not worth considering..',
            '{desc}. It\'s seems that our instincts don\'t always guide you right...',
            'Are you serious? {desc}. Come οn, don\'t be so impulsive.. '
        ]
    },
    'examine': {
        'FAIL': [
            '{desc}.',
            "Are you sure you're in the {primary}?",
            "This isn't the {primary}. You're in a different area altogether.",
            "You're in a different room. This isn't the {primary}."
        ]
    },
    'lock': {
        'FAIL': [
            'You cannot lock the {primary}. It is a location not a door.',
            'It\'s not make sense locking the {primary}. Think something else.',
            'Come on!! Saying that you want to lock the {primary} is at least foolishness.'
        ]
    },
    'unlock': {
        'FAIL': [
            'You cannot unlock the {primary}. It is a location not a door.',
            'It\'s not make sense unlocking the {primary}. Think something else.',
            'Come on!! {desc}.',
            'Listen: "{desc}". So, change your plans.'
        ]
    }
}


def process(result):
    action = result.action
    outcome = result.outcome
    input_verb = result.action.command.input_verb
    if not outcome.description:
        return False

    primary_is_room = isinstance(action.primary_object, Room)

    if primary_is_room:
        if action.command.verb in verbs_with_room_primary:
            verb = verbs_with_room_primary[action.command.verb]
            # print("i am in primary_is_room")
            # Assuming outcome.type holds either 'SUCCESS' or 'FAIL'
            if outcome.type in verb:
                success_fail_cases = verb.get(outcome.type, None)
                if not success_fail_cases:
                    return outcome.formatted_description

                selected_description = rand.choice(success_fail_cases)

                # Replace {primary} with the actual object's name
                return selected_description.format(primary=outcome.primary_object,
                                                   secondary=outcome.secondary_object,
                                                   verb=input_verb,
                                                   desc=outcome.formatted_description)
                # print("My description: \n")
                # print(formatted_desc)

    else:
        # Check if the action.command verb belongs to the dictionary's verbs in outcomes.py
        if action.command.verb in all_verb_cases:
            verb = all_verb_cases[action.command.verb]

            # Assuming outcome.type holds either 'SUCCESS' or 'FAIL'
            if outcome.type in verb:
                success_fail_cases = verb.get(outcome.type, None)
                if not success_fail_cases:
                    return outcome.formatted_description

                # select one of the descriptions that exists in outcomes.py radomnly
                selected_description = success_fail_cases[rand.randint(0, len(success_fail_cases) - 1)]

                # Replace {primary} with the actual object's name
                return selected_description.format(primary=action.primary_object,
                                                   secondary=action.secondary_object,
                                                   verb=input_verb,
                                                   desc=outcome.formatted_description)
                # print()
                # print("My description: \n")
                # print(formatted_desc)
