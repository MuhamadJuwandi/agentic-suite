import os
import json
from apify_client import ApifyClient
from api.index import analyzer, anonymizer, OperatorConfig, EntityResult

# Initialize Apify Client
# In local dev, tokens might be missing, so we handle that gracefully
try:
    client = ApifyClient()
except:
    client = None

def main():
    print("Starting SecureRedact Actor...")
    
    # 1. READ INPUT
    # Apify stores input in a specific JSON file or env var
    # We use a helper specific to the container environment
    if client:
        # Fetch input from Apify platform
        actor_input = client.key_value_store().get_record('INPUT')['value']
    else:
        # Fallback for local testing if env vars missing
        # Or read from local file
        actor_input = {"text": "Hello world (local test)", "anonymize": True}
        if os.path.exists("local_input.json"):
             with open("local_input.json") as f:
                 actor_input = json.load(f)

    if not actor_input or 'text' not in actor_input:
        print("ERROR: No text provided in input.")
        return

    text_to_process = actor_input.get('text', '')
    should_anonymize = actor_input.get('anonymize', True)
    mask_char = actor_input.get('mask_char', '*')
    
    if not text_to_process:
        print("Empty text provided.")
        return

    print(f"Processing text length: {len(text_to_process)}")

    # 2. CORE LOGIC (Imported from our existing api/index.py structure logic)
    # We reuse the global 'analyzer' and 'anonymizer' objects
    
    # Analysis
    analysis_results = analyzer.analyze(
        text=text_to_process,
        language='en'
    )

    # Anonymization
    final_text = text_to_process
    if should_anonymize:
        operators = {"DEFAULT": OperatorConfig("replace", {"new_value": "<PII>"})}
        
        if mask_char and len(mask_char) == 1:
            operators = {
                "DEFAULT": OperatorConfig("mask", {
                    "masking_char": mask_char,
                    "chars_to_mask": 100,
                    "from_end": True
                })
            }
            
        anonymized_result = anonymizer.anonymize(
            text=text_to_process,
            analyzer_results=analysis_results,
            operators=operators
        )
        final_text = anonymized_result.text

    # Normalization (Output Structure)
    structured_entities = []
    for res in analysis_results:
        entity_text = text_to_process[res.start:res.end]
        structured_entities.append({
            "type": res.entity_type,
            "start": res.start,
            "end": res.end,
            "score": round(res.score, 4),
            "text": entity_text
        })

    output_data = {
        "original_length": len(text_to_process),
        "redacted_text": final_text,
        "entities_detected": structured_entities,
        "is_success": True
    }

    # 3. PUSH OUTPUT
    if client:
        # Push to Apify Default Dataset
        client.dataset().push_items([output_data])
        # Also set as Output for quick view
        client.key_value_store().set_record('OUTPUT', output_data)
        print("Results saved to Apify Dataset.")
    else:
        print("Local Result:")
        print(json.dumps(output_data, indent=2))

    print("Actor finished successfully.")

if __name__ == '__main__':
    main()
