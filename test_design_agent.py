from agents.design_agent import DesignAgent

if __name__ == "__main__":
    agent = DesignAgent()
    result = agent.run("aspirin")  # Replace "aspirin" with any compound name you want to test
    from pprint import pprint
    pprint(result)