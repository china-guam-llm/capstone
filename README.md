# capstone

I made the python files in this repository to interact with openAI's ChatGPT api to automate the data gathering process for the project. I will briefly explain the workflow below:

1. make a folder called "credentials" and put your openAI and Google Cloud tokens there
2. input.csv has the questions that will be queried to ChatGPT
3. if you have a lot of questions, inputCSVformatter.py splits up your questions evenly into many files so you don't waste money on tokens if something crashes halfway through
4. queryer_async.py will take the questions from input.csv and query them asynchronously, returning a .json file
3a. edit the GPT model and Chinese translation variants inside the python file as necessary, as well as the total number of times to repeat each query. It is set to 10 currently
5. pass the .json files through json_stitcher.py, if you have more than one
6. json_counter.py/csv_counter.py checks to see if any got duplicated or lost
7. jsonToCSVformatter.py needs to be run to convert the json file to a csv file for the embeddings
8. csv_number_correlator.py cleans up the csv file and numbers the rows instead of repeating the original question each time, which simplifies the embeddings graph later on
9. now, with the cleaned up csv file, pass it through queryer_async.py to get the embeddings
10. pass the returned csv file to either umapper_2D.py or umapper3D.py to make an interactive html graph.
