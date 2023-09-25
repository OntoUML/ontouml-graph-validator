"""OntoUML Rule Execution Module.

This module provides a collection of functions for executing various OntoUML validation rules.
It is designed to validate OntoUML models loaded as RDF graphs using a set of predefined rules.
The module currently contains implementations for multiple rules. Additional rules can be easily added in the future.
"""
from rdflib import Graph

from validator.validations.constants import ONTOUML_CLASS_STEREOTYPES
from validator.validations.result_issue import ResultIssue
from validator.validations.sparql_queries import QUERY_CL001, QUERY_CL002


def execute_rule_CL001(ontouml_model: Graph, rule_code: str) -> tuple[list[ResultIssue], list[ResultIssue]]:
    """Execute rule CL001 and return its description and results.

    :param ontouml_model: The OntoUML model in graph format (using the ontouml-vocabulary) to be validated by the rule.
    :type ontouml_model: Graph
    :param rule_code: Code of this rule.
    :type rule_code: str
    :return: A tuple with two components:
        - A list of all warnings (as a ResultIssue object) found during the specific rule's validation process.
        - A list of all errors (as a ResultIssue object) found during the specific rule's validation process.
    :rtype: tuple[list[ResultIssue], list[ResultIssue]]
    """
    rule_definition = "Every class must be decorated with exactly one stereotype."

    rule_w_list = []
    rule_e_list = []

    query_answer = ontouml_model.query(QUERY_CL001)

    for row in query_answer:
        class_id = row.class_id.toPython()
        class_name = row.class_name.value
        class_sts = row.num_sts.value

        if class_sts == 0:
            issue_description = f"Class '{class_name}' has no stereotype."
            issue = ResultIssue(rule_code, rule_definition, issue_description, [class_id])
            rule_w_list.append(issue)
        elif class_sts > 1:
            issue_description = f"Class '{class_name}' has more than one stereotype."
            issue = ResultIssue(rule_code, rule_definition, issue_description, [class_id])
            rule_e_list.append(issue)

    return rule_w_list, rule_e_list


def execute_rule_CL002(ontouml_model: Graph, rule_code: str) -> tuple[list[ResultIssue], list[ResultIssue]]:
    """Execute rule CL002 and return its description and results.

    :param ontouml_model: The OntoUML model in graph format (using the ontouml-vocabulary) to be validated by the rule.
    :type ontouml_model: Graph
    :param rule_code: Code of this rule.
    :type rule_code: str
    :return: A tuple with two components:
        - A list of all warnings (as a ResultIssue object) found during the specific rule's validation process.
        - A list of all errors (as a ResultIssue object) found during the specific rule's validation process.
    :rtype: tuple[list[ResultIssue], list[ResultIssue]]
    """
    rule_definition = "Every class must be decorated with stereotypes of the OntoUML profile."

    rule_w_list = []
    rule_e_list = []

    query_answer = ontouml_model.query(QUERY_CL002)

    for row in query_answer:
        class_id = row.class_id.toPython()
        class_name = row.class_name.value

        if row.class_st is None:
            issue_description = f"Class '{class_name}' has no stereotype."
            issue = ResultIssue(rule_code, rule_definition, issue_description, [class_id])
            rule_w_list.append(issue)
        else:
            class_st = row.class_st.toPython()
            if class_st not in ONTOUML_CLASS_STEREOTYPES:
                issue_description = (
                    f"Class '{class_name}' has stereotype '{class_st}' " f"that is not part of the OntoUML profile."
                )
                issue = ResultIssue(rule_code, rule_definition, issue_description, [class_id])
                rule_e_list.append(issue)

    return rule_w_list, rule_e_list
