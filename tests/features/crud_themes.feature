Feature: CRUD operations on themes

  Scenario: Successfully create a new theme
    Given the database is initialized
    When a new theme is created with name "Science"
    Then the theme "Science" should be present in the database

  Scenario: Attempt to create a duplicate theme
    Given the database is initialized
    And a theme exists with name "Math"
    When a new theme is created with name "Math"
    Then an error should be logged indicating the theme already exists