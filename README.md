# patched-dialogue-model


1. On a machine with a GPU and docker installed, download the NVIDIA-NeMo docker container using the following command:
	`docker pull nvcr.io/nvidia/nemo:23.01`

2. Clone this project’s directory by running:
	`git clone git@github.com:vadam5/patched-dialogue-model.git`

3. Start the NeMo docker container with the NeMo directory in the patched-dialogue-model mounted as a volume by running
	`docker run --gpus all -it -v ~/patched-dialogue-model/NeMo:/NeMo --shm-size=8g -p 8888:8888 -p 6006:6006 --ulimit memlock=-1 --ulimit stack=67108864 --device=/dev/snd nvcr.io/nvidia/nemo:23.01`
	
4. From within the container, cd to the /NeMo directory
	`cd /NeMo`

5. Run the dialogue manager to chat with the dialogue system on command line
	`python dialogue_manager.py`

6. Type “STOP” when you are done chatting and a conversation log will print to the terminal.
