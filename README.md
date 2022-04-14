# Lí Express

## Hexagonal Architecture

Hexagonal Architecture has been used in this project. It has been implemented with dependency injection. This dependency injection is made by [bootstap.py](./liexpress/bootstrap.py) and its function
_configure_inject()_. The injection selected is based on an environment variable called **ENV**. Possible values: "dev"
> ENV=dev

Product samples are treated as a dependency.

## Fast API

### Security

An API key list is supported in the header request. They should be set in a environment variable called **API_KEYS** at the execution of the project:
> API_KEYS="1234,0000"

To make a request sending this API KEY, a header should be set:
> Authorization: 1234
