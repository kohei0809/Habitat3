import os
import random

import numpy as np
from gym import spaces
import gzip
import torch
import datetime
import multiprocessing

from matplotlib import pyplot as plt

from PIL import Image

from habitat_baselines.config.default import get_config  
from habitat.sims.habitat_simulator.habitat_simulator import HabitatSim
from habitat.datasets.maximum_info.maximuminfo_dataset import MaximumInfoDatasetV1
from habitat.datasets.maximum_info.maximuminfo_generator import generate_maximuminfo_episode
from habitat_baselines.common.environments import InfoRLEnv
from habitat_baselines.common.baseline_registry import baseline_registry
from utils.log_manager import LogManager
from utils.log_writer import LogWriter
from habitat.core.logging import logger        
       
def research_valid_z(scene_idx):
    exp_config = "./habitat_baselines/config/maximuminfo/ppo_maximuminfo.yaml"
    opts = None
    config = get_config(exp_config, opts)
    
    dir_path = "data/scene_datasets/mp3d"
    dirs = [f for f in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, f))]
    
    #scene_name = dirs[scene_idx]
    scene_name = "1LXtFkjw3qL"
    logger.info("START FOR: " + scene_name)
        
    dataset_path = "map_dataset/" + scene_name + ".json.gz"    
    
    config.defrost()
    config.TASK_CONFIG.SIMULATOR.SCENE = "data/scene_datasets/mp3d/" + scene_name + "/" + scene_name + ".glb"
    config.TASK_CONFIG.DATASET.DATA_PATH = dataset_path
    config.TASK_CONFIG.SIMULATOR.DEPTH_SENSOR.NORMALIZE_DEPTH = False
    config.TASK_CONFIG.SIMULATOR.DEPTH_SENSOR.MIN_DEPTH = 0.0
    config.TASK_CONFIG.SIMULATOR.DEPTH_SENSOR.MAX_DEPTH = 5.0
    config.TASK_CONFIG.SIMULATOR.AGENT_0.HEIGHT = 1.5
    config.TASK_CONFIG.SIMULATOR.AGENT_0.SENSORS = ["RGB_SENSOR", "DEPTH_SENSOR", "SEMANTIC_SENSOR"]
    config.TASK_CONFIG.SIMULATOR.SEMANTIC_SENSOR.HEIGHT = 256
    config.TASK_CONFIG.SIMULATOR.SEMANTIC_SENSOR.WIDTH = 256
    config.TASK_CONFIG.SIMULATOR.HABITAT_SIM_V0.PHYSICS_CONFIG_FILE = ("./data/default.phys_scene_config.json")
    config.TASK_CONFIG.TRAINER_NAME = "oracle-ego"
    config.TASK_CONFIG.DATASET.DATA_PATH = dataset_path
    config.freeze()
        
        
    #データセットに入れるz軸の候補を決める
    num = 1000000
    dataset = MaximumInfoDatasetV1()
    sim = HabitatSim(config=config.TASK_CONFIG.SIMULATOR)
    dataset.episodes += generate_maximuminfo_episode(sim=sim, num_episodes=num)         
        
    position_list = []
    num_list = []
    for i in range(len(dataset.episodes)):
        position = dataset.episodes[i].start_position[1]
            
        if position in position_list:
            idx = position_list.index(position)
            num_list[idx] += 1
        else:
            position_list.append(position)
            num_list.append(1)
                
    logger.info("LIST_SIZE: " + str(len(position_list)))
        
    #z軸が少数だったものは削除
    to_delete = []
    for i, n in enumerate(num_list):
        if n < (num/10):
            to_delete.append(i)
        
    for i in reversed(to_delete):
        num_list.pop(i)
        position_list.pop(i)
             
    logger.info("POSITION_LIST: " + str(len(position_list)))    
    for i in range(len(position_list)):
        logger.info(str(position_list[i])+ ", " + str(num_list[i]))
        
    z_list = position_list
             
                
if __name__ == '__main__':
    research_valid_z(scene_idx)
    
    logger.info("################# FINISH EXPERIMENT !!!!! ##########################")