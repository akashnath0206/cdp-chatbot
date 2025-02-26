# Step 1: Load the index file
with open("index.txt", "r") as f:
    index = {}
    for line in f:
        question, doc_info = line.strip().split(" -> ")
        index[question] = doc_info

# Step 2: Load documentation from a file
def load_documentation(file_path):
    try:
        with open(file_path, "r") as f:
            return f.read()
    except FileNotFoundError:
        return None

# Step 3: Chatbot function
def chatbot():
    print("Welcome to the CDP Support Chatbot! Ask me 'how-to' questions about Segment, mParticle, Lytics, or Zeotap.")
    print("Type 'exit' or 'quit' to end the chat.")
    
    # List of CDP-related keywords to filter irrelevant questions
    cdp_keywords = [
        "segment", "mparticle", "lytics", "zeotap", 
        "source", "profile", "audience", "integrate", 
        "track", "event", "pipeline", "export", 
        "analyze", "data", "setup", "create", 
        "build", "configure", "manage", "sync", 
        "compare", "advanced"
    ]
    
    while True:
        # Ask the user for a question
        question = input("\nYou: ")
        
        # Exit the chatbot if the user types 'exit' or 'quit'
        if question.lower() in ["exit", "quit"]:
            print("Chatbot: Goodbye!")
            break
        
        # Step 4: Check for irrelevant questions
        if not any(keyword in question.lower() for keyword in cdp_keywords):
            print("Chatbot: Sorry, I can only answer questions related to Segment, mParticle, Lytics, and Zeotap.")
            continue
        
        # Step 5: Find the best match in the index
        matched = False
        for key in index:
            if key.lower() in question.lower():
                file_path, section = index[key].split(":")
                
                # Load the documentation file
                documentation = load_documentation(file_path)
                
                # Check if the file was found
                if documentation is None:
                    print(f"Chatbot: The documentation file '{file_path}' was not found.")
                    matched = True
                    break
                
                # Check if the section exists in the documentation
                if section in documentation:
                    print(f"Chatbot: Here's how to {key}:\n{documentation}")
                else:
                    print(f"Chatbot: The section '{section}' was not found in the documentation.")
                matched = True
                break
        
        # If no match is found, ask the user to rephrase
        if not matched:
            print("Chatbot: I couldn't find an answer to your question. Please try rephrasing.")

# Step 6: Run the chatbot
chatbot()