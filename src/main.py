from data_loader import load_data
from agent import run_agent


FILE_PATH = "data/sales_data.csv"


def main():

    df = load_data(FILE_PATH)

    print("\n===== AI BUSINESS DATA ANALYST =====")
    print("Ask questions about your business data.")
    print("Type 'exit' to stop.\n")

    while True:

        question = input("You: ")

        if question.lower() == "exit":
            break

        answer = run_agent(df, question)

        print("\nAI:", answer)
        print()


if __name__ == "__main__":
    main()