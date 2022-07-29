# Testing

We test this tool really heavily, ensuring that the signatures we design actually detect the takeover conditions we plan for.

We use the pytest framework to do this, which discovers tests in this folder.

Every signature of the standard classes is tested, and this is automatic without any test configuration needed.  

Some of our tests are active, meaning that we perform a modified request to simulate the actual takeover condition.  

``` Example: We will send a web request to Github pages for a random host, and then check to make sure we detect that we can take it over ```

These can be disabled when running the pytest by using the param: ``` -k  "not active ```

Testing is also performed on the individual components, and we mock different functions to validate edge cases such as if we provided a single item, multiple items or no items.

## Adding a test

The test structure here is loosely organised, so please put tests in a relevant location.

All test files should begin ```test_``` and all functions should also begin ```test_```.  All test functions should run without a parameter, unless using paramaterised tests.

It may be easier copying the tests that resemble what you want to achieve as we quite often replace functions within the tool to force a condition.  This can be quite complex.