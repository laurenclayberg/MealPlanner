# Recipes
Recipes can be found in the `catalog` folder. Each recipe follows the format found in `template.txt`.

## Template rules
1. Anything that looks like `<word>` means that you should replace the entire thing with a value. Remove the `<>`.
2. Times always include both hours and minutes. 30 minutes is represented as `0hr 30min`.
3. Category options include: dinner, lunch, breakfast, appetizer, side, snack, party
4. For ingredients, size should be units that you want to see in your shopping list, and literal description is exactly the amount in the recipe.
5. When you add a new ingredient, make sure you also add it to the corresponding section in `ingredients.txt`.
5. Substitutes should be equal quantity substitutes (1lb ground beef sub 1lb ground turkey)
6. Rating is an integer 1 to 5 representing how often recipes will show up in your meal plan. A recipe rated 2 will show up 2 times for every 5 times a recipe rated 5 shows up.
7. The advance section has instructions for parts of the recipe that can be done in advance and `<days>` is the maximum number of days things can be prepped in advance.
8. Credit includes either a link or recipe book and page number for where the recipe came from.
