from agents.validation_agent import ValidationAgent

if __name__ == "__main__":
    agent = ValidationAgent()
    result = agent.run("aspirin")  # Replace "aspirin" with any candidate name you want to test
    from pprint import pprint
    pprint(result)
