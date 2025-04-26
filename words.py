import json
from difflib import get_close_matches, SequenceMatcher

# Load the dictionary data
data = json.load(open("data.json"))

# ისტორიის შესანახი სია
history = []

# ფუნქცია ისტორიის ფაილში შესანახად
def save_history_to_file(history_list):
    with open("word_history.txt", "w", encoding="utf-8") as file:
        file.write("სიტყვების ძიების ისტორია\n==================\n\n")
        for index, (word, desc) in enumerate(history_list, 1):
            file.write(f"{index}. Word: {word}\n")
            if isinstance(desc, list) and len(desc) > 1:
                for i, d in enumerate(desc, 1):
                    file.write(f"   {i}. {d}\n")
            else:
                file.write(f"   1. {desc[0] if isinstance(desc, list) else desc}\n")
            file.write("\n")
            
# ძირითადი ფუნქცია სიტყვისა და მისი მნიშვნელობების აღსაწერად
def describe(word):
    if word.capitalize() in data:
        return data[word.capitalize()]

    if word.upper() in data:
        return data[word.upper()]

    word = word.lower()

    if word in data:
        return data[word]

    elif get_close_matches(word, data.keys()):
        word_list = get_close_matches(word, data.keys(), 10)
        print("Which word did you mean?")
        
        for index, w in enumerate(word_list, 1):
            n_word = f"{index}. {w}"
            word_ratio = str(round(SequenceMatcher(None, w, word).ratio(), 4)) + "%"
            print(n_word, word_ratio)

        while True:
            opt = input("Please choose option N: ").strip()
            if not opt.isdigit():
                print("Please enter a digit!")
                continue
            opt = int(opt)
            if opt not in range(1, len(word_list) + 1):
                print(f"Please choose a number between 1 - {len(word_list)}")
                continue
            opt -= 1
            break

        chosen_word = word_list[opt]
        print(f"Chosen word: {chosen_word}")
        return data[chosen_word]

    else:
        return "Can't find the word :/"

# მთავარი ციკლი მომხმარებლის ინტერაქციისთვის
while True:

   # მენიუს ჩვენება სიტყვების აღწერის პროგრამისთვის
    print("\n=== Word Description Program ===")
    print("Enter a word to get its description or type 'exit' to quit.")
    word = input("Enter word: ").strip()

    # exit პირობა
    if word.lower() == "exit":
        print("Saving history and exiting...")
        save_history_to_file(history)
        print("Goodbye!")
        break

    result = describe(word)
    # სიტყვისა და აღწერის ისტორიაში დამატება
    history.append((word, result))

    # Display the result
    if isinstance(result, list) and len(result) > 1:
        for index, description in enumerate(result, 1):
            print(f"{index}. {description}")
    else:
        print(result[0] if isinstance(result, list) else result)