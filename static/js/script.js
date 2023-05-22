function addMeal() {
    var formGroup = document.createElement("div");
    formGroup.className = "form-group";

    var input = document.createElement("input");
    input.type = "text";
    input.name = "meal";
    input.placeholder = "Enter meal type";
    input.required = true;
    formGroup.appendChild(input);

    document.querySelector('form').insertBefore(formGroup, document.querySelector('#submit-button'));
}

// function generateGroceryList() {
//     var groceryList = {};

//     // iterate through each recipe
//     recipes.forEach((recipe, index) => {
//         // iterate through each ingredient in recipe
//         recipe.ingredients.forEach((ingredient) => {
//             // if ingredient is not in grocery list yet, add it
//             if (!groceryList[ingredient]) {
//                 groceryList[ingredient] = [];
//             }

//             // associate the ingredient with its recipe index
//             groceryList[ingredient].push(index + 1);
//         });
//     });

//     var groceryListContainer = document.getElementById('groceryListContainer');
//     groceryListContainer.innerHTML = '';

//     for (var ingredient in groceryList) {
//         var listItem = document.createElement('li');
//         listItem.textContent = `${ingredient} (Recipe ${groceryList[ingredient].join(', ')})`;
//         groceryListContainer.appendChild(listItem);
//     }
// }




function categorizeIngredient(ingredient) {
    var meats = ['chicken', 'beef', 'pork', 'lamb', 'fish', 'shrimp', 'crab', 'lobster', 'salmon', 'tuna', 'trout', 'cod', 'turkey', 'venison', 'duck', 'mussels', 'clams', 'oysters'];
    var vegetables = ['lettuce', 'tomato', 'carrot', 'potato', 'onion', 'pepper', 'garlic', 'cucumber', 'broccoli', 'spinach', 'zucchini', 'cauliflower', 'kale', 'celery', 'eggplant', 'asparagus', 'beets', 'squash', 'sweet potato', 'mushroom'];
    var spices = ['salt', 'pepper', 'paprika', 'oregano', 'basil', 'cinnamon', 'cumin', 'turmeric', 'coriander', 'ginger', 'nutmeg', 'cardamom', 'cloves', 'allspice', 'sage', 'fennel seeds'];
    var oils = ['olive oil', 'vegetable oil', 'canola oil', 'coconut oil', 'sunflower oil', 'sesame oil', 'peanut oil', 'grapeseed oil', 'avocado oil', 'flaxseed oil'];
    var dairy = ['milk', 'cheese', 'butter', 'cream', 'yogurt', 'cheddar', 'mozzarella', 'parmesan', 'feta', 'gouda', 'blue cheese', 'brie', 'sour cream', 'cottage cheese', 'ricotta'];
    var grains = ['rice', 'pasta', 'bread', 'flour', 'oatmeal', 'quinoa', 'cornmeal', 'barley', 'couscous', 'wheat', 'rye', 'buckwheat', 'bulgur', 'millet', 'farro'];
    var fruits = ['apple', 'orange', 'banana', 'berry', 'strawberry', 'blueberry', 'raspberry', 'peach', 'pear', 'lemon', 'lime', 'mango', 'pineapple', 'kiwi', 'grapes', 'watermelon', 'pomegranate', 'coconut', 'avocado'];
    var legumes = ['bean', 'lentil', 'pea', 'chickpea', 'black bean', 'kidney bean', 'pinto bean', 'soybean', 'green beans', 'navy beans', 'lima beans', 'mung beans'];
    var herbs = ['basil', 'thyme', 'rosemary', 'parsley', 'cilantro', 'mint', 'dill', 'chive', 'sage', 'oregano', 'tarragon', 'marjoram', 'bay leaves', 'lemongrass'];
    var condiments = ['ketchup', 'mustard', 'mayonnaise', 'hot sauce', 'soy sauce', 'vinegar', 'relish', 'salsa', 'bbq sauce', 'worcestershire sauce', 'teriyaki sauce', 'hoisin sauce', 'sriracha', 'honey mustard', 'ranch dressing']; 


    var ingredientLower = ingredient.toLowerCase();
    var categories = [
        { name: 'Meats', items: meats },
        { name: 'Vegetables', items: vegetables },
        { name: 'Spices', items: spices },
        { name: 'Oils', items: oils },
        { name: 'Dairy', items: dairy },
        { name: 'Grains', items: grains },
        { name: 'Fruits', items: fruits },
        { name: 'Legumes', items: legumes },
        { name: 'Herbs', items: herbs },
        { name: 'Condiments', items: condiments }
    ];

    for (var category of categories) {
        // if ingredient contains "powder", categorize as "Spices"
        if (ingredientLower.includes('powder')) {
            return 'Spices';
        }
        if (category.items.some(item => ingredientLower.includes(item))) {
            return category.name;
        }
    }

    return 'Others';
}

function generateGroceryList() {
    var groceryList = {};

    // iterate through each recipe
    recipes.forEach((recipe, index) => {
        // iterate through each ingredient in recipe
        recipe.ingredients.forEach((ingredient) => {
            // get the category of the ingredient
            var category = categorizeIngredient(ingredient);

            // if category is not in grocery list yet, add it
            if (!groceryList[category]) {
                groceryList[category] = {};
            }

            // if ingredient is not in category list yet, add it
            if (!groceryList[category][ingredient]) {
                groceryList[category][ingredient] = [];
            }

            // associate the ingredient with its recipe index
            groceryList[category][ingredient].push(index + 1);
        });
    });

    var groceryListContainer = document.getElementById('groceryListContainer');
    groceryListContainer.innerHTML = '';

    // iterate through each category
    for (var category in groceryList) {
        // create a category header
        var categoryHeader = document.createElement('h3');
        categoryHeader.textContent = category;
        groceryListContainer.appendChild(categoryHeader);

        // iterate through each ingredient in category
        for (var ingredient in groceryList[category]) {
            var listItem = document.createElement('li');
            listItem.textContent = `${ingredient} (Recipe ${groceryList[category][ingredient].join(', ')})`;
            groceryListContainer.appendChild(listItem);
        }
    }
}