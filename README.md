# **anANTara** backend system

The backend of anANTara project is using `Google Cloud Function` to create an endpoint that are gonna be doing small tasks and `Hasura GraphQL Engine` that served in `Hasura Cloud` to be used for basically the whole database management system including a graphql endpoint (without needing to write boilerplate code for crud endpoints) with role based permission that are connected with a `PostgreSQL` Database that served in `Google Cloud SQL`.

## Feature(s)

These are features of the `Google Cloud Function` :

1. User Login

   This is used to authenticate the user using JWT authentication and will give back the response as an Encrypted JWT Claim (JWT Token).
   
   Curl example for the request:
   ```bash
   curl -d '{"username":"foo@bar.com", "password":"something_fishy"}'\
   -H "Content-Type: application/json"\
   -X POST https://us-central1-anantara-dream-team-cap0236.cloudfunctions.net/userlogin
   ```
   
2. User Parser

   This function is used for parsing the given JWT Token and give back the Decrypted JWT Claim as the response.
   
   Curl example for the request:
   ```bash
   curl -d '{"jwt_token":"put_jwt_token_here"}'\
   -H "Content-Type: application/json"\
   -X POST https://us-central1-anantara-dream-team-cap0236.cloudfunctions.net/userparser
   ```
   
For the REST API, we currently could not disclose that information as it actually work as a wrapper to GraphQL endpoint (thus having some secret information) that is available in this link https://anantara.hasura.app/v1/graphql.

Please just use our applications in order to access all the data available for you without needing to access the endpoint directly.

## Development

### Tech Stack

- Google Cloud Function
- Google Cloud SQL
- Hasura GraphQL Engine (https://github.com/hasura/graphql-engine)

### How to Contribute

These are steps that need to be done for development :
- Fork this repository
- Create issue in this repository about what problem you want to fix / what feature you want to add
- Start the development in your own repository by first creating branch that are unique to the development (problem to fix / feature to add)
- Open pull request to this repository and ask maintainer (anantara-android-team) that consist of [@fakhri](https://github.com/fakhrip) to review the PR
- Wait for the review approval and merge if approved

## Deployment

The hasura graphql engine is deployed in [Hasura Cloud](https://hasura.io/cloud/) while others are in Google Cloud Platform
