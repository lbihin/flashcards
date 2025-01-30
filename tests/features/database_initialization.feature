Feature: Database Initialization

  Scenario: Initialize the database and create tables
    Given the database does not exist
    When the init_db function is called
    Then the database and tables should be created
    And predefined themes should be inserted

  Scenario: Prevent setup re-initialization
    Given the database exists
    When the setup_config function is called again with a different path
    Then a ValueError should be raised

  Scenario: Re-initialize the database with the same path
    Given the database exists
    When the init_db function is called again with the same path
    Then no error should be raised
    And no new themes should be inserted
