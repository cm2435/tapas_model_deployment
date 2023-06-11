import concurrent.futures
import requests

# Specify the endpoint URL for the deployed tapas model on us-east-2 with name table-qa-001
endpoint_url = "https://runtime.sagemaker.us-east-2.amazonaws.com/endpoints/table-qa-001/invocations"

# Specify the initial number of concurrent invocations
initial_concurrent_invocations = 1

# Specify the increment in concurrent invocations
concurrent_invocations_increment = 1

# Specify the number of total invocations
num_total_invocations = 100

# Function to send inference request to the endpoint
def send_inference_request():
    json_payload = {"questions": ["which actor has the last name Pitt"],"table": {"Actors": ["Brad Pitt", "Leonardo Di Caprio", "George Clooney"], "Number of movies": ["87", "53", "69"]}}
    response = requests.post(endpoint_url, json=json_payload)
    return response.status_code

# Perform load testing
concurrent_invocations = initial_concurrent_invocations
failed = False

while not failed and concurrent_invocations <= num_total_invocations:
    print(f"Testing with {concurrent_invocations} concurrent invocations...")
    
    # Load testing
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrent_invocations) as executor:
        # Submit concurrent inference requests
        futures = [executor.submit(send_inference_request) for _ in range(num_total_invocations)]

        # Wait for all invocations to complete
        concurrent.futures.wait(futures)
        
        # Check if any inference request failed
        for future in futures:
            if future.result() != 200:
                failed = True
                break

    concurrent_invocations += concurrent_invocations_increment

# Print the maximum number of concurrent invocations before failure
max_concurrent_invocations = concurrent_invocations - concurrent_invocations_increment
print(f"Endpoint started failing at {max_concurrent_invocations} concurrent invocations.")
