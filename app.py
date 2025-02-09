import pprint
from flask import Flask,render_template,request
from create_db_hg import generate_data_store
from openai_processing import process_query
from scrape import clean_body_content, extract_body_content, scrape_website
from flask_cors import CORS  # Add this import

app=Flask(__name__)
CORS(app)

@app.route('/',methods=['GET','POST'])
def home():

    # Handle POST Request here

    pprint.pprint(request.get_json())

    # collect array of boston websites
    websites = request.get_json()['websites']
    clear_database = request.get_json()['clear_database']
    
    # call function to get the content of the websites
    with open(f'websites.txt', 'w') as f:
        for w in websites:
            dom_content = scrape_website(w)
            body_content = extract_body_content(dom_content)
            cleaned_content = clean_body_content(body_content)
            # write cleaned content to a file
            f.write(cleaned_content)
    
    # re write into md file
    with open(f'websites.txt', 'r') as f:
        cleaned_content = f.read()
        # write cleaned content to a file
        with open(f'data/websites.md', 'w') as f:
            f.write(cleaned_content)
            
    # generate data store

    generate_data_store(clear_database=clear_database)
        
    
    # break content into 
    return websites


@app.route('/query', methods=['GET', 'POST'])
def query():
    query_text = request.get_json()['query_text']
    response = process_query(query_text)
    print("response")
    print(response)
    if response.content:  
        return {"response": response.content}
    else:
        return {"response":response}

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    return render_template('index.html')

if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=5000,debug=True)