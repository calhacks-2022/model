import cohere
def get_recommendations(api_key, query):
    co = cohere.Client(api_key)
    response = co.generate(
    model='large',
    prompt='User: What is the best react library that I can install and use for making UI components in React?\nList:@mui/material \nantd \nreactstrap \n@coreui/react \nsemantic-ui-react\n--\n'
        +'User: What is the best library that I can install and use for making API requests in React?\nList:axios\n@types/superagent\nky\npopsicle\nstream-http\n--\n'
        +'User: I want to include some icons\nList:material-design-icons \nfontawesome \nionicons \nreact-native-icons \nocticons \n--\n'
        +'User: I want to install and parse XML to JSON in my React project for school\nList:xml2js \nxml2json \nsimple-xml-to-json \nfast-xml-parser\n@xmldom/xmldom\n--\n'
        +'User: animation components\nList: reactstrap \nreact-spring \nreact-move \nremotion\nframer-motion\n--\n'
        +'User: dropdown\nList:downshift\nreact-single-dropdown\nreact-select-search\nreact-dropdown-tree-select\nreact-multi-select-component\n--\n'
        +'User: data visualization\nList:react-chartjs-2\nrecharts\nvictory\n@visx/visx\nnivo\n--\n'
        +'User: countdown timer\nList:react-timer-component\nreact-timer\nreact-countdown\n--\n'
        +'User: '
        + query
        + '\nList:',
    max_tokens=100,
    temperature=0.8,
    k=0,
    p=1,
    frequency_penalty=0,
    presence_penalty=0,
    stop_sequences=["--"],
    return_likelihoods='NONE')
    return response.generations[0].text.split("\n")[:-1]

if __name__ == "__main__":
    my_api = '9HCYapYYWPUqjbgkm82BhFQIirVeIqDOa23LRdHw'
    my_query = 'drag and drop interface'
    print(get_recommendations(my_api, my_query))
