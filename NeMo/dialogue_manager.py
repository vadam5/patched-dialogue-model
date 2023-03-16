# Copyright (c) 2021, NVIDIA CORPORATION.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import random
import time

import tqdm

def nop(it, *a, **k):
    return it

tqdm.tqdm = nop

import torch
import torch.multiprocessing as mp
from apex.transformer import parallel_state
from omegaconf import OmegaConf
from omegaconf.omegaconf import open_dict
from pytorch_lightning.trainer.trainer import Trainer

from nemo.collections.nlp.models.language_modeling.megatron_gpt_prompt_learning_model import (
    MegatronGPTPromptLearningModel,
)
from nemo.collections.nlp.modules.common.transformer.text_generation import LengthParam, SamplingParam
from nemo.collections.nlp.parts.nlp_overrides import NLPDDPStrategy
from nemo.core.config import hydra_runner

import logging

logging.disable("WARNING")

mp.set_start_method("spawn", force=True)

@hydra_runner(config_path="conf", config_name="dialogue_system.yaml")
def main(cfg) -> None:
    if not torch.cuda.is_available():
        raise EnvironmentError("GPU is needed for the inference")

    # trainer required for restoring model parallel models
    trainer = Trainer(strategy=NLPDDPStrategy(), **cfg.trainer)
    assert (
        cfg.trainer.devices * cfg.trainer.num_nodes
        == cfg.tensor_model_parallel_size * cfg.pipeline_model_parallel_size
    ), "devices * num_nodes should equal tensor_model_parallel_size * pipeline_model_parallel_size"

    # Update frozen GPT model path if it is given in case it has changed
    prompt_learning_cfg = MegatronGPTPromptLearningModel.restore_from(
        cfg.virtual_prompt_model_file, trainer=trainer, return_config=True,
    )
    if cfg.get("gpt_model_file"):
        with open_dict(prompt_learning_cfg):
            prompt_learning_cfg.language_model_path = cfg.gpt_model_file

    # Load prompt tuned model, virtual_prompt_model_file must be provided in config
    # Now load prompt learning model with frozen gpt model base
    model = MegatronGPTPromptLearningModel.restore_from(
        restore_path=cfg.virtual_prompt_model_file, trainer=trainer, override_config_path=prompt_learning_cfg,
    )
    model.freeze()

    # Have to turn off activations_checkpoint_method for inference
    try:
        model.frozen_model.model.language_model.encoder.activations_checkpoint_method = None
    except AttributeError:
        pass

    # Check whether the DDP is initialized
    if parallel_state.is_unitialized():

        def placeholder():
            return

        if model.trainer.strategy.launcher is not None:
            model.trainer.strategy.launcher.launch(placeholder, trainer=model.trainer)
        model.trainer.strategy.setup_environment()

    length_params: LengthParam = {
        "max_length": cfg.inference.tokens_to_generate,
        "min_length": cfg.inference.min_tokens_to_generate,
    }

    sampling_params: SamplingParam = {
        "use_greedy": cfg.inference.greedy,
        "temperature": cfg.inference.temperature,
        "top_k": cfg.inference.top_k,
        "top_p": cfg.inference.top_p,
        "repetition_penalty": cfg.inference.repetition_penalty,
        "add_BOS": cfg.inference.add_BOS,
        "all_probs": cfg.inference.all_probs,
        "compute_logprob": cfg.inference.compute_logprob,
    }

    max_input_length = model.frozen_model.cfg.encoder_seq_length - length_params["max_length"]
    random.seed(time.time())
    intros = open("/NeMo/data/intros.json", "r").readlines()
    intros = [json.loads(intro)["intro"] for intro in intros]
    chat_history = ""
    turn_num = 0

    while True:
        if turn_num == 0:
            intro = random.choice(intros)
            intro = intro.strip()
            print("\n\n\nChatbot: " + intro)

            chat_history += "chatbot: " + intro + "\n"
            turn_num += 1

        elif turn_num < 3:
            user_input = input("User: ")
            if user_input == "STOP":
                break
            chat_history += "user: " + user_input.strip() + "\n"
            turn_input = [{"taskname": "general_dialogue", "input_seq": user_input}]

            output = model.generate(
                inputs=turn_input,
                length_params=length_params,
                sampling_params=sampling_params,
            )
            bot_response = output['sentences'][0].split("\nbot_response:")[-1]
            bot_repsonse = bot_response.strip()
            print("\nChatbot: " + bot_response)

            chat_history += "chatbot: " + bot_response + "\n"
            turn_num += 1

        else:
            summary_input = [{"taskname": "summarize", "dialogue": chat_history.replace("chatbot:", "chatbot::").replace("user:", "user::")}]
            summary_output = model.generate(
                inputs=summary_input,
                length_params=length_params,
                sampling_params=sampling_params,
            )
            summary = summary_output['sentences'][0].split("summary:")[-1].strip()

            user_input = input("User: ")
            if user_input == "STOP":
                break
            user_input_line = "user: " + user_input.strip() + "\nchatbot:"
            chat_history += user_input_line

            inputs = [{"taskname": "convo_w_history", "summary": summary, "follow_up": user_input_line}]
            output = model.generate(
                inputs=inputs,
                length_params=length_params,
                sampling_params=sampling_params,
            )
            bot_response = output['sentences'][0].split("\nchatbot:")[-1]
            bot_repsonse = bot_response.strip()
            print("\nChatbot: " + bot_response)

            chat_history += bot_repsonse + "\n"
            turn_num += 1

    print(chat_history)

if __name__ == '__main__':
    main()
