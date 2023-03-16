# patched-dialogue-model

## Final Application Run Steps

1. On a machine with a GPU and docker installed, download the NVIDIA-NeMo docker container using the following command:
	`docker pull nvcr.io/nvidia/nemo:23.01`

2. Clone this project’s directory by running:
	`git clone git@github.com:vadam5/patched-dialogue-model.git`

3. Download the base GPT-2 model from NVIDIA and place it in `~/patched-dialogue-model/NeMo/models` using the following command
	```	
	wget --content-disposition https://api.ngc.nvidia.com/v2/models/nvidia/nemo/megatron_gpt_345m/versions/1/zip -O megatron_gpt_345m_1.zip
	unzip megatron_gpt_345m_1.zip
	mv megatron_gpt_345m.nemo ~/patched-dialogue-model/NeMo/models
	```

4. Start the NeMo docker container with the NeMo directory in the patched-dialogue-model mounted as a volume by running
	`docker run --gpus all -it -v ~/patched-dialogue-model/NeMo:/NeMo --shm-size=8g -p 8888:8888 -p 6006:6006 --ulimit memlock=-1 --ulimit stack=67108864 --device=/dev/snd nvcr.io/nvidia/nemo:23.01`
	
5. From within the container, cd to the /NeMo directory
	`cd /NeMo`

6. Run the dialogue manager to chat with the dialogue system on command line
	`python dialogue_manager.py`

7. Type “STOP” when you are done chatting and a conversation log will print to the terminal.
