Feature: CRUD operations on cards

  Scenario: Create a new card
    Given the database is initialized
    When a new card is created with question "What is Python?", answer "A programming language", probability 0.5 and theme ID 2
    Then the card should be present in the database

  Scenario: Read a card
    Given the database is initialized
    And a card exists with ID 1, question "What is Python?", answer "A programming language", probability 0.5 and theme ID 2
    When the card is retrieved by id 1
    Then the card should have the answer "A programming language"

  Scenario: Update a card
    Given the database is initialized
    And a card exists with ID 1, question "What is Python?", answer "A programming language", probability 0.5 and theme ID 2
    When the card's answer is updated to "A snake"
    Then the card should have the updated answer "A snake"

  Scenario: Delete a card by ID
    Given the database is initialized
    And a card exists with ID 1, question "What is Python?", answer "A programming language", probability 0.5 and theme ID 2
    When the card is deleted by ID 1
    Then the card should not be present in the database

  Scenario: Get all cards
    Given the database is initialized
    And 3 cards exist
    When all cards are retrieved
    Then the number of cards should be 3

  Scenario: Get the number of cards
    Given the database is initialized
    And 3 cards exist
    When the number of cards is retrieved
    Then the number of cards should be 3

  Scenario: Get cards by theme
    Given the database is initialized
    And 2 cards exist with theme ID 1
    When the cards are retrieved by theme ID 1
    Then the number of cards should be 2