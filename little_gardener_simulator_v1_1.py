#!/usr/bin/env python
# coding: utf-8

# # Little Gardener Simulator (V1.1)
# 

# A little step towards a farming simulator : )
# With this simple little gardener simulator, as a player, you can:
# - forage in the 'wild' to get your first seeds for the little garden, and
# - simulate the experience of gardening by planting, growing, and harvesting virtual plants
# - sell your products, buy more pots, and build a bigger garden
# 
# ***Special event: you can now find Easter eggs and bunnies while foraging in the 'wild'!***

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
        try:
            item_name = item_list[i].name
        except:
            item_name = item_list[i]
        print(f'{i+1}.{item_name}')
    
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


# Define the Market, with its attributes and essential methods

class Market:
    def __init__(self):
        self.inventory = {}

    def set_inventory(self, item, num, price):
        if num < 0 or price < 0:
            raise ValueError("Quantity and price must be non-negative.")
        self.inventory[item] = [num, price]

    def update_inventory_number(self, item, num):
        if item not in self.inventory:
            raise KeyError(f"{item} not found in market inventory. Use set_inventory method instead.")
        self.inventory[item][0] += num
    
    def set_inventory_price(self, item, price):
        if item not in self.inventory:
            raise KeyError(f"{item} not found in market inventory. Use set_inventory method instead.")
        self.inventory[item][1] = price

    def show_inventory(self):
        if len(self.inventory) == 0:
            print('The market inventory is empty! Use set_inventory method to add items')
        else:
            print("Item \tQuantity \tPrice")
            for i in self.inventory:
                print(f'{i} \t{self.inventory[i][0]} \t{self.inventory[i][1]}')
    


# In[ ]:


# Define the Gardener class, with its attributes and essential methods

class Gardener:
    
    plant_dict = {'tomato': Tomato, 'lettuce': Lettuce, 'carrot': Carrot}
    
    def __init__(self, name):
        self.name = name
        self.planted_plants = []
        self.inventory = {}
        self.golds = 100
        self.total_pots = 2

    def plant(self):
        if len(self.inventory) == 0:
            print('Your inventory is empty. Please forage for some seeds before planting.')
            return None
        if len(self.planted_plants) == self.total_pots:
            print("No empty pot! Harvest some or purchase another pot!")
            return None
        
        selected_plant = select_item(self.inventory)
        if selected_plant in self.inventory and self.inventory[selected_plant] > 0:
            self.inventory[selected_plant] -= 1
            if self.inventory[selected_plant] == 0:
                del self.inventory[selected_plant]
            new_plant = self.plant_dict[selected_plant]()
            self.planted_plants.append(new_plant)
            print(f'{self.name} has planted a {selected_plant}!')
            if len(self.planted_plants) == self.total_pots:
                print('All pots are growing plants!')
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

    def view_inventory(self):
        print(f"You have {self.golds} golds and {self.total_pots} pots in total.")
        if len(self.inventory) == 0:
            print('Your inventory is empty!')
        else:
            print('Item \tQuantity')
            for i in self.inventory:
                print(f'{i} : {self.inventory[i]}')

    def update_inventory(self, item, num):
        if item in self.inventory:
            self.inventory[item] += num
        else:
            self.inventory[item] = num

    def update_total_pots(self, num):
        self.total_pots += num
    
    def update_golds(self, num):
        self.golds += num

    def buy_pots(self):
        print(f"The next pot costs ${10*self.total_pots}.")
        user_input = input("Do you want to buy a new pot? Enter \"yes\" to confirm.")
        if user_input.lower() == 'yes':
            if self.golds >= 10*self.total_pots:
                self.update_golds(-10*self.total_pots)
                self.update_total_pots(1)
                print("You have successfully purchased a new pot!")
            else:
                print("You don't have enough golds to buy a new pot yet.")
        else:
            return None
        
    def buy_seeds(self, market):
        print("Select the seed you want to buy from the market:")
        selected_item = select_item(market.inventory)
        user_input = input("How many seeds do you want to buy?")
        try:
            user_input = int(user_input)
            if user_input <= 0:
                print("ValueError: please enter a positive integer.")
            if user_input > market.inventory[selected_item][0]:
                print(f"ValueError: there are only {market.inventory[selected_item][0]} available in the market.")
            if self.golds < user_input * market.inventory[selected_item][1]:
                print("ValueError: not enough golds!")
            else:
                self.update_golds(-1*user_input*market.inventory[selected_item][1])
                self.update_inventory(selected_item, user_input)
                market.update_inventory_number(selected_item, -1*user_input)
        except Exception:
            print("Please enter a positive integer.")

    def sell_products(self, market):
        print("Select the seed you want to sell to the market:")
        selected_item = select_item(self.inventory)
        user_input = input("How many products do you want to sell?")
        try:
            user_input = int(user_input)
            if user_input <= 0:
                print("ValueError: please enter a positive integer.")
            if selected_item not in self.inventory:
                print(f"KeyError: you don't have any {selected_item} to sell.")
            if user_input > self.inventory[selected_item]:
                print(f"ValueError: there are only {self.inventory[selected_item]} available in your inventory.")
            else:
                self.update_golds(user_input*market.inventory[selected_item][1])
                self.update_inventory(selected_item, -1*user_input)
                market.update_inventory_number(selected_item, user_input)
        except Exception:
            print("Please enter a positive integer.")


# In[ ]:


# Limited time events
def easter_event(gardener):
    event = random.random()
    if event <= 0.3:
        print("You find an Easter Bunny while foraging! You are gifted a free pot!")
        gardener.update_total_pots(1)
    elif event <= 0.5:
        print("You find an Easter Egg while foraging! Free 10 golds for you!")
        gardener.update_golds(10)

# Set the varibales for the little simulator game

all_plant_types = ['tomato', 'lettuce', 'carrot']
valid_commands = ['view_inventory', 'plant', 'tend', 'harvest', 'forage', 'buy_pots', 'buy_seeds', 'sell_products', 'help', 'quit']

# Welcome message
print('Welcome to your garden! You will act as a virtual gardener.\nForage for new seeds, plant them, and then watch them grow!\nStart by entering your name.')

# Create the market
market = Market()
for item in all_plant_types:
    market.set_inventory(item, 100, 2)

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
            easter_event(gardener)
        elif player_action == 'view_inventory':
            gardener.view_inventory()
        elif player_action == 'buy_pots':
            gardener.buy_pots()
        elif player_action == 'buy_seeds':
            gardener.buy_seeds(market)
        elif player_action == 'sell_products':
            gardener.sell_products(market)
        elif player_action == 'help':
            print('*****Commands*****')
            for command in valid_commands:
                print(command)
        elif player_action == 'quit':
            print(f'Goodbye, {gardener_name}!')
            break
    else:
        print('Invalid command. Please try again.')


# Update nots:
# * Added golds and total_pots arributes to the Gardener class. Now the gardener starts with 2 pots and 100 golds. 
# * Added a few methods to update the golds, total_pots, and inventory, so the gardener can now exchange golds with seeds and planting pots.
# * Added Easter event. During the event, the gardener have chances to find Easter Eggs and Bunnies while foraging.
# 
# **Future Updates:**
# 1. Add a few more methods to allow players to view and modify inventory and the list of all plants in the game. (Done in V1.1)
# 2. Build a economic system so players can sell products, buy seeds, tools, lands, etc. (Done in V1.1)
# 3. Add achievements and milestones.
# 4. Consider some random events like pests and challenging weather conditions.
# 5. At 2.0, let's remake the text game into a 2D web-based game using Streamlit!  
