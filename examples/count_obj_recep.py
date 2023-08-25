#!/usr/bin/env python3

# Copyright (c) Meta Platforms, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import habitat

if __name__ == "__main__":
    # Note: Use with for the example testing, doesn't need to be like this on the README

    env = habitat.Env(
        config=habitat.get_config(
            "benchmark/rearrange/pick.yaml"
        )
    ) 

    def _update_count_dict(d, key):
        if key not in d: d.update({key: 0})
        d[key] += 1

    def clean_obj_name(on):
        return on.replace(".object_config.json", "").replace("_:0000", "")
    
    def _sync_dicts(d1, d2):

        # sort first dict
        sorted_idx_ro = np.argsort(list(d1.values()))
        d1 = dict(zip(
            np.array(list(d1.keys()))[sorted_idx_ro], 
            np.array(list(d1.values()))[sorted_idx_ro],)
        )

        # sort second dict based on sorted d1 keys
        to_idx = np.array([list(d2.keys()).index(to) for to in d1.keys()])
        d2 = dict(zip( 
            np.array(list(d2.keys()))[to_idx], 
            np.array(list(d2.values()))[to_idx],)
        )

        return d1, d2


    N = 1000
    rigid_objects  = {}
    target_objects = {}
    target_receptacles = {}
    goal_receptacles = {}

    for eps in env.episodes[:N]:
        for ro in eps.rigid_objs:
            _update_count_dict(rigid_objects, clean_obj_name(ro[0]))
        for tname, _ in eps.targets.items():
            _update_count_dict(target_objects, clean_obj_name(tname))
        for tr in eps.target_receptacles:
            _update_count_dict(target_receptacles, tr[0])
        for gr in eps.goal_receptacles:
            _update_count_dict(goal_receptacles, gr[0])
    
    import numpy as np
    import matplotlib.pyplot as plt

 
    ### objects
    # rigid_objects, target_objects = _sync_dicts(rigid_objects, target_objects)

    plt.figure(figsize=(9,7))
    plt.barh(list(rigid_objects.keys()), list(rigid_objects.values()), left=list(target_objects.values()), label="# occurrences")
    plt.barh(list(target_objects.keys()), list(target_objects.values()), label="# target")

    plt.legend(loc="lower right")
    plt.title(f"object occurrences in N={N} Rearrange episodes")
    plt.tight_layout()
    plt.show()
   
    ### receptacles
    target_receptacles, goal_receptacles = _sync_dicts(target_receptacles, goal_receptacles)

    plt.figure(figsize=(9,7))
    plt.barh(list(goal_receptacles.keys()), list(goal_receptacles.values()), label="#goal")
    plt.barh(list(target_receptacles.keys()), list(target_receptacles.values()), left=list(goal_receptacles.values()), label="#target")

    plt.legend()
    plt.title(f"receptacle occurrences in N={N} Rearrange episodes")

    plt.tight_layout()
    plt.show()