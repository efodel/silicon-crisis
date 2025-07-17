"""
File:         recipe_maker.py
Author:       Eric Fodel
Last Updated: 5/9/2021
Description:  This program will ask the user
              to input information about the
              raw materials and recipes in the
              game and will create a dictionary
              with this data inside. The dictionary
              will then be loaded into a json file
              to be used in the silicon_crisis.py file.
"""
#ask the user for the full list of raw materials
def get_raw_materials(quit_command, stop_command, recipe_dict):
    raw_material = input('Name the raw material: ')
    mine_rate = int(input('What is the rate at which it is mined? '))

    recipe_dict['raw_materials'][raw_material] = mine_rate

    while raw_material != quit_command and raw_material != stop_command:
        raw_material = input('Name the raw material: ')
        if raw_material != quit_command:
            mine_rate = int(input('What is the rate at which it is mined? '))

            recipe_dict['raw_materials'][raw_material] = mine_rate

#get all recipes; including output, rate of output, ingredients, and how much of each ingredient
def get_recipes(quit_command, stop_command, recipe_dict):
    output = input('Name the output: ')
    rate_of_output = int(input('What is the rate at which it is output? '))
    ingredient = input('Name the ingredient: ')
    amount_of_ingredient = int(input('How much of the ingredient is needed? '))
#add the input data to the dictionary
    recipe_dict['recipes'][output] = {}
    recipe_dict['recipes'][output]['output'] = output
    recipe_dict['recipes'][output]['output_count'] = rate_of_output
    recipe_dict['recipes'][output]['parts'] = {}
    recipe_dict['recipes'][output]['parts'][ingredient] = amount_of_ingredient
#continue receiving ingredients
    while ingredient != quit_command and ingredient != stop_command:
        ingredient = input('Name the ingredient: ')
        if ingredient != quit_command and ingredient != stop_command:
            amount_of_ingredient = int(input('How much of the ingredient is needed? '))

            recipe_dict['recipes'][output]['parts'][ingredient] = amount_of_ingredient
#repeat above process within a while loop
    while output != quit_command and output != stop_command:
        output = input('Name the output: ')
        if output != quit_command and output != stop_command:
            rate_of_output = int(input('What is the rate at which it is output? '))
            ingredient = input('Name the ingredient: ')
            amount_of_ingredient = int(input('How much of the ingredient is needed? '))

            recipe_dict['recipes'][output] = {}
            recipe_dict['recipes'][output]['output'] = output
            recipe_dict['recipes'][output]['output_count'] = rate_of_output
            recipe_dict['recipes'][output]['parts'] = {}
            recipe_dict['recipes'][output]['parts'][ingredient] = amount_of_ingredient

        while ingredient != quit_command and ingredient != stop_command:
            ingredient = input('Name the ingredient: ')
            if ingredient != quit_command and ingredient != stop_command:
                amount_of_ingredient = int(input('How much of the ingredient is needed? '))

                recipe_dict['recipes'][output]['parts'][ingredient] = amount_of_ingredient
    
    
if __name__ == '__main__':
    import json
    quit_command = 'done'
    stop_command = 'stop'
    recipe_dict = {'raw_materials': {}, 'recipes': {}}

    get_raw_materials(quit_command, stop_command, recipe_dict)
    get_recipes(quit_command, stop_command, recipe_dict)
#write the dictionary into the json file
    json_name = str(input('What is the file name? '))

    open_json = open(json_name, 'w')
    dict_to_write = json.dumps(recipe_dict)
    open_json.write(dict_to_write)

    open_json.close()
