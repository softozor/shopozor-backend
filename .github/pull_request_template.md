# Shopozor project

## Workflow

* All Softozor members are whitelisted
* When a white-listed author opens a PR, she is triggering the corresponding unit and acceptance tests automatically
* When a white-listed member updates a PR, she is triggering the corresponding unit and acceptance tests again
* When a non-whitelisted member opens a PR, the builder will publish the question `Can one of the admins verify this patch?` to the PR's comment; in that case, one of Softozor's admins can
 
  * comment `ok to test` to accept the PR for testing
  * comment `test this please` for one time test run
  * comment `add to whitelist` to add the PR's author to the whitelist

## Useful build commands

You can use the following commands in your comments:

* `retest this please`: this runs the unit and acceptance tests again