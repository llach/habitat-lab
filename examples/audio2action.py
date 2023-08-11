#!/usr/bin/env python3

# Copyright (c) Meta Platforms, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.
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
    vis = True
    verbose = True
    n_episodes = 1

    cfg = get_config_defaults()
    override_config = OmegaConf.load("examples/rearrange.yaml")
    # override_config = OmegaConf.load("examples/audio2action.yaml")
    cfg = OmegaConf.merge(cfg, override_config)

    dataset = RearrangeDatasetV0()
    with RearrangeEpisodeGenerator(
        cfg=cfg,
        debug_visualization=vis,
        limit_scene_set=None,
    ) as ep_gen:
        print_metadata_mediator(ep_gen)

        # for _ in range(n_episodes):
        dataset.episodes += ep_gen.generate_episodes(1, verbose)
    pass