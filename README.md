# Github Auto-Review Tool
1. [Setup Instructions](#setup-instructions)
2. [Endpoints](#endpoints)
3. [Troubleshooting](#troubleshooting)
4. [Testing](#testing)
5. [Documentation](#documentation)
6. [Scaling](#scaling)
7. [FAQs](#faqs)

## Setup Instructions

1. **Clone the Repository:**

   ```bash
   git clone <repository_url>
   cd project-directory
   ```

2. **Install Dependencies:**

   Create a virtual environment and install the required packages:

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # On Windows use `.venv\Scripts\activate`
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables:**

   Create a `.env` file in the project root directory with the following variables:

   ```ini
    
   GITHUB_ACCESS_TOKEN=<your_github_access_token>
   LOCAL_DEVELOPMENT=<local_llm_flag>
   OPENAI_API_KEY=<your_openai_api_key>
   REDIS_HOST=<your_redis_host>
   REDIS_PORT=<your_redis_port>
   REDIS_DB=<your_redis_db>
   ENABLE_REDIS=<enable_redis_flag>
   ```
   Environment descriptions:
  - GITHUB_ACCESS_TOKEN: Your GitHub Access Token to access repositories via GitHub API.
  - LOCAL_DEVELOPMENT: Flag to indicate whether to use local LLM (True or False).
  - OPENAI_API_KEY: Your OpenAI API key for GPT models (required if LOCAL_DEVELOPMENT is False).
  - REDIS_HOST: The hostname or IP address of the Redis server (default: localhost).
  - REDIS_PORT: The port on which the Redis server is running (default: 6379).
  - REDIS_DB: The Redis database number (default: 0).
  - ENABLE_REDIS: Flag to enable or disable Redis caching (True or False).

4. **Run app:**
  ```bash
  uvicorn app:app --host 0.0.0.0 --port 8000 --reload
  ```

## Endpoints:

- ### POST `/review`
    This endpoint reviews a GitHub repository based on the provided URL, candidate level, and assignment description.

    ### Request body:
    Send a JSON object with the following format:

    ```json
    {
        "github_repo_url": "URL_of_the_GitHub_repository",
        "candidate_level": "Junior | Middle | Senior",
        "assignment_description": "Description of the assignment"
    }
    ```

    ### Response:
    - **Success (200)**: Returns a JSON object containing the review result. Example:
    ```json
    {
        "review": "Generated review result based on repository analysis"
    }
    ```
    - **Error (500)**: Returns an error message if something goes wrong during processing. Example:
    ```json
    {
        "detail": "Error message"
    }
    ```

    ### Description:
    The `/review` endpoint takes a GitHub repository URL, candidate level, and assignment description as input, processes the repository using the provided AI model, and generates a review of the code present in the repository. The review includes a summary of the code quality, areas of improvement, and overall performance. If any error occurs during the process, the endpoint returns a 500 status code along with the error details.

## Troubleshooting:

- **Common Issues:**
  - Ensure all environment variables are correctly set in the `.env` file.
  - Verify that all dependencies are installed by checking the `requirements.txt` file.

- **Error Messages:**
  - If you encounter errors, check the application logs for detailed error messages and stack traces.


## Testing:

**Run tests:**
```bash
pytest -v
```
**Run tests with coverage:**
1. Install coverage module: 
    ```bash
    pip install pytest-cov
    ```
2. Run coverage: 
    ```bash
    pytest -v --cov=.
    ```

**Coverage report:**
![coverage report img](https://i.imgur.com/lk7XatD.png)

## Documentation:

- **API Documentation:**
  - The API documentation is available at `http://localhost:8000/docs` after starting the application.

## Scaling:

**Handling High Traffic (100+ Requests per Minute):**
To handle high traffic volume, we can implement an **asynchronous processing** model using a **message queue** such as RabbitMQ or Amazon SQS. Every time a user creates a review request, the system can respond with a `message_id` and forward the review request to be processed asynchronously in the background by several workers. The workers can forward the tasks to different queues and process them simultaneously, enabling efficient handling of every review request.

To further enhance throughput, we have already implemented **caching** to store frequently accessed data such as repository paths and previously processed reviews. This reduces the need for repeated requests to external APIs like GitHub and OpenAI, speeding up response times and minimizing unnecessary processing.

**Supporting Large Repositories (100+ Files):**
For large repositories, we have already implemented chunking logic. Chunking splits large files or repositories into smaller fragments for better handling. This keeps memory usage low and enables the system to handle each chunk in parallel, maintaining efficiency in the review process even for large codebases.

**Database and Caching:**
We can use a **NoSQL database** like MongoDB or Cassandra for scalability and store metadata such as review results and repository details. **Redis caching** can be implemented to store frequently accessed data, such as repository paths or previously processed reviews, ensuring fast results and reducing hits to the GitHub and OpenAI APIs.

**Handling API Rate Limits:**
To manage the GitHub API rate limits, we can implement **caching** and store repository metadata to minimize API calls. In case of rate-limiting, we can utilize a **retry mechanism** along with a backoff strategy. Similarly, for managing **OpenAI API rate limits**, we can use a queuing system to control the number of concurrent API calls and ensure cost overruns are kept under control.

**Infrastructure and Auto-Scaling:**
We can leverage **AWS Lambda** or **Kubernetes** cloud services to enable auto-scaling based on traffic demand. This allows the system to handle spikes in traffic and prevents over-provisioning resources during low-traffic times. For monitoring, services like **Prometheus** or **AWS CloudWatch** can track the health of the system and enable automatic adjustments when needed.


## FAQs:

1. **How do I get my OpenAI key?**
   - Create an account in openai platform: https://platform.openai.com
   - Follow the guide for getting API key: https://help.openai.com/en/articles/4936850-where-do-i-find-my-openai-api-key
   - Set up billing: https://platform.openai.com/settings/organization/billing/overview
2. **How do I get my Github token?**
   - Create token here: https://github.com/settings/tokens

