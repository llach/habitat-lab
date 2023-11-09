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
    n_episodes = 1

    data_path = "/Users/llach/repos/home-robot/data"
    objects_path = join(data_path, "hssd-hab/objects/")
    a2a_dataset_path = join(data_path, "datasets/audio2action/")

    episodes_file_name = "audio2action_multi_ep_dataset.json"

    objects_decomposed_path = os.path.join(objects_path, "decomposed")
    additional_obj_config_paths = [
        os.path.join(objects_path, "openings"),
        *[join(objects_path,x) for x in os.listdir(objects_path) if len(x)==1],
        *[join(objects_decomposed_path,x) for x in os.listdir(objects_decomposed_path) if isdir(join(objects_decomposed_path, x))],
    ]

    cfg = get_config_defaults()
    # override_config = OmegaConf.load("examples/rearrange.yaml")
    override_config = OmegaConf.load("examples/audio2action.yaml")
    cfg = OmegaConf.merge(cfg, override_config)

    dataset = RearrangeDatasetV0()
    with RearrangeEpisodeGenerator(
        cfg=cfg,
        debug_visualization=vis,
        limit_scene_set=None,
    ) as ep_gen:
        print_metadata_mediator(ep_gen)

        for _ in range(n_episodes):
            dataset.episodes += ep_gen.generate_episodes(1, verbose)

        for ep in dataset.episodes:
            ep.additional_obj_config_paths = additional_obj_config_paths

        # save a local, readable copy for inspection
        with open(episodes_file_name, "w") as f:
            f.write(dataset.to_json())
        
        # dump the compressed file in the datasets folder
        with gzip.open(join(a2a_dataset_path, episodes_file_name+".gz"), "wt") as f:
                f.write(dataset.to_json())

    pass