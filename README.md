# go_def_scoring

To run it, you need to:
- save the sheet with all the definitions in as ‘definitions.tsv’. I can add an input selection if you want, but this is easier
- In the same directory as the definitions, run docker run -it --rm -v `pwd`:/app afgreen/go-def-score
	that will pull down a pre-built docker which should all work. It will have the current working directory mounted in
- go to http://0.0.0.0:7860
- Select the right ontology from the dropdown near the bottom. The fields should auto populate
- Rate the entry, then click submit. The next one should auto populate
- When you’re done, type a filename into the 'Output Name’ bottom left and click the ‘Write’ button. You must use a .csv because I’m too lazy to detect intended filetype from what you write here
- The output is saved as a csv with three columns: The id which corresponds to the internal_id column on the original sheet, accuracy and confidence. There should be a header
- hit ctrl+c in the terminal to stop it


Caveats:
- Changing the ontology will reset your progress. I think it will still be saved, but you’ll have duplicate entries, which is not ideal
- I can’t actually test the container because it’s built for x86 and I’m on an M1. I think it should work, but I write this at 1am so who knows
- If it doesn’t work, you can do the following to install a python virtual environment:
-   I assume you have python, if not, install python 3.9 from brew `brew install python@3.9`
-   `curl -sSL https://install.python-poetry.org | python3 -` to install poetry
-   Clone this repo: `git clone https://github.com/afg1/go_def_scoring.git`
-   In the repo directory `poetry install` then `poetry run app.py`
  
