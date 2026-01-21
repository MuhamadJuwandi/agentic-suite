from typing import List, Optional, Dict, Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import spacy
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

# --- Global Initialization (Lazy Loading for Cold/Warm Starts) ---
print("Loading NLP Engine...")
from presidio_analyzer.nlp_engine import NlpEngineProvider

try:
    # Explicitly configure Presidio to use the small model (en_core_web_sm)
    # This prevents it from downloading the default large model (500MB+)
    configuration = {
        "nlp_engine_name": "spacy",
        "models": [{"lang_code": "en", "model_name": "en_core_web_sm"}],
    }

    # Create NLP engine based on configuration
    provider = NlpEngineProvider(nlp_configuration=configuration)
    nlp_engine = provider.create_engine()
    
    # Initialize Presidio Analyzer with the custom small engine
    analyzer = AnalyzerEngine(nlp_engine=nlp_engine, supported_languages=["en"])
    anonymizer = AnonymizerEngine()
    print("NLP Engine Ready (Small Model Loaded).")
except Exception as e:
    print(f"Critical Error: Failed to load NLP model. {e}")
    # We don't raise immediately to allow health check to pass, but logic will fail safely
    analyzer = None
    anonymizer = None

# --- API Schema Definitions (Input/Output Normalization) ---
class RedactRequest(BaseModel):
    text: str
    entities: Optional[List[str]] = None  # Specific entities to filter (e.g., ['PHONE_NUMBER'])
    mask_char: str = "*"
    anonymize: bool = True

class EntityResult(BaseModel):
    type: str
    start: int
    end: int
    score: float
    text: str  # Original text

class RedactResponse(BaseModel):
    original_length: int
    redacted_text: str
    entities_detected: List[EntityResult]
    metadata: Dict[str, Any]

# --- FastAPI Application Setup ---
app = FastAPI(
    title="ZeroCost PII Guard",
    description="Serverless PII Redaction API for AI Agent Infrastructure",
    version="1.0.0"
)

# --- Endpoints ---

@app.get("/health")
def health_check():
    """
    Simple health check to verify if the service is up and if the NLP engine loaded.
    Mapping to 'cold_start' status.
    """
    return {
        "status": "operational",
        "nlp_engine_loaded": analyzer is not None
    }

@app.post("/api/redact", response_model=RedactResponse)
async def redact_pii(request: RedactRequest):
    """
    Main endpoint for PII redaction.
    """
    if not analyzer:
         raise HTTPException(status_code=500, detail="Server Configuration Error: NLP Model Missing")
    
    if not request.text:
        return RedactResponse(
            original_length=0,
            redacted_text="",
            entities_detected=[],
            metadata={"status": "empty_input"}
        )

    # 1. ANALYSIS PHASE (Detection)
    # Presidio automatically uses Regex (for patterns) and SpaCy (for context)
    analysis_results = analyzer.analyze(
        text=request.text,
        entities=request.entities,
        language='en'
    )

    # 2. ANONYMIZATION PHASE (Redaction)
    final_text = request.text
    if request.anonymize:
        # Default operator: replace with empty string or specialized config
        operators = {
            "DEFAULT": OperatorConfig("replace", {"new_value": "<PII>"}) 
        }
        
        # If user requests specialized masking (e.g. My Phone is *****)
        if request.mask_char and len(request.mask_char) == 1:
            operators = {
                "DEFAULT": OperatorConfig("mask", {
                    "masking_char": request.mask_char,
                    "chars_to_mask": 100, # Mask entire detected entity
                    "from_end": True
                })
            }
            
        anonymized_result = anonymizer.anonymize(
            text=request.text,
            analyzer_results=analysis_results,
            operators=operators
        )
        final_text = anonymized_result.text

    # 3. RESPONSE NORMALIZATION
    # Convert raw results into standard JSON schema
    structured_entities = []
    for res in analysis_results:
        # Extract original text based on start/end indices
        entity_text = request.text[res.start:res.end]
        structured_entities.append(EntityResult(
            type=res.entity_type,
            start=res.start,
            end=res.end,
            score=round(res.score, 4),
            text=entity_text
        ))

    return RedactResponse(
        original_length=len(request.text),
        redacted_text=final_text,
        entities_detected=structured_entities,
        metadata={
            "engine": "presidio-lite",
            "model": "en_core_web_sm",
            "entity_count": len(structured_entities)
        }
    )
