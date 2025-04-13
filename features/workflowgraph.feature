Feature: WorkflowGraph functionality

  Scenario: Executing a full WorkflowGraph
    Given a WorkflowGraph with the diamond graph
    And a sample context
    When the WorkflowGraph is executed
    Then the WorkflowGraph should return the expected result


 #Feature: WorkflowGraph functionality
 #
 #  Scenario: WorkflowGraph added node with Task
 #    Given a WorkflowGraph
 #    And a sample adding Task with Signature(2,KeyGetter('a'))
 #    And sample context {'a':3}
 #    When the Task is added as node to the WorkflowGraph
 #    And the WorkflowGraph is executed
 #    Then WorkflowGraph should return 5
 #
 #  Scenario: WorkflowGraph added node with Workflow
 #    Given a WorkflowGraph
 #    And a Workflow 
 #    And a sample context
 #    When the Workflow is added as node to the WorkflowGraph
 #    And Workflow is called
 #    Then the Workflow should execute correctly
 #
 #  Scenario: WorkflowGraph with two nodes connected with edge
 #    Given a WorkflowGraph
 #    And two Tasks connected with an edge
 #    When the WorkflowGraph is executed
 #    Then WorkflowGraph should return what is expected
 #
 #  Scenario: WorkflowGraph traverses multiple nodes
 #    Given a WorkflowGraph
 #    And nodes node1, node2, node3, and node4
 #    And edges connecting node1 to node2, node1 to node3, node2 to node4, and node3 to node4
 #    When the WorkflowGraph is traversed
 #    Then the nodes should be visited in the correct order
 #
 #  Scenario: WorkflowGraph copes with loops
 #    Given a WorkflowGraph
 #    And nodes that form a loop
 #    When the WorkflowGraph is executed
 #    Then an error should be raised
 #
 #  Scenario: WorkflowGraph checks connectivity - correct sample
 #    Given a WorkflowGraph with correctly connected nodes and edges
 #    When the connectivity is checked
 #    Then the nodes and edges should be correctly connected
 #
 #  Scenario: WorkflowGraph checks connectivity - incorrect sample
 #    Given a WorkflowGraph with incorrectly connected nodes and edges
 #    When the connectivity is checked
 #    Then WorkflowGraph should return info about disconnected elements
 #
 #  Scenario: WorkflowGraph checks connectivity - missing elements
 #    Given a WorkflowGraph with correctly connected nodes and edges but missing node
 #    When the connectivity is checked
 #    Then WorkflowGraph should return info about disconnected elements
 #
 #  Scenario: WorkflowGraph prints graph paths
 #    Given a WorkflowGraph
 #    And nodes and edges
 #    When the graph paths are printed
 #    Then the paths should be displayed correctly

  # Suggested additional scenarios:
  # Scenario: WorkflowGraph handles parallel tasks
  #   Given a WorkflowGraph
  #   And multiple Tasks that can run in parallel
  #   When the WorkflowGraph is executed
  #   Then the Tasks should execute concurrently

  # Scenario: WorkflowGraph handles conditional execution
  #   Given a WorkflowGraph
  #   And a Task with a conditional execution path
  #   When the condition is met
  #   Then the Task should follow the correct path
