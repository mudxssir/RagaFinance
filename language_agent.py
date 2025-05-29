# agents/language_agent.py

from transformers import pipeline
import warnings
warnings.filterwarnings("ignore", category=UserWarning, message=".*resource_tracker.*")

class LanguageAgent:
    def __init__(self, model_name="gpt2"):
        self.generator = pipeline(
            "text-generation",
            model=model_name,
            device=-1  # CPU; set to 0 if you have GPU
        )

    def generate_summary(self, context: str, max_length: int = 150) -> str:
        outputs = self.generator(
            context,
            max_length=max_length,
            do_sample=True,
            top_p=0.95,
            top_k=50,
            num_return_sequences=1
        )
        return outputs[0]['generated_text']

# Quick local test
if __name__ == "__main__":
    agent = LanguageAgent()
    sample_context = (
        "The Asia tech sector today shows mixed results. TSMC beat earnings expectations by 4%, "
        "while Samsung missed by 2%. Regional sentiment remains cautious due to rising interest rates."
    )
    summary = agent.generate_summary(sample_context)
    print("Generated Summary:\n", summary)

agent = LanguageAgent()

def generate_narrative(context: str) -> str:
    return agent.generate_summary(context)
