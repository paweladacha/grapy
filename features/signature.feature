Feature: Signature
  Scenario: Signature can be updated 
    Given I have sample Signature
    When I insert argument at zero index
    Then Signature has that argument at zero index
