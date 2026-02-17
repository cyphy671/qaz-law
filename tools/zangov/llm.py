from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIResponsesModel
from marvin import Agent

lmstudio_provider = OpenAIProvider(base_url="http://localhost:1234/v1/")


gpt_oss_model = OpenAIResponsesModel(
    "openai/gpt-oss-20b",
    provider=lmstudio_provider
)


mark_downer = Agent(
    name="Mark Downer",
    description=(
        "Converts structured legal HTML documents into normalized "
        "GitHub Flavored Markdown while preserving the original text content."
    ),
    instructions="""Convert the provided HTML document into GitHub Flavored Markdown (GFM).
        
        Preserve the original text exactly.
        Maintain document hierarchy (titles, sections, articles, numbered points, notes).
        Remove HTML markup and layout artifacts.
        Normalize formatting for clean, consistent Markdown output.
        
        Output only Markdown.
        """,
    model=gpt_oss_model
)
