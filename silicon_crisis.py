"""
File:         silicon_crisis.py
Author:       Eric Fodel
Last Updated: 5/9/2021
Description:  This program will load the recipe dictionary
              from the json file, run the command line for
              the game, store values for the factories and
              mines, execute given commands, and provide
              correct outputs accordingly.
"""
#create a class to store data for the factories
class Factory :
    def __init__(self, number, recipe):
        self.number = number
        self.recipe = recipe
        self.name = 'Factory ' + str(self.number)
#check if the factory's 'recipe' can be produced
    def check_for_production(self, recipe_dict, stockpile):
        required_materials = 0
        if self.recipe in recipe_dict['recipes']:
            for key in recipe_dict['recipes'][self.recipe]['parts']:
                if key in stockpile:
                    if recipe_dict['recipes'][self.recipe]['parts'][key] <= stockpile[key]:
                        required_materials += 1
            if required_materials == len(recipe_dict['recipes'][self.recipe]['parts']):
                return True
            else:
                return False
#produce the factory's recipe
    def make_product(self, recipe_dict, stockpile, factory_check, mine_check, factory_dict, mine_dict):
        if self.check_for_production(recipe_dict, stockpile):
            production_rate = recipe_dict['recipes'][self.recipe]['output_count']

            if self.recipe != factory_check and self.recipe != mine_check:
                if self.recipe in stockpile.keys():
                    stockpile[self.recipe] += production_rate
                elif self.recipe not in stockpile.keys():
                    stockpile[self.recipe] = production_rate
                
                for key in recipe_dict['recipes'][self.recipe]['parts']:
                    stockpile[key] -= recipe_dict['recipes'][self.recipe]['parts'][key]
            #if the recipe is a factory or mine, add it to the appropriate dictionary
            elif self.recipe == factory_check:
                factory_dict['Factory ' + str(len(factory_dict))] = ''
            elif self.recipe == mine_check:
                mine_dict['Mine ' + str(len(mine_dict))] = ''
#display the name of the factory and what it is producing
    def display_factory(self, recipe_dict, stockpile):
        production_rate = recipe_dict['recipes'][self.recipe]['output_count']
        if self.recipe in stockpile.keys():
            self.total_product = stockpile[self.recipe]
        else:
            self.total_product = 0
            
        print(self.name)
        print(' ', self.recipe, 'factory producing', production_rate, 'per turn,', 'total production', self.total_product)

#create a class to store data for the mines
class Mine:
    def __init__(self, number, raw_material):
        self.number = number
        self.raw_material = raw_material
        self.total_material = 0
        self.name = 'Mine ' + str(self.number)
#mine the material at the end of a turn
    def mine_material(self, recipe_dict, stockpile):
        mine_rate = recipe_dict['raw_materials'][self.raw_material]
        self.total_material += mine_rate

        if self.raw_material not in stockpile.keys():
            stockpile[self.raw_material] = mine_rate
        elif self.raw_material in stockpile.keys():
            stockpile[self.raw_material] += mine_rate
#display the mine, what it's producing, and the effeciency
    def display_mine(self, recipe_dict):
        mine_rate = recipe_dict['raw_materials'][self.raw_material]
        print(self.name)
        print(' ', self.raw_material, 'mine producing', mine_rate, 'per turn')

#calculate how many(x)'s are in a (y) using recursivity
def calculate_amount(recipe_dict, item_searched, item_analyzed, multiplier, current_amount):
    new_multiplier = 1
    add_amount = 0

    if item_analyzed not in recipe_dict['recipes'].keys():
        return current_amount

    else:
        if item_searched in recipe_dict['recipes'][item_analyzed]['parts'].keys():
            add_amount = (recipe_dict['recipes'][item_analyzed]['parts'][item_searched] * multiplier)
            if len(recipe_dict['recipes'][item_analyzed]['parts']) == 1:
                return current_amount

        for key in recipe_dict['recipes'][item_analyzed]['parts']:
            if key in recipe_dict['recipes'].keys():
                new_multiplier = recipe_dict['recipes'][item_analyzed]['parts'][key]
                return calculate_amount(recipe_dict, item_searched, key, multiplier * new_multiplier, current_amount + add_amount)
            
#run the full command line
def get_command(recipe_dict, next_action, factory_dict, mine_dict, stockpile):
#constants for checking commands (and others)
    set_command_check = 'set'
    factory_check = 'factory'
    mine_check = 'mine'
    display_command_check = 'display'
    stockpile_check = 'stockpile'
    factories_display_check = 'factories'
    mines_display_check = 'mines'
    raw_materials_check = 'raw'
    recipes_check = 'recipes'
    how_many_check = 'how'
    analyze_num = 6
    search_item = 2
    lower_action = next_action.lower()
    split_command = lower_action.split()

    if split_command[0] == set_command_check:
        object_number = split_command[2]
        object_output = split_command[3]
        if split_command[1] == mine_check:
            #set mine
            if object_number in mine_dict.keys():
                if mine_dict[object_number] == '':
                    mine_dict[object_number] = object_output
                else:
                    print('This mine is already in use.')
            else:
                print('This factory does not exist.')

        elif split_command[1] == factory_check:
            #set factory
            if object_number in factory_dict.keys():
                factory_dict[object_number] = object_output
            else:
                print('This factory does not exist.')

    elif split_command[0] == display_command_check:
        if split_command[1] == stockpile_check:
            #display stockpile
            print(':::Current Stockpile:::')
            for key in stockpile:
                print('\t' + key + ':', stockpile[key])

        elif split_command[1] == factories_display_check:
            #display factories
            for key in factory_dict:
                current_factory = Factory(key, factory_dict[key])
                if factory_dict[key] != '':
                    current_factory.display_factory(recipe_dict, stockpile)
                else:
                    print(current_factory.name)
                    print('  ' + 'Factory Currently Inactive')

        elif split_command[1] == mines_display_check:
            #display mines
            for key in mine_dict:
                current_mine = Mine(key, mine_dict[key])
                if mine_dict[key] != '':
                    current_mine.display_mine(recipe_dict)
                else:
                    print(current_factory.name)
                    print('  ' + 'Mine Currently Inactive')

        elif split_command[1] == raw_materials_check:
            #display all raw materials
            print(':::Raw Materials:::')
            for key in recipe_dict['raw_materials']:
                print('\t' + '- ' + key)

        elif split_command[1] == recipes_check:
            #display all recipes
            print(':::Recipes:::')
            for key in recipe_dict['recipes']:
                print('\t' + key, '- produced in increments of', recipe_dict['recipes'][key]['output_count'])
                print('\t' + 'Required Materials:')
                for i in recipe_dict['recipes'][key]['parts']:
                    print('\t' + '  ' + i + ':', recipe_dict['recipes'][key]['parts'][i])

    elif split_command[0] == how_many_check:
        #calculate how many (x)'s are in a (y)
        item_searched = split_command[search_item]
        item_analyzed = split_command[analyze_num]
        multiplier = 1
        current_amount = 0
        total_amount = calculate_amount(recipe_dict, item_searched, item_analyzed, multiplier, current_amount)
        print('There are', total_amount, item_searched, 'in a', item_analyzed)

#run the entire game with the necessary loops
def run_game():
#constants for the game
    recipe_dict = {}
    stockpile = {}
    factory_dict = {'0': '', '1': ''}
    mine_dict = {'0': '', '1': ''}
    factory_check = 'factory'
    mine_check = 'mine'
    quit_command = 'quit'
    end_turn_command = 'end turn'
    turn_count = 1
    factory_production = Factory(100, 'none')
    end_turn = False
    produce_factory = False
#load json file
    file_name = str(input('Enter the SC Recipe File Name: '))

    open_file = open(file_name, 'r')
    json_string = open_file.read()
    recipe_dict = json.loads(json_string)
    
    next_action = input('Select Next Action>> ')
    get_command(recipe_dict, next_action, factory_dict, mine_dict, stockpile)
    while next_action != quit_command:
        while end_turn != True and next_action != quit_command:
            next_action = input('Select Next Action>> ')
            get_command(recipe_dict, next_action, factory_dict, mine_dict, stockpile)
            if next_action == end_turn_command:
                end_turn = True
#perform post-turn actions
        print('Mining...')
        for key in mine_dict:
            current_mine = Mine(key, mine_dict[key])
            current_mine.mine_material(recipe_dict, stockpile)
        print('Making...')
        for key in factory_dict:
            current_factory = Factory(key, factory_dict[key])
            if current_factory.recipe != factory_check:
                current_factory.make_product(recipe_dict, stockpile, factory_check, mine_check, factory_dict, mine_dict)
            elif current_factory.recipe == factory_check:
                factory_production = Factory(key, factory_dict[key])
                produce_factory = True
        if produce_factory == True:
            factory_production.make_product(recipe_dict, stockpile, factory_check, mine_check, factory_dict, mine_dict)
        
        print('Turn', turn_count, 'Complete')
        turn_count += 1
        end_turn = False

if __name__ == '__main__':
    import json
    run_game()
