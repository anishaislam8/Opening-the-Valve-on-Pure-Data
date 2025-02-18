# Data Analysis and Results

We can access our database and run SQL queries directly to analyze our data. Run `python3 data_analysis.py` to generate the figures used in the paper and get the distribution of authors, PD files, revisions of the PD files, nodes and edges, and commits.

Similarly, we can answer our research questions by finding differences in the number of nodes and edges between each commit and their content parents by running `./calculate_differences.sh`. This script will create a file called *differences_final.csv* which we can use to answer our research questions. 

Additionally, we can run `python3 rq_analysis.py` to generate the values of our results section.