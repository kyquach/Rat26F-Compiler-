class lexer:
    def __init__(self, states, alphabet, transition_states, starting_state, accepted_states):
        self.transition_table = transition_states
        self.initial_state = starting_state
        self.final_states = accepted_states
        self.all_states = states
        self.input_alphabet = alphabet


    def is_accepted(self, input_string):
        active_states = self.find_epsilon_reachable({self.initial_state})

        for character in input_string:
            character_type = self.classify_character(character)
            if character_type is None:
                return False

            reachable_states = self.follow_transitions(active_states, character_type)
            active_states = self.find_epsilon_reachable(reachable_states)

            if len(active_states) == 0:
                return False

        return not active_states.isdisjoint(self.final_states)

    def follow_transitions(self, current_states, character_type):
        destination_states = set()
        for current_state in current_states:
            key = (current_state, character_type)
            destination_states.update(self.transition_table.get(key, set()))
        return destination_states

    def classify_character(self, character):
        if character.isdigit():
            return "digit"
        elif character.isalpha():
            return "letter"
        return None
      

    def find_epsilon_reachable(self, starting_states):
        epsilon = set(starting_states)
        pending_states = list(starting_states)

        while pending_states:
            current_state = pending_states.pop()
            epsilon_targets = self.transition_table.get((current_state, None), set())

            for target_state in epsilon_targets:
                if target_state not in epsilon:
                    epsilon.add(target_state)
                    pending_states.append(target_state)

        return epsilon
