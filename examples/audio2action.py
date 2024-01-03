#!/usr/bin/env python3

# Copyright (c) Meta Platforms, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
import os
import gzip 

from os.path import join, isdir

from omegaconf import OmegaConf

from habitat.datasets.rearrange.rearrange_dataset import RearrangeDatasetV0
from habitat.datasets.rearrange.rearrange_generator import (
    RearrangeEpisodeGenerator,
)
from habitat.datasets.rearrange.run_episode_generator import (
    get_config_defaults,
    print_metadata_mediator
)

if __name__ == "__main__":
    vis = False
    verbose = False
    N_episodes = 2
    N_steps = 3

    a2a_dataset_path = "data/datasets/audio2action/"
    episodes_file_name = "audio2action_multi_ep_dataset_ovmm.json"
    os.makedirs(a2a_dataset_path, exist_ok=True)

    cfg = get_config_defaults()
    override_config = OmegaConf.load("examples/ovmm_train.yaml")
    cfg = OmegaConf.merge(cfg, override_config)

    cfg.object_target_samplers[0]["params"]["num_samples"] = [N_steps,N_steps]

    dataset = RearrangeDatasetV0()
    with RearrangeEpisodeGenerator(
        cfg=cfg,
        debug_visualization=vis,
        limit_scene_set=None,
    ) as ep_gen:
        print_metadata_mediator(ep_gen)

        while len(dataset.episodes) < N_episodes:
            try:
                ep = ep_gen.generate_episodes(1, verbose)
                dataset.episodes += ep
                print("##########################")
                print(f"#### GENERATED EPISODE {len(dataset.episodes)}")
                print("##########################")
            except AssertionError as e: # we just discard the episode and re-run generation
                 print(f"AssertionError: {e}\nCould not generate episode!")            

        # save a local, readable copy for debugging
        with open(episodes_file_name, "w") as f:
            f.write(dataset.to_json())
        
        # dump the compressed file in the datasets folder
        with gzip.open(join(a2a_dataset_path, episodes_file_name+".gz"), "wt") as f:
                f.write(dataset.to_json())