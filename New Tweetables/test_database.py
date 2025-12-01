from neo4j import GraphDatabase

URI = "neo4j+s://f1c11ed7.databases.neo4j.io"
AUTH = ("neo4j", "79eNFmepYfcx2ganEpeoEpVeny-Is0lKLXok6sHQrSs")

def check_credentials(driver, username, password):
    query = """
        MATCH (u:USER {username: $username, password: $password})
        RETURN u.username AS username
        """
    records, summary, key = driver.execute_query(query, username=username, password=password)
    if len(records) == 0:
        print("No matching user found.")
    else:
        print("User found")
    

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()
    check_credentials(driver, "brian", "brianiscool")
    driver.close()