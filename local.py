# Sigh, I keep hitting the inference quota on HuggingFace.
# So here we go, let's run this locally with Ollama :)
import os
from smolagents import LiteLLMModel
# from smolagents.models import ChatMessage
from smolagents import Tool, CodeAgent
from smolagents import ToolCollection, CodeAgent
from mcp import StdioServerParameters

# Initialize the model
model = LiteLLMModel(
    model_id="ollama_chat/qwen2:7b",  # Or try other Ollama-supported models
    api_base="http://127.0.0.1:11434",  # Default Ollama local server
    num_ctx=8192,
)

# How do we create a tool??
# Apparoach 1: Make a class that inherits Tool
class SuperheroPartyThemeTool(Tool):
    name = "superhero_party_theme_generator"
    description = """
    This tool suggests creative superhero-themed party ideas based on a category.
    It returns a unique party theme idea."""

    inputs = {
        "category": {
            "type": "string",
            "description": "The type of superhero party (e.g., 'classic heroes', 'villain masquerade', 'futuristic Gotham').",
        }
    }

    output_type = "string"

    def forward(self, category: str):
        themes = {
            "classic heroes": "Justice League Gala: Guests come dressed as their favorite DC heroes with themed cocktails like 'The Kryptonite Punch'.",
            "villain masquerade": "Gotham Rogues' Ball: A mysterious masquerade where guests dress as classic Batman villains.",
            "futuristic Gotham": "Neo-Gotham Night: A cyberpunk-style party inspired by Batman Beyond, with neon decorations and futuristic gadgets."
        }

        return themes.get(category.lower(), "Themed party idea not found. Try 'classic heroes', 'villain masquerade', or 'futuristic Gotham'.")

# Approach 2: load agent tools from MCP
server_parameters = StdioServerParameters(
    command="uvx",
    args=["--quiet", "pubmedmcp@0.1.3"],
    env={"UV_PYTHON": "3.12", **os.environ},
)


def main():
    # Approach 1: use the tool directly 

    # party_theme_tool = SuperheroPartyThemeTool()
    # agent = CodeAgent(tools=[party_theme_tool], model=model)
    # result = agent.run(
    #     "What would be a good superhero party idea for a 'villain masquerade' theme?"
    # )
    # print(result)

    # Approach 2: use the pubmed MCP tool collection
    with ToolCollection.from_mcp(server_parameters, trust_remote_code=True) as tool_collection:
        agent = CodeAgent(tools=[*tool_collection.tools], model=model, add_base_tools=True)
        agent.run("Please find a remedy for hangover.")

if __name__ == "__main__":
    main()