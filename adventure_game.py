import json
from os import name
import os
import re
import sys
import time
import random
import tkinter as tk
from queue import Queue
import adventure_GUI

input_queue = Queue()  # Queue for communication between GUI and game logic

def display_title():
    print("===========================================================================")
    print("\t\t Welcome to the Adventure Game!\n")
    print("You find yourself in a mysterious land filled with danger and excitement.")
    print("Your goal is to explore and survive the challenges ahead.\n")
    print("The game will prompt you with choices that will shape your adventure. \nUse the number keys combined with the Enter key to make your choices, when prompted. Choose wisely!\n")
    print("Good luck on your adventure!")
    print("===========================================================================\n")

game_state = {
    "player_name": "",
    "choices": [],
    "outcomes": []
}

name = ""  # Global variable to store player's name

def get_input_from_gui(prompt=""):
    if prompt:
        print(prompt, end="", flush=True)
   
    return input_queue.get()  # Wait for input from the GUI

def send_input(self, event):
    user_input = self.entry.get().strip()
    self.entry.delete(0, tk.END)

    if user_input == "":
        return  # Ignore empty input
    self.write(f"> {user_input}\n")  # Echo input in GUI
    input_queue.put(user_input)  # Send input back to game logic

def display_player_name() :
    nameDefault = "Player"
    global name
    name = get_input_from_gui("Please enter a name below : |\n "
                                                "\t\t\t    |\n" 
                                                "\t\t\t    V")
    if name == "": 
        print("Welcome, ", nameDefault)
        return nameDefault
    elif not re.fullmatch(r"[A-Za-z]+", name):
      print("Invalid name. Letters only.")
      display_player_name()
    else : 
        print("\nWelcome", name ,":\n")
        game_state["player_name"] = name
        return name

def display_menu():
    while True:
      print("Please choose an option:")
      print("1. Start New Game")
      print("2. Load Game")
      print("3. Exit")
      choice = get_player_choice()
      if choice == '1':
        start_new_game()
      elif choice == '2':
        load_game()
      elif choice == '3':
        print("Exiting the game. Goodbye!")
        sys.exit()

def get_player_choice():    
    choice = get_input_from_gui("Enter your choice (1, 2, or 3): ")
    while choice not in ['1', '2', '3']:
        print("Invalid choice. Please try again.")
        choice = get_input_from_gui("Enter your choice (1, 2, or 3): ")
    return choice

def slow_print(text, delay=0.04):
    for char in text:
      print(char, end="", flush=True)
      time.sleep(delay)
    print()
    # Utility function to print text slowly for dramatic effect

def attack():
    slow_print("You attack the enemy with all your might...")
    time.sleep(1)
    if random.random() < 0.6:  # 60% chance of success
        slow_print(f"{name}'s attack is successful!")
        return True
    else:
        slow_print(f"{name}'s attack was unsuccessful.")
        return False
    # Simulate an attack with a random chance of success

def start_new_game():
    save_game(game_state, filename=f"save_{name}.json")  # Save initial game state
    print("Starting a new game...\n  ")
    time.sleep(2)  # Simulate loading time

    def intro():
      slow_print("You awaken in a dimly lit forest...")
      slow_print("The air is cold. The trees whisper.")
      slow_print("A narrow path stretches out before you.\n")
      time.sleep(1)
      choose_path()

    def choose_path():
      slow_print(f"What will {name} do?")
      print("1, Follow the path")
      print("2, Explore the trees")
      print("3, Sit and wait")
      print("4, Exit the game")

      choice = get_input_from_gui("> ").strip()

      if choice == "1":
        game_state["choices"].append("path")
        save_game(game_state, filename=f"save_{name}.json")  
        path_route()
      elif choice == "2":
        game_state["choices"].append("trees")
        save_game(game_state, filename=f"save_{name}.json")  
        trees_route()   
      elif choice == "3":
        game_state["choices"].append("wait")
        save_game(game_state, filename=f"save_{name}.json")  
        wait_route() 
      elif choice == "4":
          print("Exiting the game. Goodbye!")
          sys.exit()
      else:
        print("Invalid choice. Try again.\n")
        return choose_path()  # re-prompt

    def path_route():
        slow_print("\nYou walk along the winding path...")
        slow_print("A strange figure appears in the distance.")
        slow_print("As you approach, it vanishes into thin air... The hair on the back of your neck stands up.")
        slow_print("You feel a chill run down your spine. It feels as if something is watching you. \nThe path seems to stretch endlessly ahead.\n")
        game_state["outcomes"].append("encountered a mysterious figure on the path")
        save_game(game_state, filename=f"save_{name}.json")
        choose_path_route()

    def choose_path_route():
        slow_print(f"What will {name} do?\n")
        print("1, Keep walking")
        print("2, Turn back")
        print("3, Venture off the path")
        print("4, Exit the game")
        choice = get_input_from_gui("> ").strip()
        if choice == "1":
            game_state["choices"].append("keep walking")
            save_game(game_state, filename=f"save_{name}.json")
            path_route2()
        elif choice == "2":
            game_state["choices"].append("turn back")
            save_game(game_state, filename=f"save_{name}.json")
            path_route_back()
        elif choice == "3":
            game_state["choices"].append("venture off the path")
            save_game(game_state, filename=f"save_{name}.json")
            path_route_venture()
        elif choice == "4":
            print("Exiting the game. Goodbye!")
            sys.exit()
        else:
            print("Invalid choice. Try again.\n")
            path_route()  # re-prompt

    def path_route2():
        slow_print("\nYou keep walking, but the figure reappears, now much closer...")
        slow_print("It reaches out to you with a ghostly hand...")
        slow_print("You try to run, but your legs feel like they're stuck in quicksand...")
        slow_print("The figure's grip tightens around you, and everything goes black...\n")
        game_state["outcomes"].append("was caught by the mysterious figure on the path")
        save_game(game_state, filename=f"save_{name}.json")
        choose_path_route2()

    def attack_figure():
        if attack() == True:
            slow_print("\nYou gouge at the figures eyes violently and manage to break free from the figure's grasp. \nYou run swiftly and escape into the forest...")
            slow_print("You find a hidden path that leads you out of the forest, you emerge into the sunlight, safe but shaken...\n")
            time.sleep(1)
            slow_print(f"Congratulations, {name}! You've survived the encounter with the mysterious figure and escaped the forest!\n")
            game_state["outcomes"].append("attacked the figure and escaped")
            save_game(game_state, filename=f"save_{name}.json")
            display_menu()  # back to main menu
        else:
            slow_print("\nYour attack fails, and the figure tightens its grip...")
            slow_print("You feel yourself being pulled deeper into the darkness. \nYou realize with horror that your soul is trapped in the figure's grasp forever...\n")
            time.sleep(1)
            slow_print(f"{name}'s soul has been trapped by the mysterious figure.... Game Over.\n")
            game_state["outcomes"].append("attacked the figure but failed and got trapped")
            save_game(game_state, filename=f"save_{name}.json")
            display_menu()  # back to main menu

    def path_route2_surrender():
        slow_print("\n You surrender to the figure, hoping it will show mercy. \nA foul twisted voice echoes in your mind, promising eternal torment. \nThe figure drags you into the darkness, and you realize with horror that your soul is trapped within it's grasp forever...\n")
        time.sleep(1)
        slow_print(f"{name}'s soul has been trapped by the mysterious figure.... Game Over.\n")
        game_state["outcomes"].append("surrendered to the figure and got trapped")
        save_game(game_state, filename=f"save_{name}.json")
        

    def path_route2_communicate():
        slow_print("\nYou attempt to communicate with the figure, speaking softly...")
        slow_print("The figure seems to understand you, and it responds with a series of eerie sounds...")
        slow_print("You realize that the figure is trying to communicate something important, but you can't quite decipher its message...\n")
        slow_print("While suspended in dialogue with the figure you take a chance to attack and break free while the figure is distracted...\n")
        attack_figure()  # attempt to attack while communicating
        game_state["outcomes"].append("attempted to communicate with the figure but couldn't understand its message")
        save_game(game_state, filename=f"save_{name}.json")
        choose_path_route2()  # re-prompt for next action

    def choose_path_route2():
        slow_print(f"What will {name} do?\n")
        print("1, Attack the figure")
        print("2, Surrender to the figure")
        print("3, Attempt to communicate")
        print("4, Exit the game")
        choice = get_input_from_gui("> ").strip()
        if choice == "1":
            game_state["choices"].append("attack the figure")
            save_game(game_state, filename=f"save_{name}.json")
            attack_figure()
        elif choice == "2":
            game_state["choices"].append("surrender to the figure")
            save_game(game_state, filename=f"save_{name}.json")
            path_route2_surrender()
        elif choice == "3":
            game_state["choices"].append("attempt to communicate")
            save_game(game_state, filename=f"save_{name}.json")
            path_route2_communicate()
        elif choice == "4":
            print("Exiting the game. Goodbye!")
            sys.exit()
        else:
            print("Invalid choice. Try again.\n")
            path_route2()  # re-prompt


    def path_route_back():   
        slow_print("\nYou turn back, but the path behind you has disappeared...")
        slow_print("You're trapped in the forest with no way out...")   
        slow_print("The trees seem to close in around you, and you can hear something moving in the darkness...")
        slow_print("Frozen with fear you stand still awaiting whatever is lurking in the shadows to reveal itself...")
        slow_print("With a violent burst, a spider the size of a horse leaps out of the darkness and attacks you\n")
        game_state["outcomes"].append("turned back on the path and got trapped in the forest")
        save_game(game_state)
        choose_path_route_back()

    def choose_path_route_back():
        slow_print(f"What will {name} do?\n")
        print("1, Attack the spider")
        print("2, Climb a tree to escape")
        print("3, Run!")
        print("4, Exit the game")
        choice = get_input_from_gui("> ").strip()
        if choice == "1":
            game_state["choices"].append("attack the spider")
            save_game(game_state, filename=f"save_{name}.json")
            attack_spider()
        elif choice == "2":
            game_state["choices"].append("climb a tree to escape")
            save_game(game_state, filename=f"save_{name}.json")
            trees_route_climb()
        elif choice == "3":
            game_state["choices"].append("run!")
            save_game(game_state, filename=f"save_{name}.json")
            run_through_forest()
        elif choice == "4":
            print("Exiting the game. Goodbye!")
            sys.exit()
        else:
            print("Invalid choice. Try again.\n")
            path_route_back()  # re-prompt

    def attack_spider():
        if attack() == True:
            slow_print("\nYou strike the spider with all your might, and it screeches in pain...")
            slow_print("The spider retreats back into the darkness, giving you a chance to escape...")
            slow_print("You run as fast as you can, eventually finding a hidden path that leads you out of the forest...\n")
            time.sleep(1)
            slow_print(f"Congratulations, {name}! You've survived the encounter with the giant spider and escaped the forest!\n")
            game_state["outcomes"].append("attacked the giant spider and escaped")
            save_game(game_state, filename=f"save_{name}.json")
            display_menu()  # back to main menu
        else:
            slow_print("\nYour attack fails, and the spider's venom takes hold...")
            slow_print("You feel yourself growing weaker and weaker, until eventually you collapse to the ground, succumbing to the spider's poison...\n")
            time.sleep(1)
            slow_print(f"{name} has been poisoned by the giant spider.... Game Over.\n")
            game_state["outcomes"].append("attacked the giant spider but failed and got poisoned")
            save_game(game_state, filename=f"save_{name}.json")
            display_menu()  # back to main menu

    def run_through_forest():
        slow_print("\nYou sprint through the forest, trying to put as much distance between you and the spider as possible...")
        slow_print("The spider gives chase, its heavy footsteps pounding behind you...")
        slow_print("You weave through the trees, trying to lose it, but it's relentless...")
        slow_print("Completely gassed, you stumble upon a hidden path that leads you out of the forest, you break free of the canopy. \nAs the blinding sunlight streams across your face you hear the screech of the spider as the sun sears it's hairy hide...\n")
        slow_print("the spider withers and squirms back into the darkness, you can breath freely again...\n")
        time.sleep(1)
        slow_print(f"Congratulations, {name}! You've outrun the giant spider and escaped the forest!\n")
        game_state["outcomes"].append("ran through the forest and escaped the giant spider")
        save_game(game_state, filename=f"save_{name}.json")
        display_menu()  # back to main menu
        

    def path_route_venture():
        slow_print("\nYou venture off the path, hoping to find another way out...")
        slow_print("But the trees seem to close in around you, and you quickly lose your sense of direction...")
        slow_print("You wander for hours, growing more and more disoriented...")
        slow_print("Eventually, you collapse from exhaustion, realizing you're hopelessly lost in the forest...\n")
        slow_print("You awaken to the strange figure standing over you, its eyes glowing with an otherworldly light...")
        slow_print("The figure reaches out to you with a ghostly hand, and you feel a cold chill run down your spine as it grasps your neck...")
        game_state["outcomes"].append("ventured off the path and got lost in the forest")
        save_game(game_state, filename=f"save_{name}.json")
        choose_path_route2()  # re-prompt for next action
            

    

    def trees_route():
      slow_print("\nYou step into the dark trees...")
      slow_print("Something moves behind you.")
      slow_print("You turn, but there's nothing there...")
      slow_print("The trees seem to close in around you.\n")
      game_state["outcomes"].append("explored the trees and felt something following them")
      save_game(game_state, filename=f"save_{name}.json")
      choose_trees_route()

    def choose_trees_route():
      slow_print(f"What will {name} do?\n")
      print("1, Keep exploring")
      print("2, Climb a tree")
      print("3, Run back to the path")
      print("4, Exit the game")
      choice = get_input_from_gui("> ").strip()
      if choice == "1":
          game_state["choices"].append("keep exploring")
          save_game(game_state, filename=f"save_{name}.json")
          trees_route2()
      elif choice == "2":
          game_state["choices"].append("climb a tree")
          save_game(game_state, filename=f"save_{name}.json")
          trees_route_climb()
      elif choice == "3":
          game_state["choices"].append("run back to the path")
          save_game(game_state, filename=f"save_{name}.json")
          choose_path()  # back to path route
      elif choice == "4":
          print("Exiting the game. Goodbye!")
          sys.exit()
      else:
          print("Invalid choice. Try again.\n")
          trees_route()  # re-prompt

    def trees_route2():
      slow_print("\nYou keep exploring, but the forest seems to grow darker and more oppressive...")
      slow_print("You hear whispers in the wind, and you feel like something is following you...")
      slow_print("Eventually, you stumble upon a clearing with a strange, glowing object in the center...")
      slow_print("As you approach it, the object pulses with energy, and you feel a surge of power coursing through your veins...\n")
      game_state["outcomes"].append("found a mysterious glowing object in the trees")
      save_game(game_state, filename=f"save_{name}.json")
      choose_trees_route2()

    def choose_trees_route2():
      slow_print(f"What will {name} do?\n")
      print("1, Take the glowing object")
      print("2, Leave the area, keep exploring the forest.")
      print("3, Climb a tree to find a way out")
      print("4, Exit the game")
      choice = get_input_from_gui("> ").strip()
      if choice == "1":
          game_state["choices"].append("take the glowing object")
          save_game(game_state, filename=f"save_{name}.json")
          slow_print("\nYou take the glowing object, and in a premonitious state you see visions of the universe and the secrets of existence itself...")
          slow_print("An overwhelming breadth of knowledge floods your mind... but then a sinister presence manifests...\n")
          slow_print("The universe shrinks smaller and smaller until you're floating in a void of darkness.\n")
          slow_print("You feel a cold, malevolent force wrapping around you, and you sit there in darkness, in the void for eternity...\n")
          time.sleep(1)
          slow_print(f"{name} has been consumed by the void... Game Over.\n")
          game_state["outcomes"].append("took the glowing object")
          save_game(game_state, filename=f"save_{name}.json")
          display_menu()  # back to main menu0
      elif choice == "2":
          game_state["choices"].append("leave the area")
          save_game(game_state, filename=f"save_{name}.json")
          slow_print("\nYou decide to leave the glowing object alone, sensing that it may be dangerous.")
          slow_print("As you turn to leave, you feel a soft breeze on your neck, and you hear a whispering voice in your ear...\n")
          slow_print("The voice has a warm and comforting tone. You follow it as the brush and canopy start to lighten, the sunlight peering through the leaves.\n")
          slow_print("You break through the canopy, and find yourself in a beautiful meadow filled with wildflowers and prairie grass...\n")
          time.sleep(1)
          slow_print(f"Congratulations, {name}! You've found a safe haven in the forest and escaped the darkness!\n")
          game_state["outcomes"].append("left the glowing object alone")
          save_game(game_state, filename=f"save_{name}.json")
          display_menu()  # back to main menu
      elif choice == "3":
          game_state["choices"].append("climb a tree to find a way out")
          save_game(game_state, filename=f"save_{name}.json")
          trees_route_climb()
      elif choice == "4":
          print("Exiting the game. Goodbye!")
          sys.exit()
      else:
          print("Invalid choice. Try again.\n")
          trees_route2()  # re-prompt

    def trees_route_climb():
      slow_print("\nYou climb the nearest tree, hoping to get a better view of your surroundings...")
      slow_print("You climb and climb, as the air grows thinner and colder, and the branches become more sparse...")
      slow_print("You've been climbing for what feels like hours, no treetop in sight. almost as if you are climbing in circles.\n You look down and see the ground only a few meters below you\n")
      game_state["outcomes"].append("climbed a tree and saw a mysterious figure")
      save_game(game_state, filename=f"save_{name}.json")
      choose_trees_route3()

    def choose_trees_route3():
      slow_print(f"What will {name} do?\n")
      print("1, Climb down and find another way out")
      print("2, Continue climbing")
      print("3, Shout for help")
      print("4, Exit the game")
      choice = get_input_from_gui("> ").strip()
      if choice == "1":
          game_state["choices"].append("climb down and find another way out")
          save_game(game_state, filename=f"save_{name}.json")
          trees_route_climb_down()
      elif choice == "2":
          game_state["choices"].append("continue climbing")
          save_game(game_state, filename=f"save_{name}.json")
          trees_route_climb2()
      elif choice == "3":
          game_state["choices"].append("shout for help")
          save_game(game_state, filename=f"save_{name}.json")
          trees_route_shout()
      elif choice == "4":
          print("Exiting the game. Goodbye!")
          sys.exit()
      else:
          print("Invalid choice. Try again.\n")
          trees_route_climb()  # re-prompt

    def trees_route_climb_down():
      slow_print("\nYou climb down and land onto a very different looking part of the forest, the trees full of life and the air filled with the sound of birds and insects.\nYou follow a small stream that leads you out of the forest and into a peaceful village...\n")
      time.sleep(1)
      slow_print(f"Congratulations, {name}! You've found a way out of the forest and discovered a new home in the village!\n")
      game_state["outcomes"].append("climbed down and found a peaceful village")
      save_game(game_state, filename=f"save_{name}.json")
      display_menu()  # back to main menu

    def trees_route_climb2():
      slow_print("\nYou've been climbing for hours and hours more, weathered and exhausted you eventually find a way to suspend yourself from the branches and fall asleep...")
      slow_print("You awaken to the sound of muffled singing. You look up and see a giant treehouse in the branches above you, with a warm light emanating from its windows...")
      slow_print("You approach the treehouse and peer in the window, you see a group of tree elves gathered around a fire, singing and dancing...")
      slow_print("The tree elves notice you and invite you inside, offering you food and shelter...")
      slow_print("You spend the night with the tree elves, learning their songs and stories, and in the morning they guide you to a hidden path that leads you out of the forest...\n")
      time.sleep(1)
      slow_print(f"Congratulations, {name}! You've found a safe haven with the tree elves and escaped the forest!\n")
      game_state["outcomes"].append("found the tree elves")
      save_game(game_state, filename=f"save_{name}.json")
      display_menu()  # back to main menu

    def trees_route_shout():
      slow_print("\nYou shout for help, hoping someone will hear you... You shout again, silence...")
      slow_print("Suddenly a strange looking bird swoops through the canopy and lands on a branch nearby, it seems to be watching you...")
      slow_print("A long moment passes and another bird of the same kind lands next to the first.\nAgain and again more of these unusual birds appear, until the branches are filled with them...A SWARM!")
      slow_print("You start to panic and as soon as you make a move to flee, the birds attack, pecking and clawing at you until you're covered in deep wounds...")
      slow_print("You collapse to the ground, bleeding and in pain, as the birds continue to attack you until you eventually succumb to your injuries...\n")
      time.sleep(1)
      slow_print(f"{name} has been attacked by the swarm of birds... Game Over.\n")
      game_state["outcomes"].append("shouted for help and got attacked by a swarm of birds")
      save_game(game_state, filename=f"save_{name}.json")
      display_menu()  # back to main menu
                                    


    def wait_route():
      slow_print("\nYou sit quietly...")
      slow_print("The forest grows unnervingly silent.")
      slow_print("Suddenly, you hear footsteps approaching...")
      slow_print("A shadowy figure emerges from the darkness, staring at you with glowing eyes...\n")
      game_state["outcomes"].append("sat and waited, then encountered a shadowy figure")
      save_game(game_state, filename=f"save_{name}.json")
      choose_wait_route()

    def choose_wait_route():
      slow_print(f"What will {name} do?\n")
      print("1, Stand your ground")
      print("2, Try to communicate")
      print("3, Attempt to flee")
      print("4, Exit the game")
      choice = get_input_from_gui("> ").strip()
      if choice == "1":
          game_state["choices"].append("stand your ground")
          save_game(game_state, filename=f"save_{name}.json")
          wait_route_stand()
      elif choice == "2":
          game_state["choices"].append("try to communicate")
          save_game(game_state, filename=f"save_{name}.json")
          wait_route_communicate()
      elif choice == "3":
          game_state["choices"].append("attempt to flee")
          save_game(game_state, filename=f"save_{name}.json")
          wait_route_flee()
      elif choice == "4":
          print("Exiting the game. Goodbye!")
          sys.exit()
      else:
          print("Invalid choice. Try again.\n")
          wait_route()  # re-prompt

    def wait_route_stand():
      slow_print("\nYou stand your ground, trying to appear confident...")
      slow_print("The figure seems to hesitate, then slowly backs away into the darkness...")
      slow_print("You feel a sense of relief, but also a lingering fear that the figure may return...\n")
      game_state["outcomes"].append("stood your ground and the figure retreated")
      save_game(game_state, filename=f"save_{name}.json")
      choose_path()  # back to path route

    def wait_route_communicate():
      path_route2_communicate()  # re-use the communication route from the path encounter
      game_state["outcomes"].append("tried to communicate with the figure")
      save_game(game_state, filename=f"save_{name}.json")

    def wait_route_flee():
      slow_print("\nYou attempt to flee, but the figure moves with supernatural speed...")
      slow_print("It quickly catches up to you, and you feel its cold grip on your shoulder...")
      slow_print("You try to break free, but it's too strong...")
      slow_print("The figure drags you deeper into the forest, and you realize with horror that you're completely at its mercy...\n")
      game_state["outcomes"].append("attempted to flee but was caught by the figure")
      save_game(game_state, filename=f"save_{name}.json")

    intro() # initialize the game by calling the intro function

def save_game(game_state, filename="savegame.json"):
   with open(filename, "w") as f:
      json.dump(game_state, f, indent=4)
    # Save game state to a file

def load_game():
    print("Loading a saved game...\n")  
    
    # List available save files
    save_files = [f for f in os.listdir('.') if f.startswith('save_') and f.endswith('.json')]
    
    if not save_files:
        print("No saved games found.")
        display_menu()
        return
    
    print("Available saves:")
    print("-" * 50)
    for i, save_file in enumerate(save_files, 1):
        # Extract player name from filename (remove "save_" and ".json")
        player_name = save_file.replace("save_", "").replace(".json", "")
        with open(save_file, "r") as f:
            save_data = json.load(f)
            choices_made = len(save_data.get("choices", []))
        print(f"{i}. {player_name} - {choices_made} choices made")
    print("-" * 50)
    print("\nType the number of the save to load (or 0 to go back to menu):")
    
    # Get player choice
    choice = get_input_from_gui("> ")
    
    try:
        choice_num = int(choice)
        if choice_num == 0:
            display_menu()
            return
        if 1 <= choice_num <= len(save_files):
            filename = save_files[choice_num - 1]
        else:
            print("Invalid choice.")
            load_game()
            return
    except ValueError:
        print("Invalid input. Please enter a number.")
        load_game()
        return
    
    # Load the save file
    try:
        with open(filename, "r") as f:
            loaded_state = json.load(f)
            global game_state, name
            game_state = loaded_state
            name = loaded_state.get("player_name", "Player")
            print(f"\nWelcome back, {name}!")
            print(f"You've made {len(game_state['choices'])} choices so far.\n")
            time.sleep(2)
            
            # Resume the game with loaded state
            resume_game()
    except FileNotFoundError:
        print("Save file not found.")
        display_menu()

def resume_game():
    """Resume the game from the loaded state"""
    print("Resuming your adventure...\n")
    time.sleep(1)
    
    # Display recap of recent choices
    if game_state['choices']:
        print("Recent choices:")
        for choice in game_state['choices'][-3:]:  # Show last 3 choices
            print(f"  - {choice}")
        print()
    
    # Continue the game loop
    display_menu()

def main(start_mode="menu"):
    display_title()
    if start_mode == "new_game":
        display_player_name()
        start_new_game()
    elif start_mode == "load_game":
        load_game()
    else:  # menu mode
        display_player_name()
        display_menu()

if __name__ == "__main__":
    main()