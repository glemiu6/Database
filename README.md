# Database
### By: Vlad Digori

## Summary
1. About the project
2. Code breakdown

---

## About the project

The main objective of this project is to create a "Database".  

---

## Code breakdown
We make an API so we will know the main structure of the class.  
First we create a class Table with the following methods:  
1. `add(self,item)`-> adds a row in the table
2. `delete(self,item)` -> deletes a row from a table
3. `lookup(self,item)` -> returns a list where the items match
4. `select(self,p)  # p is a function lambda` -> return a new table with only the rows selected
5. `project(self,subscheme,subkey_idx)`-> returns a new table with a different sub scheme and different primary keys
6. `__add__(self,other)` -> returns a new table with all the rows from both tables combined
7.  `__mul__(self,other)` -> returns a new table only with the common rows  
8. `__sub__(self,other)` -> returns a new table where the rows in table 1 doesn't match the rows from table 2
9.  `__pow__(self,other)` -> returns a new table where we make a natural join and the common columns appear one 
10. `__iter__(self)` -> make the object an iterable
11. `__repr__(self)` -> to represent the table 

After that we run some test cases for the Table were we first create a function `make_db()` where we can create and add the test rows for the database.