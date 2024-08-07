# News Dashboard - API

## Description

A RESTful API built with Flask that allows clients to retrieve news headline
information. The JSON resources returned by its 3 routes are structured
according to the *database/schema.sql* file of this project. These routes are
as follows:

1. **/api/headlines**: Allows clients to retrieve news headlines and some
related information
2. **/api/sources**: Allows clients to retrieve info on the news sources that
headlines are gathered from
3. **/api/dates**: Allows clients to retrieve the dates that headlines have been
gathered on

Most of the API's complexity comes from its support of OData-style filtering,
elaborated upon in the Usage section

## Running the API

After getting the code for the API the following steps must be taken before
it can be run:

1. **Install Dependencies:** Install the API's dependencies, listed in the
HeadlineAPI's requirements.txt file

    ```shell
    pip install -r requirements.txt
    ```

2. **Setup Relational Database:** Create a SQL database with the schema found in
*database/schema.sql*. This database must be running when the API is run

3. **Configure Database Connection:** Create a .env file within the HeadlineAPI
folder. This .env file must have a variable called SQLALCHEMY_CONN_STRING set
to equal the connection string for the SQL database from the previous step

The API can now be run in development mode with the command `flask run`

## Usage

The API has 3 routes that accept GET requests: */api/headlines*, */api/sources*
and */api/dates*. Each route supports the following query parameters:

1. **$top**: Clients can use $top to place a maximum on number of resources
returned by the API. Allows for pagination alongside $skip
2. **$skip**: Clients can specify the number of resources that the API skips
before it begins to return resources. Allows for pagination alongside $top
3. **$orderby**: Clients can specify a property that resources will be ordered
by and whether they'll be returned in ascending or descending order
4. **$filter**: Clients can filter results using a variety of operators

$top and $skip are very simple, but $orderby and $filter merit a bit more
explanation

### $orderby

Clients can order results by any of a resources properties. For headlines these
properties are *text*, *date*, *sentiment* and *source*. For sources they're
*name* and *link*. For dates they're *date* and *avg_sentiment*.

After specifying the property to use for ordering, clients must include the order
itself. The word 'asc' is used to tell the API to return results in ascending
order and the word 'desc' is used to tell it to return results in descending
order.

The property and direction should be seperated with a space. Here's an example 
of a URL with a valid $orderby query param:
`http://127.0.0.1:5000/api/headlines?$orderby=sentiment desc`

### $filter
I took inspiration from the [OData API specifications](https://www.odata.org/documentation/)
when implementing the $filter query param, although I only implemented a small
portion of its requirements.

When filtering, clients can use the same resources properties listed for $orderby.
The values for these resources can be constrained with the following operators:

- eq (equal to)
- neq (not equal to)
- gt (greater than)
- ge (greater than or equal to)
- lt (less than)
- le (less than or equal to)

For example, if a client wanted to get all dates with an avg_sentiment greater
than .1 the URL would be as follows:
`http://127.0.0.1:5000/api/dates?$filter=avg_sentiment gt .1`

The values in a $filter statement can be numeric literals (e.g. .1, 3, -201)
or string literals (e.g. 'hello world', '2024-01-01').

Filters can be composed together with the 'and' and 'or' operators. For
example, if a client wanted to get all headlines from the New York Times that
were released after '2024-01-01' the URL would be as follows:
`http://127.0.0.1:5000/api/headlines?$filter=source eq 'New York Times' and date gt '2024-01-01'`

## Testing

I wrote pytest unit tests for the functionality that tokenizes and parses
the $filter query param. These tests are found in the *backend/tests directory*
and can be ran with `pytest test_filter_parser.py`
