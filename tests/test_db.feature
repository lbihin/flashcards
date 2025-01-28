Feature: Database Initialization

  Scenario: Initialize the database and create tables
    Given the database does not exist
    When the init_db function is called
    Then the database and tables should be created
    And predefined themes should be inserted

  Scenario: Prevent reinitialization of the database
    Given the database does not exist
    When the init_db function is called
    And the init_db function is called again
    Then an error should be logged

  Scenario: Handle database connection error
    Given the database path is invalid
    When the init_db function is called
    Then an error should be logged
