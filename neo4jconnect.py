from neo4j import GraphDatabase

URI = "neo4j://34.232.57.230:7687"
AUTH = ("neo4j", "internship-2024")

def connect_to_neo4j():
    """
    Connect to Neo4j database and return the driver object.
    
    :return: Neo4j driver object.
    """
    try:
        driver = GraphDatabase.driver(URI, auth=AUTH)
        driver.verify_connectivity() 
        return driver
    except Exception as e:
        print("Failed to connect to Neo4j database:", e)
        return None
