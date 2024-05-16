from neo4jconnect import connect_to_neo4j

driver = connect_to_neo4j()

class Queries():

    def get_random_recipe_data(driver):
        query = """
        MATCH (a:Author)-[i:WROTE]->(r:Recipe)
        OPTIONAL MATCH (r)-[:CONTAINS_INGREDIENT]->(ingredient)
        RETURN a.name AS author_name,
        id(r) as rcp_id,
        id(a) AS author_id,
        r.skillLevel AS skill_level,
        r.preparationTime AS preparation_time,
        r.name AS recipe_name,
        r.description AS recipe_description,
        r.cookingTime AS recipe_cookingTime,
        collect(ingredient.name) AS ingredients,
        collect(ingredient.id) AS ingredients_id,
        count(ingredient) AS ingredients_count
        ORDER BY r.name ASC
        LIMIT 33411
        """
        
        with driver.session() as session:
            result = session.run(query)
            data = []
            rcp_ids = []  
            for record in result:
                rcp_ids.append(record['rcp_id'])  
                data.append({
                    'rcp_id':record['rcp_id'],
                    'author_id': record['author_id'],
                    'author_name': record['author_name'],
                    'recipe_name': record['recipe_name'],
                    'preparation_time': record['preparation_time'],
                    'skill_level': record['skill_level'],
                    'ingredients_count': record['ingredients_count'],
                    'recipe_description': record['recipe_description'],
                    'recipe_cookingTime': record['recipe_cookingTime'],
                    'ingredients': record['ingredients'],
                    'ingredients':record['ingredients_id']
                })
        return data

    def get_author_recipies(driver, author_id):
        limit_value = 33333
        query = """
        MATCH (r:Recipe)<-[i:WROTE]-(a:Author) 
        WHERE id(a) = {}
        OPTIONAL MATCH (r)-[:CONTAINS_INGREDIENT]->(ingredient)
        RETURN a.name AS author_name, 
        id(a) AS author_id, 
        r.skillLevel AS skill_level,
        r.preparationTime AS preparation_time,
        r.name AS recipe_name,
        count(ingredient) AS ingredients_count
        ORDER BY r.name ASC
        LIMIT {}
        """.format(author_id, limit_value)

        with driver.session() as session:
            result = session.run(query, author_id=author_id)
            data = []
            for record in result:
                data.append({
                    'author_id': record['author_id'],
                    'author_name': record['author_name'],
                    'recipe_name': record['recipe_name'],
                    'preparation_time': record['preparation_time'],
                    'skill_level': record['skill_level'],
                    'ingredients_count':record['ingredients_count']
                })
        return data
    def get_recipe_data(driver, rcp_name):
        limit_value = 1
        query = """
        MATCH (r:Recipe WHERE id(r)={})
        OPTIONAL MATCH (r)-[:COLLECTION]->(collection)
        OPTIONAL MATCH (r)-[:KEYWORD]->(keyword)
        OPTIONAL MATCH (r)-[:DIET_TYPE]->(diet)
        OPTIONAL MATCH (r)-[:CONTAINS_INGREDIENT]->(ingredient)
        RETURN r.cookingTime AS recipe_cookingTime,
        r.name AS rcp_name,
        r.description AS recipe_description,
        r.preparationTime AS recipe_preparationTime,
        r.name AS recipe_name,
        collect(DISTINCT collection.name) AS collections,
        collect(DISTINCT keyword.name) AS keywords,
        collect(DISTINCT diet.name) AS diet_types,
        collect(DISTINCT ingredient.name) AS ingredients
        LIMIT {}
        """.format(rcp_name, limit_value)

        with driver.session() as session:
            result = session.run(query, rcp_name=rcp_name)
            data = []
            for record in result:
                data.append({
                    'rcp_name': record['rcp_name'],
                    'recipe_description': record['recipe_description'],
                    'recipe_preparationTime': record['recipe_preparationTime'],
                    'recipe_cookingTime': record['recipe_cookingTime'],
                    'ingredients': record['ingredients'],
                    'collections': record['collections'],
                    'keywords': record['keywords'],
                    'diet_types': record['diet_types']

                })
        return data
    
    def get_ing_mostcommon(driver):
    
        query = """
        MATCH (i:Ingredient)<-[:CONTAINS_INGREDIENT]-(r:Recipe)
        RETURN i.name AS ingredient, count(r) AS recipe_count
        ORDER BY recipe_count DESC
        LIMIT 5
        """

        with driver.session() as session:
            result = session.run(query)
            data = []
            for record in result:
                data.append({
                    'ingredient': record['ingredient'],
                    'recipe_count': record['recipe_count'],
                })
        return data
    def get_auth_mostcommon(driver):
    
        query = """
        MATCH (a:Author)-[:WROTE]->(r:Recipe)-[:CONTAINS_INGREDIENT]->(i:Ingredient)
        RETURN a.name AS author_name, count(r) AS recipe_nr
        ORDER BY recipe_nr DESC
        LIMIT 5

        """
        with driver.session() as session:
            result = session.run(query)
            data = []
            for record in result:
                data.append({
                    'author_name': record['author_name'],
                    'recipe_nr': record['recipe_nr'],
                })
        return data
    def get_recipe_mostcomplex(driver):
    
        query = """
        MATCH (r:Recipe)-[:CONTAINS_INGREDIENT]->(i:Ingredient)
        WHERE r.skillLevel = 'A challenge'
        WITH r, COUNT(i) AS ingredientCount
        ORDER BY ingredientCount DESC, r.preparationTime DESC
        RETURN r.name AS recipes_names, r.preparationTime AS PreparationTime, ingredientCount AS IngredientCount
        LIMIT 5
        """
        with driver.session() as session:
            result = session.run(query)
            data = []
            for record in result:
                data.append({
                    'recipes_names': record['recipes_names']
                })
        return data
    
    def get_ingredients(driver):
    
        query = """
        MATCH (n:Ingredient)
        RETURN n.name as ing_name,
        id(n) as ing_id
        ORDER BY n.name ASC;
        """

        with driver.session() as session:
            result = session.run(query)
            data = []
            for record in result:
                data.append({
                    'ing_name': record['ing_name'],
                    'ing_id': record['ing_id']
                })
        return data
    def get_ingSpecific(driver,ing_id):
        limit_value = 4000
        query = """
       MATCH (r:Recipe)-[:CONTAINS_INGREDIENT]->(i:Ingredient) WHERE id(i)={}
        RETURN r.name as recipe_name,
        id(r) as rcp_id,
         r.preparationTime as preparation_time,
        r.skillLevel as skillLevel,
        id(i) as ing_id
        LIMIT {}
        """.format(ing_id,limit_value)

        with driver.session() as session:
            result=session.run(query, ing_id=ing_id)
            data = []
            for record in result:
                data.append({
                    'rcp_id': record['rcp_id'],
                    'recipe_name': record['recipe_name'],
                    'preparation_time': record['preparation_time'],
                    'skillLevel': record['skillLevel'],
                    'ing_id': record['ing_id']
                })
        return data
    def get_similar_recipies(driver,recipe_id):
        limit_value = 5
        query = """
        MATCH (selectedRecipe:Recipe)-[:CONTAINS_INGREDIENT]->(ingredient:Ingredient)
        WHERE id(selectedRecipe) = {}
        WITH selectedRecipe, collect(ingredient) AS selectedIngredients, size(collect(ingredient)) AS totalSelectedIngredients

        MATCH (otherRecipe:Recipe)-[:CONTAINS_INGREDIENT]->(otherIngredient:Ingredient)
        WHERE otherRecipe <> selectedRecipe
        WITH selectedRecipe, selectedIngredients, totalSelectedIngredients, otherRecipe, collect(otherIngredient) AS otherIngredients, size(collect(otherIngredient)) AS totalOtherIngredients

        MATCH (a:Author)-[:WROTE]->(otherRecipe) 

        WITH otherRecipe, a, totalOtherIngredients, 
        size([ingredient IN otherIngredients WHERE ingredient IN selectedIngredients]) AS commonIngredientsCount,
        [ingredient IN otherIngredients WHERE ingredient IN selectedIngredients | ingredient.name] AS commonIngredientNames,
        otherRecipe.preparationTime AS preparationTime, 
        otherRecipe.cookingTime AS cookingTime,
        otherRecipe.skillLevel AS skillLevel,
        id(otherRecipe) AS recipe_id
        ORDER BY commonIngredientsCount DESC    

        RETURN otherRecipe.name AS recipe_name, 
        commonIngredientsCount, 
        totalOtherIngredients, 
        preparationTime, 
        cookingTime, 
        skillLevel, 
        commonIngredientNames,
        recipe_id,
        a.name as author_name,
        id(a) AS author_id
        LIMIT {}
        """.format(recipe_id,limit_value)

        with driver.session() as session:
            result=session.run(query, recipe_id=recipe_id)
            data = []
            for record in result:
                data.append({
                    'recipe_name': record['recipe_name'],
                    'commonIngredientsCount': record['commonIngredientsCount'],
                    'totalOtherIngredients': record['totalOtherIngredients'],
                    'preparationTime': record['preparationTime'],
                    'cookingTime': record['cookingTime'],
                    'skillLevel': record['skillLevel'],
                    'commonIngredientNames':record['commonIngredientNames'],
                    'recipe_id': record['recipe_id'],
                    'author_id': record['author_id'],
                    'author_name': record['author_name']
                })
        return data
    def get_sortingIng(driver,status):
        query = """
        MATCH (a:Author)-[i:WROTE]->(r:Recipe)
        OPTIONAL MATCH (r)-[:CONTAINS_INGREDIENT]->(ingredient)
        RETURN a.name AS author_name,
        id(r) as rcp_id,
        id(a) AS author_id,
        r.skillLevel AS skill_level,
        r.preparationTime AS preparation_time,
        r.name AS recipe_name,
        r.description AS recipe_description,
        r.cookingTime AS recipe_cookingTime,
        collect(ingredient.name) AS ingredients,
        collect(ingredient.id) AS ingredients_id,
        count(ingredient) AS ingredients_count
        ORDER BY ingredients_count {}
        LIMIT 33411
        """.format(status)
        
        with driver.session() as session:
            result=session.run(query, status=status)
            data = []
            rcp_ids = []  
            for record in result:
                rcp_ids.append(record['rcp_id'])  
                data.append({
                    'rcp_id':record['rcp_id'],
                    'author_id': record['author_id'],
                    'author_name': record['author_name'],
                    'recipe_name': record['recipe_name'],
                    'preparation_time': record['preparation_time'],
                    'skill_level': record['skill_level'],
                    'ingredients_count': record['ingredients_count'],
                    'recipe_description': record['recipe_description'],
                    'recipe_cookingTime': record['recipe_cookingTime'],
                    'ingredients': record['ingredients'],
                    'ingredients':record['ingredients_id']
                })
        return data
    def get_sortingSkill(driver,status,statusClone):
        query = """
        MATCH (a:Author)-[i:WROTE]->(r:Recipe)
        OPTIONAL MATCH (r)-[:CONTAINS_INGREDIENT]->(ingredient)
        RETURN a.name AS author_name,
        id(r) AS rcp_id,
        id(a) AS author_id,
        r.skillLevel AS skill_level,
        r.preparationTime AS preparation_time,
        r.name AS recipe_name,
        r.description AS recipe_description,
        r.cookingTime AS recipe_cookingTime,
        collect(ingredient.name) AS ingredients,
        collect(ingredient.id) AS ingredients_id,
        count(ingredient) AS ingredients_count
        ORDER BY CASE r.skillLevel
            WHEN 'Easy' THEN 1
            WHEN 'More effort' THEN 2
            WHEN 'A challenge' THEN 3
            ELSE 0
        END {}, 
        skill_level {}
        LIMIT 33411

        """.format(status,statusClone)
        
        with driver.session() as session:
            result=session.run(query, status=status, statusClone=statusClone)
            data = []
            rcp_ids = []  
            for record in result:
                rcp_ids.append(record['rcp_id'])  
                data.append({
                    'rcp_id':record['rcp_id'],
                    'author_id': record['author_id'],
                    'author_name': record['author_name'],
                    'recipe_name': record['recipe_name'],
                    'preparation_time': record['preparation_time'],
                    'skill_level': record['skill_level'],
                    'ingredients_count': record['ingredients_count'],
                    'recipe_description': record['recipe_description'],
                    'recipe_cookingTime': record['recipe_cookingTime'],
                    'ingredients': record['ingredients'],
                    'ingredients':record['ingredients_id']
                })
        return data
    