import json
import sys

def main():
    try:
        recipes_file = open('../recipes.json','r')
    except IOError:
        print("**ERROR**: Could not find '../recipes.json'. Ensure that this file is present in the project root.")
        sys.exit()

    try:
        recipes = json.load(recipes_file)
    except json.decoder.JSONDecodeError:
        print("**ERROR**: Could not read '../recipes.json'. Ensure that this file has proper JSON syntax and follows the project conventions for defining recipe values. See here for more information.")
        sys.exit()

    print(json.dumps(recipes, indent=4))

if __name__ == "__main__":
    main()