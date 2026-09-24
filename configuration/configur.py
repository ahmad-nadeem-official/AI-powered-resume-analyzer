from pathlib import Path


temp = 0.1
llm = "openai/gpt-oss-120b"
max_tokens = None
reasoning_format="parsed"
rate_limiter=None
max_retries=3


########imahe error fixing##############
BASE_DIR = Path(__file__).resolve().parent.parent
image = BASE_DIR / "resources" / "logo" / "Gemini_Generated_Image_moo2wamoo2wamoo2-removebg-preview.png"
