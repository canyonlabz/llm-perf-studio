import os
import sys
import json
import shutil
from datetime import datetime
from deepeval.test_case import LLMTestCase
from deepeval.dataset import EvaluationDataset
from deepeval.test_case import LLMTestCaseParams
from deepeval.metrics import GEval
from src.utils.event_logs import thread_safe_add_log

# ========================= Framework Node Functions =========================

def run_deepeval_analysis_node(shared_data, state_snapshot):
    """
    Execute DeepEval quality assessment analysis.
    Combines loading test cases and running evaluation.
    
    Args:
        shared_data: Thread-safe data structure
        state_snapshot: Copy of session state at execution time
        
    Returns:
        dict: Results structure with success status, file paths, and metadata
    """
    try:
        # Extract configuration from shared_data
        llm_responses_file = shared_data['deepeval_config']['llm_responses_file']
        selected_metrics = shared_data['deepeval_config']['selected_metrics']
        run_timestamp = shared_data['deepeval_config']['run_timestamp']
        
        # Load test cases from JMeter JSON output
        thread_safe_add_log(shared_data['logs'], 
                           f"📖 Loading test cases from: {os.path.basename(llm_responses_file)}", 
                           agent_name="DeepEvalAgent")
        
        test_cases = load_test_cases_from_jmeter_output(llm_responses_file)
        
        thread_safe_add_log(shared_data['logs'], 
                           f"✅ Loaded {len(test_cases)} test cases successfully.", 
                           agent_name="DeepEvalAgent")
        
        # Execute DeepEval assessment
        thread_safe_add_log(shared_data['logs'], 
                           "🔬 Starting DeepEval correctness assessment...", 
                           agent_name="DeepEvalAgent")
        
        execute_deepeval_assessment(test_cases, shared_data)
        
        thread_safe_add_log(shared_data['logs'], 
                           "✅ DeepEval assessment execution completed.", 
                           agent_name="DeepEvalAgent")
        
        # Handle file renaming with JMeter timestamp
        deepeval_output_file = rename_deepeval_output_with_timestamp(run_timestamp, shared_data)
        
        return {
            'success': True,
            'test_cases_count': len(test_cases),
            'deepeval_output_file': deepeval_output_file,
            'run_timestamp': run_timestamp,
            'selected_metrics': selected_metrics
        }
        
    except Exception as e:
        thread_safe_add_log(shared_data['logs'], 
                           f"❌ DeepEval analysis failed: {str(e)}", 
                           agent_name="DeepEvalAgent")
        return {
            'success': False,
            'error': str(e)
        }

def analyze_deepeval_results_node(shared_data, state_snapshot):
    """
    Analyze DeepEval results and prepare structured data for UI display.
    
    Args:
        shared_data: Thread-safe data structure containing execution results
        state_snapshot: Copy of session state at execution time
        
    Returns:
        dict: Structured analysis for UI components and report tabs
    """
    try:
        # Parse the renamed .latest_test_run.json file
        thread_safe_add_log(shared_data['logs'], 
                           "📊 Parsing DeepEval results for UI display...", 
                           agent_name="DeepEvalAgent")
        
        # Get the renamed file path from shared_data results
        run_timestamp = shared_data['deepeval_config']['run_timestamp']
        deepeval_results = parse_latest_test_run_file(run_timestamp)
        
        # Create comprehensive analysis structure for the 5 UI tabs
        analysis = create_comprehensive_analysis(deepeval_results, shared_data)
        
        thread_safe_add_log(shared_data['logs'], 
                           f"✅ Analysis complete: {analysis['metadata']['pass_count']}/{analysis['metadata']['total_questions']} passed ({analysis['metadata']['overall_pass_rate']:.1f}%)", 
                           agent_name="DeepEvalAgent")
        
        return analysis
        
    except Exception as e:
        thread_safe_add_log(shared_data['logs'], 
                           f"❌ DeepEval analysis failed: {str(e)}", 
                           agent_name="DeepEvalAgent")
        return {'error': str(e)}

# ========================= Supporting Utility Functions =========================

def load_test_cases_from_jmeter_output(json_file_path):
    """
    Load test cases from JMeter JSON output file.
    Refactored version of the original load_test_cases() function.
    """
    test_cases = []
    with open(json_file_path, 'r') as file:
        for line_num, line in enumerate(file, 1):
            try:
                data = json.loads(line.strip())  # Read one JSON object per line
                test_case = LLMTestCase(
                    input=data.get('prompt', 'MISSING_PROMPT'),
                    actual_output=data.get('llm_response', 'MISSING_RESPONSE').strip().upper(),
                    expected_output=data.get('correct_answer', 'MISSING_ANSWER').strip().upper()
                )
                test_cases.append(test_case)
            except json.JSONDecodeError as e:
                print(f"[ERROR]: Skipping invalid JSON on line {line_num}: {line.strip()}")
                print(f"Reason: {e}")
                continue
    return test_cases

def execute_deepeval_assessment(test_cases, shared_data):
    """
    Execute DeepEval assessment with G-Eval correctness metric.
    Refactored version of the original evaluate_responses() function.
    """
    # Define metrics for evaluation
    correctness_metric = GEval(
        name="Correctness",
        criteria="Determine if actual output matches expected output exactly.",
        evaluation_params=[LLMTestCaseParams.ACTUAL_OUTPUT, LLMTestCaseParams.EXPECTED_OUTPUT],
        strict_mode=True  # Enforce strict matching
    )
    
    # Create dataset and evaluate
    dataset = EvaluationDataset(test_cases=test_cases)
    
    # Show progress indicator
    thread_safe_add_log(shared_data['logs'], 
                       f"🔍 Evaluating {len(test_cases)} test cases with G-Eval correctness metric...", 
                       agent_name="DeepEvalAgent")
    
    # Evaluate the test cases using the correctness metric
    evaluation_result = dataset.evaluate([correctness_metric])
    
    thread_safe_add_log(shared_data['logs'], 
                       "✅ G-Eval assessment completed - results saved to .latest_test_run.json", 
                       agent_name="DeepEvalAgent")
    
    return evaluation_result

def rename_deepeval_output_with_timestamp(run_timestamp, shared_data):
    """
    Rename .latest_test_run.json with JMeter timestamp for correlation.
    """
    try:
        deepeval_dir = os.path.join("src", "tools", ".deepeval")
        original_file = os.path.join(deepeval_dir, ".latest_test_run.json")
        timestamped_file = os.path.join(deepeval_dir, f"{run_timestamp}_.latest_test_run.json")
        
        if os.path.exists(original_file):
            shutil.move(original_file, timestamped_file)
            thread_safe_add_log(shared_data['logs'], 
                               f"📁 Results file renamed to: {run_timestamp}_.latest_test_run.json", 
                               agent_name="DeepEvalAgent")
            return timestamped_file
        else:
            thread_safe_add_log(shared_data['logs'], 
                               "⚠️ Warning: .latest_test_run.json not found for renaming", 
                               agent_name="DeepEvalAgent")
            return None
            
    except Exception as e:
        thread_safe_add_log(shared_data['logs'], 
                           f"⚠️ File renaming error: {str(e)}", 
                           agent_name="DeepEvalAgent")
        return None

def parse_latest_test_run_file(run_timestamp):
    """
    Parse the timestamped DeepEval output file.
    """
    deepeval_dir = os.path.join("src", "tools", ".deepeval")
    timestamped_file = os.path.join(deepeval_dir, f"{run_timestamp}_.latest_test_run.json")
    
    if not os.path.exists(timestamped_file):
        # Fallback to original filename if timestamp version doesn't exist
        original_file = os.path.join(deepeval_dir, ".latest_test_run.json")
        if os.path.exists(original_file):
            timestamped_file = original_file
        else:
            raise FileNotFoundError(f"DeepEval results file not found: {timestamped_file}")
    
    with open(timestamped_file, 'r') as file:
        return json.load(file)

def create_comprehensive_analysis(deepeval_results, shared_data):
    """
    Create comprehensive analysis structure for the 5 UI tabs.
    """
    test_cases = deepeval_results.get('testCases', [])
    
    # Calculate basic statistics
    total_questions = len(test_cases)
    pass_count = sum(1 for case in test_cases if case.get('success', False))
    fail_count = total_questions - pass_count
    overall_pass_rate = (pass_count / total_questions * 100) if total_questions > 0 else 0
    
    # Extract scores for distribution analysis
    scores = []
    for case in test_cases:
        metrics_data = case.get('metricsData', [])
        if metrics_data:
            score = metrics_data[0].get('score', 0)
            scores.append(score)
    
    analysis = {
        # Tab 1: DeepEval Summary
        'summary': {
            'total_questions': total_questions,
            'pass_count': pass_count,
            'fail_count': fail_count,
            'overall_pass_rate': overall_pass_rate,
            'average_score': sum(scores) / len(scores) if scores else 0,
            'total_cost': deepeval_results.get('evaluationCost', 0),
            'total_duration': deepeval_results.get('runDuration', 0),
            'run_timestamp': shared_data['deepeval_config']['run_timestamp']
        },
        
        # Tab 2: Detailed Results Table
        'detailed_results': create_detailed_results_table(test_cases),
        
        # Tab 3: Score Distribution Chart
        'score_distribution': create_score_distribution_data(scores),
        
        # Tab 4: Quality Assessment Insights
        'quality_insights': create_quality_insights(test_cases, deepeval_results),
        
        # Tab 5: Individual Test Cases
        'individual_cases': create_individual_cases_data(test_cases),
        
        # Metadata for overall tracking
        'metadata': {
            'total_questions': total_questions,
            'pass_count': pass_count,
            'fail_count': fail_count,
            'overall_pass_rate': overall_pass_rate,
            'total_cost': deepeval_results.get('evaluationCost', 0),
            'total_duration': deepeval_results.get('runDuration', 0)
        }
    }
    
    return analysis

def create_detailed_results_table(test_cases):
    """Create data structure for detailed results table (Tab 2)."""
    results = []
    for i, case in enumerate(test_cases, 1):
        metrics_data = case.get('metricsData', [])
        score = metrics_data[0].get('score', 0) if metrics_data else 0
        reason = metrics_data[0].get('reason', 'No reason provided') if metrics_data else 'No reason provided'
        
        results.append({
            'question_number': i,
            'input_prompt': case.get('input', '')[:100] + '...' if len(case.get('input', '')) > 100 else case.get('input', ''),
            'expected_output': case.get('expectedOutput', ''),
            'actual_output': case.get('actualOutput', ''),
            'score': score,
            'success': case.get('success', False),
            'reasoning': reason[:200] + '...' if len(reason) > 200 else reason
        })
    return results

def create_score_distribution_data(scores):
    """Create data structure for score distribution chart (Tab 3)."""
    if not scores:
        return {'bins': [], 'counts': [], 'statistics': {}}
    
    # Create score bins
    bins = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
    counts = [0] * (len(bins) - 1)
    
    for score in scores:
        for i in range(len(bins) - 1):
            if bins[i] <= score < bins[i + 1] or (i == len(bins) - 2 and score == 1.0):
                counts[i] += 1
                break
    
    return {
        'bins': bins,
        'counts': counts,
        'statistics': {
            'mean': sum(scores) / len(scores),
            'min': min(scores),
            'max': max(scores),
            'std': calculate_std(scores)
        }
    }

def create_quality_insights(test_cases, deepeval_results):
    """Create insights for quality assessment (Tab 4)."""
    insights = {
        'performance_by_score': {
            'excellent': sum(1 for case in test_cases if get_case_score(case) >= 0.9),
            'good': sum(1 for case in test_cases if 0.7 <= get_case_score(case) < 0.9),
            'fair': sum(1 for case in test_cases if 0.5 <= get_case_score(case) < 0.7),
            'poor': sum(1 for case in test_cases if get_case_score(case) < 0.5)
        },
        'common_failure_patterns': analyze_failure_patterns(test_cases),
        'execution_metrics': {
            'total_cost': deepeval_results.get('evaluationCost', 0),
            'average_duration_per_case': deepeval_results.get('runDuration', 0) / len(test_cases) if test_cases else 0,
            'total_duration': deepeval_results.get('runDuration', 0)
        }
    }
    return insights

def create_individual_cases_data(test_cases):
    """Create detailed data for individual test cases (Tab 5)."""
    cases = []
    for i, case in enumerate(test_cases, 1):
        metrics_data = case.get('metricsData', [])
        cases.append({
            'case_number': i,
            'input': case.get('input', ''),
            'expected_output': case.get('expectedOutput', ''),
            'actual_output': case.get('actualOutput', ''),
            'success': case.get('success', False),
            'score': metrics_data[0].get('score', 0) if metrics_data else 0,
            'reasoning': metrics_data[0].get('reason', 'No reason provided') if metrics_data else 'No reason provided',
            'duration': case.get('runDuration', 0),
            'cost': case.get('evaluationCost', 0)
        })
    return cases

# ========================= Helper Functions =========================

def get_case_score(case):
    """Extract score from a test case."""
    metrics_data = case.get('metricsData', [])
    return metrics_data[0].get('score', 0) if metrics_data else 0

def analyze_failure_patterns(test_cases):
    """Analyze common patterns in failed test cases."""
    failed_cases = [case for case in test_cases if not case.get('success', False)]
    
    patterns = {
        'total_failures': len(failed_cases),
        'common_issues': ['Exact match requirement not met', 'Case sensitivity mismatch', 'Formatting differences'],
        'failure_rate': len(failed_cases) / len(test_cases) * 100 if test_cases else 0
    }
    return patterns

def calculate_std(values):
    """Calculate standard deviation."""
    if not values:
        return 0
    mean = sum(values) / len(values)
    variance = sum((x - mean) ** 2 for x in values) / len(values)
    return variance ** 0.5
