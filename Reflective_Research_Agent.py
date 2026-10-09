from dotenv import load_dotenv
import aisuite as ai


#This code requires an OPENAI_API_KEY in a .env file 
load_dotenv()

CLIENT = ai.Client()

def generate_draft(topic: str, model: str = "openai:gpt-4o") -> str: 
    
    #PreProcess Promt. change this to alter the LLM's goals
    prompt = f"You are an expert reporter. Write a one page essay on {topic}"
    
    # Get a response from the LLM by creating a chat with the client.
    response = CLIENT.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=1.0,
    )
    
    return response.choices[0].message.content

def reflect_on_draft(draft: str, model: str = "openai:o4-mini") -> str:

    # Define how we want the LLM to reflect on it's work.
    prompt = f"""You are an essay reviewer. 
    review the essay for questionable claims and professional tone.
    Also ensure that there are no unintended readings such as sexual inuendos,
    or culturally insensitive wording.
    
    Provide a list of possible improvments for the auther in the following format:
    Severity:() Issue:() Proposed Fix: 
    
    Review this essay: {draft}"""

    # Get a response from the LLM by creating a chat with the client.
    response = CLIENT.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=1.0,
    )

    return response.choices[0].message.content

def revise_draft(original_draft: str, reflection: str, model: str = "openai:gpt-4o") -> str:


    # Prompt the LLM to rewrite the essay with the new information
    prompt = f"""You are an Essay writter.
        You have written this essay:{original_draft}
        A reviewer has sent it back with the following comments:{reflection}
        Rewrite the essay taking the reviewer's comments into consideration"""

    # Get a response from the LLM by creating a chat with the client.
    response = CLIENT.chat.completions.create(
        model = model,
        messages = [{"role": "user","content":prompt}],
        temperature=1.0,
    )

    return response.choices[0].message.content

#Finally lets run the whole thing an see how it works
essay_prompt = "Should social media platforms be regulated by the government?"

# Agent 1 – Draft
draft = generate_draft(essay_prompt)
print("📝 Draft:\n")
print(draft)

# Agent 2 – Reflection
feedback = reflect_on_draft(draft)
print("\n🧠 Feedback:\n")
print(feedback)

# Agent 3 – Revision
revised = revise_draft(draft, feedback)
print("\n✍️ Revised:\n")
print(revised)