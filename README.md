# FastAPI Application

This API application enables users to create accounts and make posts. Users can authenticate using their email and password. Upon successful authentication, a JWT token is provided, which is required for all subsequent operations.

## Table of Contents

- [API Overview](#api-overview)
  - [Available Endpoints](#available-endpoints)
  - [API Schema](#api-schema)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
- [Usage](#usage)
- [License](#license)
- [Contact](#contact)

## API Overview

### Available Endpoints
<pre><img src="./static/Apis.png" alt="API's image"></pre>

### API Schema
<pre><img src="./static/Api schema.png" alt="API schema"></pre>

## Getting Started

### Prerequisites

Ensure you have the following installed on your system:
- Python 3.6 or higher
- pip (Python package installer)

### Installation

1. **Clone the Repository**
   <pre>git pull &lt;git_url&gt;</pre>

2. **Create a Virtual Environment**
   <pre>python -m venv venv</pre>

3. **Activate the Virtual Environment**
   - On Windows:
     <pre>.\venv\Scripts\activate</pre>
   - On Linux:
     <pre>source venv/bin/activate</pre>

4. **Install Dependencies**
   <pre>pip install -r requirements.txt</pre>

### Running the Application

1. **Navigate to the Application Directory**
   <pre>cd App</pre>

2. **Run the Application**
   <pre>uvicorn run:app --reload</pre>

This will start the FastAPI application, allowing you to interact with the endpoints as described in the API overview.

## Usage

After starting the application, you can interact with the API using any API client (e.g., Postman) or directly via the Swagger UI available at `http://127.0.0.1:8000/docs`.

- **User Registration**: Create a new user account.
- **User Authentication**: Authenticate using email and password to receive a JWT token.
- **Post Creation**: Create posts using the authenticated user's token.
- **Post Retrieval**: Retrieve posts using the authenticated user's token.

## License

This project is licensed under the MIT License. See the <pre>LICENSE</pre> file for details.

## Contact

For further details or queries, please contact the development team at <pre>jaimitlearn@gmail.com</pre>
