import os
import sys
import json
from deepeval.test_case import LLMTestCase
from deepeval.dataset import EvaluationDataset
from deepeval.test_case import LLMTestCaseParams
from deepeval.metrics import GEval

# Subfolder paths (relative to the script's location)
INPUT_FOLDER = "../../jmeter/test_results"
OUTPUT_FOLDER = "../../jmeter/test_results"

# Load test cases from the exported JSON file
def load_test_cases(json_file_path):
    test_cases = []
    with open(json_file_path, 'r') as file:
        for line in file:
            try:
                data = json.loads(line.strip())  # Read one JSON object per line
                test_case = LLMTestCase(
                    input=data.get('prompt', 'MISSING_PROMPT'),
                    actual_output=data.get('llm_response', 'MISSING_RESPONSE').strip().upper(),
                    expected_output=data.get('correct_answer', 'MISSING_ANSWER').strip().upper()
                )
                test_cases.append(test_case)
            except json.JSONDecodeError as e:
                print(f"[ERROR]: Skipping invalid JSON line: {line.strip()}")
                print(f"Reason: {e}")
    return test_cases

# Define metrics for evaluation
correctness_metric = GEval(
    name="Correctness",
    criteria="Determine if actual output matches expected output exactly.",
    evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT, LLMTestCaseParams.EXPECTED_OUTPUT],
    strict_mode=True  # Enforce strict matching
)

# Evaluate test cases 
def evaluate_responses(test_cases):
    dataset = EvaluationDataset(test_cases=test_cases)
    # Evaluate the test cases using the provided correctness_metric.
    evaluation_result = dataset.evaluate([correctness_metric])
    
    # Since evaluation_result is a Pydantic model, access test_results via dot notation.
    test_results = evaluation_result.test_results
    
    for test_result in test_results:
        # Debug: print the attributes of the test_result object
        #print("TestResult attributes:", dir(test_result))
        
        # Print test case details
        print(f"Input: {test_result.input}")
        print(f"Actual Output: {test_result.actual_output}")
        print(f"Expected Output: {test_result.expected_output}")
        
        # Iterate over metrics_data if available
        if test_result.metrics_data:
            for md in test_result.metrics_data:
                print(f"Score: {md.score}")
                print(f"Reason: {md.reason}\n")
        else:
            print("No metric scores returned.\n")

# Main execution
if __name__ == "__main__":
    # Ensure the input and output folders exist
    if not os.path.exists(INPUT_FOLDER):
        print(f"[ERROR]: Input folder '{INPUT_FOLDER}' does not exist.")
        sys.exit(1)
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
    
    # Check if a file path was provided as a command-line argument
    if len(sys.argv) < 2:
        print("Usage: python deepeval_assessment.py <LLM_RESPONSE_JSON_FILE>")
        file_name = input("Please enter the LLM Response JSON file name: ")
    else:
        file_name = sys.argv[1]
    
    # Validate if the file exists in the input folder
    json_file_path = os.path.join(INPUT_FOLDER, file_name)
    if not os.path.exists(json_file_path):
        print(f"[ERROR]: The file '{json_file_path}' does not exist. Please check the file name and try again.")
        sys.exit(1)
    
    print(f"[INFO]: Processing {file_name}...")

    # Load test cases from the JSON file
    test_cases = load_test_cases(json_file_path)
    evaluate_responses(test_cases)
