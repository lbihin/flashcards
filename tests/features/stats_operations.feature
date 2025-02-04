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

  Scenario: Successfully update stats
    Given the database is initialized
    And stat exist or is created and contain 5 correct answers and 3 incorrect answers
    When the stat is updated with a correct answer
    Then the stat should have 6 correct answers and 3 incorrect answers

  Scenario: Attempt to update stats of a non-existent record
    Given the database is initialized
    When the stats with ID 999 are updated to bonnes_reponses 6 and mauvaises_reponses 2
    Then an error should be logged indicating the stats with ID 999 were not found