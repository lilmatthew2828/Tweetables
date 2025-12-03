import tkinter as tk
import threading
import subprocess
import os
import sys
import unittest
import tkinter.messagebox
from neo4j import GraphDatabase

URI = "neo4j+s://f1c11ed7.databases.neo4j.io"
AUTH = ("neo4j", "79eNFmepYfcx2ganEpeoEpVeny-Is0lKLXok6sHQrSs")

class TestNeo4jDatabaseConnection(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = GraphDatabase.driver(URI, auth=AUTH)
        cls.driver.verify_connectivity()

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()



    def test1AddUser(self):                                                              
        query = """                                                                      
            CREATE (u:USER {username: $username, password: $password})
            RETURN u.username AS username
            """
        records, _, _ = self.driver.execute_query(                                       
            query, username="testuser", password="testpass"
        )
        self.assertTrue(len(records) == 1)                                                                                

    def test2VerifyUser(self):                                                          
        query = """                                                                      
            MATCH (u:USER {username: $username, password: $password})
            RETURN u.username AS username
            """
        records, _, _ = self.driver.execute_query(                                     
            query, username="testuser", password="testpass"
        )
        self.assertTrue(len(records) >0 and records[0]["username"] == "testuser", "Node not found in database")                                             

    def test3DeleteUser(self):                                                          
        deleteQuery = """                                                                      
            MATCH (u:USER {username: $username})
            DELETE u
            """
        self.driver.execute_query(                                                     
            deleteQuery, username="testuser"
        )
        # Verify deletion
        verify_query = """
            MATCH (u:USER {username: $username})
            RETURN u.username AS username
            """
        records, _, _ = self.driver.execute_query(                                     
            verify_query, username="testuser"
        )
        self.assertTrue(len(records) == 0, "Node was not deleted from database")       

if __name__ == "__main__":
    unittest.main()
        
