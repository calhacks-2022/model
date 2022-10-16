import cohere 

EXAMPLES = {
    'summarize': "Summarize this question:\nUser: What is the best library that I can install and use for making UI components in React?\nTLDR: Best React UI component library\n--\nSummarize this question:\nUser: What is the best library that I can install and use for making API requests in React?\nTLDR: Best React API request library\n--\nSummarize this question:\nUser: I want to install and parse XML to JSON in my React project for school\nTLDR: Best React XML to JSON library\n--\nSummarize this question:\nUser: I want to make an animated button in React\nTLDR: Best React animated button library\n--\nSummarize this question:\nUser: Graph\nTLDR: Best React graph library\n--\nSummarize this question:\nUser: File upload\nTLDR: Best React File upload library\n--\nSummarize this question: \nUser:",
    'expand': "Expand this question:\nUser: UI Components\nTLDR: Best React UI component library\n--\nExpand this question:\nUser: API request\nTLDR: Best React API request library\n--\nExpand this question:\nUser: ]XML to JSON\nTLDR: Best React XML to JSON library\n--\nExpand this question:\nUser: animated button\nTLDR: Best React animated button library\n--\nExpand this question:\nUser: Graph\nTLDR: Best React graph library\n--\nExpand this question:\nUser: File upload\nTLDR: Best React File upload library\n--\nExpand this question:\nUser:",
    'vary': "", 
}

def user_prompt(api_key, user_input, use_case="summarize"):
    if use_case not in EXAMPLES:
        print("Error")
        return
    co = cohere.Client(api_key) 
    response = co.generate( 
        model='large', 
        prompt=f'{EXAMPLES[use_case]}{user_input}', 
        max_tokens=100, 
        temperature=0.8, 
        k=0, 
        p=1, 
        frequency_penalty=0, 
        presence_penalty=0, 
        stop_sequences=["--"], 
        return_likelihoods='NONE'
    ) 
    return response.generations[0].text

my_api = "9HCYapYYWPUqjbgkm82BhFQIirVeIqDOa23LRdHw"
my_question = "I want to include a "
user_response = user_prompt(my_api, my_question, "summarize")
print('Prediction: {}'.format(user_response))
