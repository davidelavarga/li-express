# Lí Express

## Execution instructions

- To run the service and the database use the following command. It will build the Dockerfile and download and run a postgres database.
    ```
    make run
    ```

    > Li Express service will be expose in [**localhost:5000**](localhost:5000)

- Once the service is running, in order to see the API go to [docs](localhost:5000/docs)

- To build only the Docker image, execute:
    ```
    make build
    ```

    > It will build a Docker image called **liexpress:latest**


- To run the tests, execute:
    ```
    make test
    ```

    > It will run the pytest tests in "tests" folder

---
## Hexagonal Architecture
Hexagonal Architecture has been used in this project. It has been implemented with dependency injection. This dependency injection is made by [bootstap.py](./liexpress/bootstrap.py) and its function _configure_inject()_. The injection selected is based on an environment variable called **ENV**. Possible values: "dev"
> ENV=dev

Product samples are treated as a dependency in order to easily replace a database.

---
## Configuration

A YAML config file is used in this project. In order to use it CONFIG_PATH environent variable should be set.
> CONFIG_PATH=config.yaml

The configurations stored in the config file are loaded with the method called _get_config()_ in [config_loader.py](./liexpress/utils/config_loader.py) and they could be used as a python dictionary.

---
## Fast API

### **Security**

An API key list is supported in the header request. They should be set in a environment variable called **API_KEYS** at the execution of the project:
> API_KEYS="1234,0000"

To make a request sending this API KEY, a header should be set:
> Authorization: 1234

### **Error control**
- HTTP 400:
    | Exception                 | Explanation                        |
    |---------------------------|------------------------------------|
    | OrderCriteriaNotSupported | Order by query param not supported |
    | ReservationIdNotFound     | Reservation ID not found           |
    | ProductNotFound           | Product ID not found               |
    | BadConfigurationError     | Bad order fields for a given product|
    | ProductAlreadyRequested     | When order a product already ordered|

- HTTP 404:
    | Exception                 | Explanation                        |
    |---------------------------|------------------------------------|
    | ActiveProductNotFound     | No active products found           |

- HTTP 503:

    | Exception                 | Explanation                        |
    |---------------------------|------------------------------------|
    | Unhandled Exceptions      | Any unhandled exception            |



---
## Decisions
1. Product creation. A Product is created with a PUT operation to be idempotent. This allows to create new Product or update an existing one
2. Criteria Pattern has been implemented in this project to have a common way to filter the products (reservations) and its fields. It supports pagination but it is not fully implemented due to simplicity
3. UUID4 identifiers. Initially, int identifiers have been used for simplicity. Afterwards, uuid4 has been used to have a realistic solution
4. Products names are managed as lower case although they are returned as capitalize
5. It has been decided not to have a config with the values supported in place holder configurations because these place holders are an frontend concern


---
## Product IDs and Reservation IDs

### Products

| Name    | UUID4                                |
|---------|--------------------------------------|
| Surf    | 5e1d3c2-08c7-40b7-8045-f5748e004b9c  |
| brunch  | 25dae451-7bf4-41f9-ae2d-2307fa8f38ec |
| musseum | bd4ea9f6-e984-46a0-b674-b61302047cb1 |
| spa     | 44b260d9-78c9-47f7-a644-afec0482ae03 |

### Reservations

| UUID4                                |
|--------------------------------------|
| e0388679-f1f4-4b70-87fe-6dba6c66183b |
| 1092a4bd-0e7a-42cc-ab12-12d7155ee772 |
