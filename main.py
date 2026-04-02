import os
import sys
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from call_functions import available_functions, call_function

load_dotenv()
if not os.environ.get("GEMINI_API_KEY"):
    raise ValueError("GEMINI_API_KEY environment variable is not set.")
else:
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

def main():
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    for _ in range(20):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(system_instruction=system_prompt, temperature=0, tools=[available_functions])
        )
        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)
        function_results = []
        if not response.function_calls is None:
            for function_call in response.function_calls:
                function_call_response = call_function(function_call, verbose=args.verbose)
                if len(function_call_response.parts) == 0:
                    raise Exception("Function call response does not contain any parts.")
                if function_call_response.parts[0].function_response is None:
                    raise Exception("Function call response part does not contain a function response.")
                if function_call_response.parts[0].function_response.response is None:
                    raise Exception("Function call response part does not contain a function response result.")
                function_results.append(function_call_response.parts[0])
                if args.verbose:
                    print(f"-> {function_call_response.parts[0].function_response.response}")
        else:
            print(response.text)
            break
        messages.append(types.Content(role="user", parts=function_results))
    else:
        print("Reached maximum number of iterations without a final response.")
        sys.exit(1)

if __name__ == "__main__":
    main()
