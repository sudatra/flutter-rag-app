import google.generativeai as genai
from config import Settings

settings = Settings()

class LLMService:
  def __init__(self):
    genai.configure(api_key=settings.GEMINI_API_KEY)
    self.model = genai.GenerativeModel("gemini-2.0-flash-exp")

  def generate_response(self, query: str, search_results: list[dict]):
    context_text = "\n\n".join([
      f"Source {i + 1} ({result['url']}):\n{result['content']}"
      for i, result in enumerate(search_results)
    ])
    full_prompt = f"""
      Context from web search:
      {context_text}

      Query: {query}

      Please provide a comprehensive, detailed, well-cited, response using the above context. Think and reason deeply.
      Ensure you answer the query asked by the user. Do not use your own knowledge base to give the answer, unless it is absolutely necessary.
    """

    response = self.model.generate_content(full_prompt, stream=True)
    for chunk in response:
      yield chunk.text