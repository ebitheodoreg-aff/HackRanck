import csv
import os
from data_loader import load_deletion_requests
from compliance_engine import evaluate_request

def main():
    input_path = "dataset/deletion_requests.csv"
    if not os.path.exists(input_path):
        input_path = "deletion_requests.csv"
        
    output_path = "output.csv"

    print(f"Loading requests from {input_path}...")
    df = load_deletion_requests(input_path)

    results = []
    for _, row in df.iterrows():
        result = evaluate_request(row)
        results.append(result)

    fieldnames = [
        'request_id',
        'status',
        'exposed_identifiers',
        'active_recreation_processes',
        'remediation_steps'
    ]

    print(f"Writing evaluated results to {output_path}...")
    with open(output_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for res in results:
            writer.writerow(res)

    print("Deletion audit evaluation complete successfully!")

if __name__ == "__main__":
    main()