from agents.approval_agent import ApprovalAgent

if __name__ == "__main__":
    agent = ApprovalAgent()
    result = agent.run("aspirin")  # Replace "aspirin" with any candidate name you want to test
    from pprint import pprint
    pprint(result)
