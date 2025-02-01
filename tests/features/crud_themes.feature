Feature: CRUD operations on themes

  Scenario: create a new theme
    Given the database is initialized
    When a new theme is created with name "Science"
    Then the theme "Science" should be present in the database

  Scenario: Attempt to create a duplicate theme
    Given the database is initialized
    And a theme exists with ID 1 and name "Math"
    When a new theme is created with name "Math"
    Then an error should be logged indicating the theme already exists

  Scenario: get a theme by ID
    Given the database is initialized
    And a theme exists with ID 1
    When the theme is retrieved by ID 1
    Then the theme with ID 1 should be returned

  Scenario: Attempt to get a non-existent theme by ID
    Given the database is initialized
    When the theme is retrieved by ID 999
    Then no theme should be returned

  Scenario: Update a theme
    Given the database is initialized
    And a theme exists with ID 1 and name "Math"
    When the theme with ID 1 is updated to "Science"
    Then the theme with ID 1 should have the name "Science"

  Scenario: Attempt to update a non-existent theme
    Given the database is initialized
    When the theme with ID 999 is updated to "History"
    Then an error should be logged indicating the row in themes with ID 999 was not found

  Scenario: Delete a theme
    Given the database is initialized
    And a theme exists with ID 1 and name "Math"
    When the theme with ID 1 is deleted
    Then the theme with ID 1 should not be present in the database

  Scenario: Attempt to delete a non-existent theme
    Given the database is initialized
    When the theme with ID 999 is deleted
    Then an error should be logged indicating the row in themes with ID 999 was not found

  Scenario: Get all themes
    Given the database is initialized
    And 3 themes exist in the database
    When all themes are retrieved
    Then 3 themes should be returned