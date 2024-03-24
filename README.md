automatic 100% local etsy digital download painting generator (new products coming soon)
powered by ollama - just use chrome extension singlefile to download a best selling digital download product(painting) and the code will do the rest

TUTORIAL FOR INSTALLING AND RUNNING AUTOETSY V1.0
https://drive.google.com/file/d/1MJn0CRJgOBGdNZY_JAmEIPYJACARjj-R/view?usp=sharing
Google Docs
chrome_qaanSqd3Uh.mp4
Pre-install Requirements: https://chromewebstore.google.com/detail/singlefile/mpiodijhokgodhhofbcjdecpffjipkle - SingleFile Chrome Extension
https://www.anaconda.com/ - Anaconda Installed
https://ollama.com/ - Ollama local models
https://git-scm.com/downloads - git

Run in console/terminal after ollama is installed
Ollama pull mistral-openorca
Ollama pull orca-mini
Ollama pull llava

AUTOETSY
https://github.com/matthewczeg/autoetsy
git clone the repo
cd autoetsy
conda create -n etsy python==3.10
conda activate etsy
pip install -r requirements.txt

python watcher.py to start (only after fooocusapi is working and pointing to the correct output folder - focusgen)


FOOOCUS API:
https://github.com/matthewczeg/autoetsy
After git cloning fooocus-api
CD Into it -> cd fooocus-api
THEN
git checkout v0.3.30-20-g0fbb004
THEN
conda env create -f environment.yaml
conda activate fooocus-api 

pip install -r requirements.txt 

python main.py

You will need to conda activate fooocus-api each time you want to run main.py in the fooocus-api folder to start the image gen server

Remember to change the config.txt in fooocus-api folder to point to the focusgen folder inside autoetsy