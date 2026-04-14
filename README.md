# end-to-end-medical-chatbot

Clone the repository

```bash
Project repo: https://github.com/
```

### STEP 01- Create a conda environment

```bash
conda create -n llmapp python=3.8 -y
```

```bash
conda activate llmapp
```

### STEP 02- install the requirements
```bash
pip install -r requirements.txt
```

### Create a `.env` file in the root directory and add your Pinecone & openai or gemini key as follows:

```ini
PINECONE_API_KEY="XXXXXXXXXXXXXXXXXXXXXXXX"
GEMINI_API_KEY="XXXXXXXXXXXXXXXXXXXXXX"
```

```bash
python store_index.py
````

```bash
#finally run the following command
python app.py
```

now,
```bash
open up localhost:
```