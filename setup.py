from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from jinja2 import Environment, FileSystemLoader, select_autoescape
from query import Queries
from neo4j import GraphDatabase
from neo4jconnect import connect_to_neo4j
import os
from read_css_file import read_css_file
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
driver = connect_to_neo4j()
result = Queries.get_random_recipe_data(driver)
ingredient_cnt= Queries.get_ing_mostcommon(driver)
author_cnt=Queries.get_auth_mostcommon(driver)
MostComplex_recipes=Queries.get_recipe_mostcomplex(driver)
ing_data=Queries.get_ingredients(driver)
class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global result
        global ingredient_cnt
        global author_cnt
        global MostComplex_recipes
        global ing_data
        env = Environment(
            loader=FileSystemLoader(os.path.join(CURRENT_DIR, 'templates')),
            autoescape=select_autoescape(['html', 'xml'])
        )
        if self.path.startswith('/styles/'): 
            file_name = os.path.basename(self.path)
            css_content = read_css_file(file_name)
            if css_content:
                self.send_response(200)
                self.send_header('Content-type', 'text/css') 
                self.end_headers()
                self.wfile.write(css_content.encode('utf-8'))
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Not Found")

        if self.path.startswith('/'):
            query_components = parse_qs(urlparse(self.path).query)
            search_query = query_components.get('search', [''])[0]
            author_recipe_query = query_components.get('author_recipies', [''])[0]
            recipe_details_query=query_components.get('recipe_details', [''])[0]
            ing_query=query_components.get('ing_filter', [''])[0]
            sort_ingAsc_query=query_components.get('nring_asc', [''])[0]
            sort_skill_query=query_components.get('skill_sorted', [''])[0]
            if search_query:  
                filtered_result = [record for record in result if search_query.lower() in record['recipe_name'].lower()]

                page_number = int(query_components.get('page', ['1'])[0])
                items_per_page = 20
                total_pages = (len(filtered_result) + items_per_page - 1) // items_per_page
                start_index = (page_number - 1) * items_per_page
                end_index = min(start_index + items_per_page, len(filtered_result))
                paginated_result = filtered_result[start_index:end_index]

                template = env.get_template('search.html')

                html_content = template.render(search_results=paginated_result,
                                               total_pages=total_pages,
                                               search_query=search_query)

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(html_content.encode('utf-8'))

            elif author_recipe_query:
                author_name = author_recipe_query
                filtered_result = Queries.get_author_recipies(driver, author_name)

                page_number = int(query_components.get('page', ['1'])[0])
                items_per_page = 20
                total_pages = (len(filtered_result) + items_per_page - 1) // items_per_page
                start_index = (page_number - 1) * items_per_page
                end_index = min(start_index + items_per_page, len(filtered_result))
                paginated_result = filtered_result[start_index:end_index]
                
                template = env.get_template('author_recipies.html')

                html_content = template.render(search_results=paginated_result,
                                               total_pages=total_pages,
                                               author_name=author_name,
                                               ing_data=ing_data)
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(html_content.encode('utf-8'))

            elif recipe_details_query:
                recipe_name=recipe_details_query
                recipe_data=Queries.get_recipe_data(driver,recipe_name)
                similar_recipies=Queries.get_similar_recipies(driver,recipe_name)
                #similar_recipies[0]['commonIngredientNames'] = ', '.join(similar_recipies[0]['commonIngredientNames'])
                recipe_data[0]['ingredients'] = ', '.join(recipe_data[0]['ingredients'])

                template = env.get_template('recipe_details.html')

                html_content = template.render(recipe_result=recipe_data,similar_recipies=similar_recipies)
    
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(html_content.encode('utf-8'))

            elif ing_query:
                ing_id = ing_query
                filtered_result = Queries.get_ingSpecific(driver, ing_id)
                page_number = int(query_components.get('page', ['1'])[0])
                items_per_page = 20
                total_pages = (len(filtered_result) + items_per_page - 1) // items_per_page
                start_index = (page_number - 1) * items_per_page
                end_index = min(start_index + items_per_page, len(filtered_result))
                paginated_result = filtered_result[start_index:end_index]

                template = env.get_template('ing_filter.html')

                html_content = template.render(search_results=paginated_result,
                                               total_pages=total_pages,
                                               ing_id=ing_id,
                                               )
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(html_content.encode('utf-8'))
            elif sort_ingAsc_query:
                    page_number = int(query_components.get('page', ['1'])[0])
                    status=sort_ingAsc_query
                    result_ing=Queries.get_sortingIng(driver,status)

                    page_number = int(query_components.get('page', ['1'])[0])
                    items_per_page = 20
                    total_pages = (len(result_ing) + items_per_page - 1) // items_per_page
                    interval = 10 
                    start_page = max(1, page_number - interval)
                    end_page = min(total_pages, page_number + interval)
                    start_index = (page_number - 1) * items_per_page
                    end_index = min(start_index + items_per_page, len(result_ing))
                    paginated_result = result_ing[start_index:end_index]

                    template = env.get_template('nring_asc.html')

                    html_content = template.render(paginated_result=paginated_result, 
                                                   start_page=start_page, 
                                                   end_page=end_page,
                                                   ingredient_cnt=ingredient_cnt,
                                                   author_cnt=author_cnt,
                                                   MostComplex_recipes=MostComplex_recipes,
                                                   ing_data=ing_data,
                                                   status=status
                                                   )
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(html_content.encode('utf-8'))
            elif sort_skill_query:
                    page_number = int(query_components.get('page', ['1'])[0])
                    status=sort_skill_query
                    statusClone=status
                    result_ing=Queries.get_sortingSkill(driver,status,statusClone)
                    
                    items_per_page = 20
                    total_pages = (len(result_ing) + items_per_page - 1) // items_per_page
                    interval = 10 
                    start_page = max(1, page_number - interval)
                    end_page = min(total_pages, page_number + interval)
                    start_index = (page_number - 1) * items_per_page
                    end_index = min(start_index + items_per_page, len(result_ing))
                    paginated_result = result_ing[start_index:end_index]

                    template = env.get_template('skill_sorted.html')
                 
                    html_content = template.render(paginated_result=paginated_result, 
                                                   start_page=start_page, 
                                                   end_page=end_page,
                                                   ingredient_cnt=ingredient_cnt,
                                                   author_cnt=author_cnt,
                                                   MostComplex_recipes=MostComplex_recipes,
                                                   ing_data=ing_data,
                                                   status=status,
                                                   statusClone=status
                                                   )
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(html_content.encode('utf-8'))        
            else:  
                if self.path == '/' or self.path.startswith('/index.html'):
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

                    query_components = parse_qs(urlparse(self.path).query)
                    page_number = int(query_components.get('page', ['1'])[0])

                    items_per_page = 20
                    total_pages = (len(result) + items_per_page - 1) // items_per_page
                    interval = 10  
                    start_page = max(1, page_number - interval)
                    end_page = min(total_pages, page_number + interval)
                    start_index = (page_number - 1) * items_per_page
                    end_index = min(start_index + items_per_page, len(result))
                    paginated_result = result[start_index:end_index]

                    template = env.get_template('index.html')
                    
                    html_content = template.render(paginated_result=paginated_result, 
                                                   start_page=start_page, 
                                                   end_page=end_page,
                                                   ingredient_cnt=ingredient_cnt,
                                                   author_cnt=author_cnt,
                                                   MostComplex_recipes=MostComplex_recipes,
                                                   ing_data=ing_data
                                                   )
                    
                    self.wfile.write(html_content.encode('utf-8'))
                elif self.path.startswith('/home'):

                    query_components = parse_qs(urlparse(self.path).query)
                    page_number = query_components.get('page', ['1'])[0]
                    self.redirect_to_index(page_number)
                else:
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(b"Not Found")
                    
    def redirect_to_index(self, page_number):
        self.send_response(301)
        self.send_header('Location', '/index.html?page=' + page_number)
        self.end_headers()

def run():
    print('Starting server...')
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyHTTPRequestHandler)
    print('Server running at http://localhost:8000')
    httpd.serve_forever()

run()
