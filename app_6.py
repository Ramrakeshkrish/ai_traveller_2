import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import CommaSeparatedListOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI

# Read API Key (Ensure the file is a .txt file, not .rtf)
try:
    with open('/Users/jrudram/Downloads/API_KEY.rtf', 'r') as f:
        GOOGLE_API_KEY = f.read().strip()
    print("✅ API Key Loaded Successfully")
except Exception as e:
    print("❌ Error loading API Key:", e)
# Initialize Google GenAI Chat Model
chat_model = ChatGoogleGenerativeAI(api_key=GOOGLE_API_KEY, model="gemini-2.0-flash-exp")

# Output Parser
outp = CommaSeparatedListOutputParser()

# Define the Chat Prompt Template
prompt_template = ChatPromptTemplate(
    messages=[
        ("system", """You are an AI-powered travel assistant.
You help users find the best travel options between a source and a destination.
Provide options for cab, train, bus, and flights with estimated costs.
Output Format Instructions:
{output_format_instructions}
"""),
        ("human", "Find the best travel options from {source} to {destination}.")
    ],
    partial_variables={"output_format_instructions": outp.get_format_instructions()}
)

# Define the chain
chain = prompt_template | chat_model  # Removed `| outp`

# Streamlit UI
st.title("AI-Powered Travel Planner")
st.write("Enter your travel details to get the best travel options.")

# User Inputs
source_input = st.text_input("Enter Source Location:")
destination_input = st.text_input("Enter Destination Location:")

btn_click = st.button("Find Travel Options")

if btn_click:
    if source_input and destination_input:
        # Create a dictionary with user inputs
        user_inputs = {"source": source_input, "destination": destination_input}

        # Invoke the AI model through LangChain pipeline
        response = chain.invoke(user_inputs)
        print(response)
        # Apply output parser
        parsed_response = outp.parse(response.content)

        # Display the response
        st.subheader("Recommended Travel Options")
        st.write(parsed_response)  # Output from AI model after parsing
    else:
        st.warning("Please enter both source and destination.")