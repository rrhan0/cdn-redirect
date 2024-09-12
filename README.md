# My Archive

A Flask-based web application for archiving and retrieving snapshots of web pages using MongoDB and GridFS. This application allows users to create and list snapshots of web pages, which are stored in a MongoDB database.

### Endpoints

- **GET `/status`**  
  Returns the uptime and current date of the server.

- **GET `/archive/{url}`**  
  Lists all snapshots for the specified URL.

- **POST `/archive/{url}`**  
  Creates a new snapshot for the specified URL and stores it in the database.

- **GET `/archive/{url}/{timestamp}`**  
  Retrieves the HTML content of a specific snapshot identified by the URL and timestamp.

## Acknowledgements

- [webpage2html](https://pypi.org/project/webpage2html/) - Library for generating HTML snapshots.
