# Documentation
This is the file where all the documentation for this repository will go
## System Design
Below is a class diagram of the project

![Image of the System Design](assets/design.PNG)

Summary:

The program runs through the MediaDatabase class which instantiates a splash screen and menu object. There is then a separate class for each top level window. The Style class is like a helper class it has no objects it only stores the styling values used throughout.

## Versions:

### V2:
SQLite3 implementation for the database to replace the txt file database.
I was thinking about using mysql instead as I haven't used it with python and it gives me an excuse to learn it however, since this program is based around a database having a specific database file is very useful therefore I chose sqlite3.
### V1:
The original program, using a text based database, all functions hand made (not great)