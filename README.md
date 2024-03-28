automatic 100% local etsy digital download painting generator (new products coming soon)
powered by ollama - just use chrome extension singlefile to download a best selling digital download product(painting) and the code will do the rest

TUTORIAL FOR INSTALLING AND RUNNING AUTOETSY V1.0


Pre-install Requirements: https://chromewebstore.google.com/detail/singlefile/mpiodijhokgodhhofbcjdecpffjipkle - SingleFile Chrome Extension
https://www.anaconda.com/ - Anaconda Installed
https://ollama.com/ - Ollama local models
https://git-scm.com/downloads - git

Run in console/terminal after ollama is installed
Ollama pull mistral-openorca
Ollama pull rhysjones/phi-2-orange
Ollama pull llava

AUTOETSY
https://github.com/matthewczeg/autoetsy
git clone the repo
cd autoetsy
conda create -n etsy python==3.10
conda activate etsy
pip install -r requirements.txt

AutoEtsy repo setup should be done if ollama is installed and models are pulled and you have created the conda environment, activated and installed the requirements file, now onto the foocusapi

FOOOCUS API:
https://github.com/matthewczeg/autoetsy
After git cloning fooocus-api
CD Into it -> cd fooocus-api
THEN
git checkout v0.3.30-20-g0fbb004
THEN
conda activate etsy 
(we'll use the same conda env for both etsy repo and focusapi repo)


pip install -r requirements.txt 
pip install torch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cu121

python main.py (run once then quit)

Open config.txt in fooocus-api folder to point the OUTPUT to the focusgen folder inside autoetsy
example: - "path_outputs": "C:\\code\\autoetsy\\focusgen" <- this will be different for you depending on where you git cloned your autoetsy folder and fooocus-api folder

Next install juggernaut V8 into by dragging and dropping the file into 
fooocus-api/repositories/fooocus/models/checkpoints/
Juggernaut download link: https://civitai.com/models/133005?modelVersionId=288982

Next install our LORA for oil paintings into
fooocus-api/repositories/fooocus/models/loras/
oil painting lora download link: https://civitai.com/models/84542/oil-paintingoil-brush-stroke

You will need to conda activate "etsy" or whichever name you used for our python 3.10 conda environment each time you want to run main.py in the fooocus-api folder to start the image generation server before starting main.py inside autoetsy


STARTUP INSTRUCTIONS:
Once all is working to start everything up each time:

open console or terminal and cd to the fooocus-api folder and run:
conda activate yourenvname
(or whichever conda env name you set)
python main.py 
(on mac it might be python3 main.py)

Then open another console or terminal and cd to autoetsy folder and run:
conda activate yourenvname
(or whichever conda env name you set)
python watcher.py and follow the instructions

To start generation, open etsy.com find a product you want to create similar version and click on the singlefile chrome extension
after you have download an product html file simply drag and drop it into the autoetsy/dump folder

(the product MUST be a digital download painting file and the MAIN product image must simply be a painting in a frame, no photo packs or other product variations will work with this code)

Your finished files will save inside the autoetsy/export folder

please report any issues!


