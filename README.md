# Djbehave

Djbehave exposes [Behave](http://pythonhosted.org/behave/) for use under [Django](https://www.djangoproject.com/).
It provides a `manage.py behave` analogue to Django's `manage.py test` command (**command line switches have not been propogated through to configure Behave, so only the default works right now**), maintaining the feel of Django's unittest interface.
Djbehave requires [Subbehave](https://github.com/popham/subbehave).

## Typical Use
The system's architecture exposes the [test database](https://docs.djangoproject.com/en/1.6/topics/testing/overview/#the-test-database) and a [test server](https://docs.djangoproject.com/en/1.6/topics/testing/tools/#liveservertestcase) for manipulation from Behave.
The architecture should support additional resources, whatever they may be.
My projects currently use hooks from Behave to start a test server and alter the state of my test database, e.g.

```python
from djbehave.server.command import CreateTestServer, Flush, LoadFixtures

def before_all(context):
    CreateTestServer().trigger(context.config)

def before_tag(context, tag):
    if tag == 'flush':
        Flush().trigger(context.config)
    if tag == 'oauth_fixtures':
        LoadFixtures('user/oauth').trigger(context.config)
```

The `before_all` hook provides the test server resource for all tests to access.
Consider the following [Gherkin](https://github.com/cucumber/cucumber/wiki/Gherkin):

```
Feature: Inactive Oauth User Interaction
  @flush
  @oauth_fixtures
  Scenario: ...
```

Before the scenario runs, the test database gets flushed and then the `user/oauth` fixture gets loaded.
Behave executes tag hooks in the order that they're encountered, so the database gets flushed before the fixtures are loaded.

## Resource Destruction
The command `CreateTestServer` builds a resource that is available until its scope closes.
In the earlier example, the resource was created under the `before_all` hook, giving it global scope and, therefore, making it available to all tests.
Consider the tag hook:

```python
def before_tag(context, tag):
    if tag == 'server':
        CreateTestServer().trigger(context.config)
```

In the absence of the `before_all` hook from earlier, availability of the corresponding resource gets limited to the tagged scopes.
Consider the following Gherkin:

```
@server
Feature: Inactive Oauth User Interaction
  Scenario: ...

Feature: Active Oauth User Interaction
  Scenario: ...
```

My `Inactive Oauth User Interaction` feature, its scenarios, and their steps all have access to the test server resource.
The non-tagged `Active Oauth User Interaction` feature, however, has no such access.

## Deficiencies
  * I have not built any tests for this code.
  * **I have not propogated command line settings into the Behave process.**  I will get around to this in parallel with tests.
  * I operate under Python 3.3.
    - I've used `super()` all over the place, so Python 3.2 and below will not function properly without slight revision (in the time it took to type this, I could have been well on my way).
    - I've imported directly from Unittest in a couple of spots, so earlier versions may not work.
    - Django goes through a lot of trouble to cover Unittest2 functionality--I have not.
  * The reported outcomes lump Behave errors and failures both as a Unittest failure, while a Unittest error never occurs.
