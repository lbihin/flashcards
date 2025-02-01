Feature: CRUD operations on themes

  Scenario: create a new theme
    Given the database is initialized
    When a new theme is created with name "Science"
    Then the theme "Science" should be present in the database

  Scenario: Attempt to create a duplicate theme
    Given the database is initialized
    And a theme exists with name "Math"
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