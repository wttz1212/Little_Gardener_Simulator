#!/usr/bin/env python
# coding: utf-8

# # Little Gardener Simulator (V1.0)
# 

# A little step towards a farming simulator :-)
# With this simple little gardener simulator, as a player, you can:
# - forage in the 'wild' to get your first seeds for the little garden, and
# - simulate the experience of gardening by planting, growing, and harvesting virtual plants

# In[ ]:


import random # Imagine a game without RNG...


# In[ ]:


# Define the Plant class with its attributes and essential methods

class Plant:
    
    def __init__(self, name, harvest_yield):
        self.name = name
        self.harvest_yield = harvest_yield
        self.growth_stages = ["seed", "sprout", "mature", "flower", "fruit", "harvest-ready"]
        self.current_stage = self.growth_stages[0]
        self.harvest_ready = False
    
    def grow(self):
        current_index = self.growth_stages.index(self.current_stage)
        if self.current_stage == self.growth_stages[-1]:
            print(f'{self.name} is fully grown!')
        elif current_index < len(self.growth_stages) - 1:
            self.current_stage = self.growth_stages[current_index + 1]
            if self.current_stage == self.growth_stages[-1]:
                self.harvest_ready = True

            
    def harvest(self):
        if self.harvest_ready:
            self.harvest_ready = False
            return self.harvest_yield
        else:
            return None
            


# In[ ]:


# Define some specific plant types as subclasses of Plant class. 

class Tomato(Plant):
    def __init__(self):
        super().__init__('Tomato', 10)

class Lettuce(Plant):
    def __init__(self):
        super().__init__('Lettuce', 5)
        self.growth_stages = ["seed", "sprout", "mature", "flower", "harvest-ready"]

class Carrot(Plant):
    def __init__(self):
        super().__init__("Carrot", 8)
        self.growth_stages = ["seed", "sprout", "mature", "harvest-ready"]    


# In[ ]:


'''
Selec_time function is a helper that will go through a dictionary or list, display a numbered list to player,
prompt the player to select an item by number, and lastly return the selected item.
'''

def select_item(items):
    # Determine if the input items is a dictionary or a list
    if type(items) == dict:
        item_list = list(items.keys())
    elif type(items) == list:
            item_list = items
    else:
        print('Invalid items type.')
        return None
    
    # Display a numbered list to player
    print('Here is the item list: ')
    for i in range(len(item_list)):
        print(f'{i+1}.{item_list[i]}')
    
    # Get player input
    while True:
        user_input = input("Select an item: ")
        try:
            user_input = int(user_input)
            if 0 < user_input <= len(item_list):
                return item_list[user_input - 1]
            else:
                print('Invalid input: out of range.')
        except:
            print('Type error: please enter an integer')


# In[ ]:


# Define the Gardener class, with its attributes and essential methods

class Gardener:
    
    plant_dict = {'tomato': Tomato, 'lettuce': Lettuce, 'carrot': Carrot}
    
    def __init__(self, name):
        self.name = name
        self.planted_plants = []
        self.inventory = {}
        
    def plant(self):
        if len(self.inventory) == 0:
            print('Your inventory is empty. Please forage for some seeds before planting.')
            return None
        selected_plant = select_item(self.inventory)
        if (selected_plant in self.inventory) and (self.inventory[selected_plant] > 0):
            self.inventory[selected_plant] -= 1
            if self.inventory[selected_plant] == 0:
                del self.inventory[selected_plant]
            new_plant = self.plant_dict[selected_plant]()
            self.planted_plants.append(new_plant)
            print(f'{self.name} has planted a {selected_plant}!')
        else:
            print(f"{self.name} doesn't have any {selected_plant} to plant.")
    
    def tend(self):
        if len(self.planted_plants) == 0:
            print('No plants to tend. Please plant some first!')
            return None
        for plant in self.planted_plants:
            if plant.harvest_ready:
                print(f'{plant.name} is ready to be harvested!')
            else:
                plant.grow()
                print(f'{plant.name} is now a {plant.current_stage}!')
    
    def harvest(self):
        selected_plant = select_item(self.planted_plants)
        if selected_plant.harvest_ready:
            if selected_plant.name in self.inventory:
                self.inventory[selected_plant.name.lower()] += selected_plant.harvest()
            else:
                self.inventory[selected_plant.name.lower()] = selected_plant.harvest()
            print(f"You harvested a {selected_plant.name.lower()}!")
            self.planted_plants.remove(selected_plant)
        else:
            print(f"You can't harvest a {selected_plant.name.lower()}!")
            
    def forage_for_seeds(self):
        seed = random.choice(list(all_plant_types))
        if seed in self.inventory:
            self.inventory[seed] += 1
        else:
            self.inventory[seed] = 1
        print(f'{self.name} has found some {seed} seeds!')


# In[ ]:


# Set the varibales for the little simulator game

all_plant_types = ['tomato', 'lettuce', 'carrot']
valid_commands = ['plant', 'tend', 'harvest', 'forage', 'help', 'quit']

# Welcome message
print('''Welcome to your garden! You will act as a virtual gardener.\n
      Forage for new seeds, plant them, and then watch them grow!\n
      Start by entering your name.''')

# Create the gardener
gardener_name = input('What is your name? ')
print(f"Welcome, {gardener_name}! Let's get gardening!\nType 'help' for a list of commands.")
gardener = Gardener(gardener_name)


# In[ ]:


# The main game loop

while True:
    player_action = input('What would you like to do? ')
    player_action = player_action.lower()

    if player_action in valid_commands:
        if player_action == 'plant':
            gardener.plant()
        elif player_action == 'tend':
            gardener.tend()
        elif player_action == 'harvest':
            gardener.harvest()
        elif player_action == 'forage':
            gardener.forage_for_seeds()
        elif player_action == 'help':
            print('*****Commands*****')
            for command in valid_commands:
                print(command)
        elif player_action == 'quit':
            print(f'Goodbye, {gardener_name}!')
            break
    else:
        print('Invalid command. Please try again.')


# That's it for the Little Gardener Simulator (V1.0). It's simple, and has lots of room for more features and improvements.
# 
# **Future Updates:**
# 1. Add a few more methods to allow players to view and modify inventory and the list of all plants in the game.
# 2. Build a economic system so players can sell products, buy seeds, tools, lands, etc.
# 3. Add achievements and milestones.
# 4. Consider some random events like pests and challenging weather conditions.
# 5. At 2.0, let's remake the text game into a 2D web-based game using Streamlit!  

# 
