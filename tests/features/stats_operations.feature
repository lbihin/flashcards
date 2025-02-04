Feature: Operations on card probabilities and stats

  Scenario: Update card probability with incorrect answer
    Given the database is initialized
    And a card exists with ID 1 and probability 0.5
    When the card with ID 1 with incorrect answer is updated
    Then the card with ID 1 should have the probability 0.55

  Scenario: Update card probability with correct answer
    Given the database is initialized
    And a card exists with ID 1 and probability 0.5
    When the card with ID 1 with correct answer is updated
    Then the card with ID 1 should have the probability 0.45

  Scenario: Attempt to update probability of a non-existent card
    Given the database is initialized
    When the card with ID 999 with incorrect answer is updated
    Then an error should be logged indicating the card with ID 999 was not found

  Scenario: Successfully update exiting stats with correct answer
    Given the database is initialized
    And stat exist or is created and contain 5 correct answers and 3 incorrect answers
    When the stat is updated with a correct answer
    Then the stat should have 6 correct answers and 3 incorrect answers

  Scenario: Successfully update exiting stats with incorrect answer
    Given the database is initialized
    And stat exist or is created and contain 5 correct answers and 3 incorrect answers
    When the stat is updated with a incorrect answer
    Then the stat should have 5 correct answers and 4 incorrect answers

  Scenario: Successfully update new stats with correct answer
    Given the database is initialized
    And the daily stat does not exist
    When the stat is updated with a correct answer
    Then the stat should have 1 correct answers and 0 incorrect answers

    Scenario: Successfully update new stats with incorrect answer
    Given the database is initialized
    And the daily stat does not exist
    When the stat is updated with a incorrect answer
    Then the stat should have 0 correct answers and 1 incorrect answers