## Speech Emotion Recognition
This repository contains our work on Speech emotion recognition.

### Prerequisites
Linux (preferable Ubuntu LTS). Python3.x 

### Installing dependencies 
Dependencies are listed below and in the `requirements.txt` file.

* h5py
* Keras
* scipy
* sklearn
* speechpy
* tensorflow
* tqdm

Install one of python package managers in your distro. If you install pip, then you can install the dependencies by running 
`pip3 install -r requirements.txt` 

If you prefer to accelerate keras training on GPU's you can install `tensorflow-gpu` by 
`pip3 install tensorflow-gpu`

### Details of the code
- `utilities.py` - Contains code to read the files, extract the features and create test and train data
- `train_model.py` - Code to train non DL models. The code has three models with below given model numbers
    - `1 - CNN`
    - `2 - LSTM`

### Executing the code
Run `python3 server.py` from the command line.
And try to connect server using port number 5000.
