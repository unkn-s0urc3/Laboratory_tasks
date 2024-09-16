import mix_settings

def normalize_text(text):
    for cyrillic_letter, replacements in mix_settings.replacement_map.items():
        for replacement in replacements:
            text = text.replace(replacement, cyrillic_letter)
    return text

def contains_greek_letters(text):
    return any(char in mix_settings.letters_greek_set for char in text)

def contains_alert_word(text):
    normalized_text = normalize_text(text.lower())
    for word in mix_settings.alert_lst:
        if word in normalized_text:
            return True
    return False

def contains_stop_word(text):
    for phrase in mix_settings.stop_words_lst:
        if phrase in text:
            return True
    return False

def check_message(message):
    if contains_greek_letters(message):
        return "Greek characters were found in the message."
    elif contains_alert_word(message):
        return "Bad words found in the text."
    elif contains_stop_word(message):
        return "Suspicious words were found in the message."
    return "The message is ok."

print("░█████╗░███╗░░██╗████████╗██╗░██████╗██████╗░░█████╗░███╗░░░███╗")
print("██╔══██╗████╗░██║╚══██╔══╝██║██╔════╝██╔══██╗██╔══██╗████╗░████║")
print("███████║██╔██╗██║░░░██║░░░██║╚█████╗░██████╔╝███████║██╔████╔██║")
print("██╔══██║██║╚████║░░░██║░░░██║░╚═══██╗██╔═══╝░██╔══██║██║╚██╔╝██║")
print("██║░░██║██║░╚███║░░░██║░░░██║██████╔╝██║░░░░░██║░░██║██║░╚═╝░██║")
print("╚═╝░░╚═╝╚═╝░░╚══╝░░░╚═╝░░░╚═╝╚═════╝░╚═╝░░░░░╚═╝░░╚═╝╚═╝░░░░░╚═╝")
print("")

user_message = input("Enter a message to verify: ")
result = check_message(user_message)
print(result)