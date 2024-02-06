import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
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
       
def research_valid_z():
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
    config.TASK_CONFIG.SIMULATOR.AGENT_0.SENSORS = ["RGB_SENSOR", "DEPTH_SENSOR"]
    config.TASK_CONFIG.SIMULATOR.SEMANTIC_SENSOR.HEIGHT = 256
    config.TASK_CONFIG.SIMULATOR.SEMANTIC_SENSOR.WIDTH = 256
    #config.TASK_CONFIG.SIMULATOR.HABITAT_SIM_V0.PHYSICS_CONFIG_FILE = ("data/default.phys_scene_config.json")
    config.TASK_CONFIG.TRAINER_NAME = "oracle-ego"
    config.TASK_CONFIG.DATASET.DATA_PATH = dataset_path
    config.freeze()
        
        
    #データセットに入れるz軸の候補を決める
    num = 1000000
    dataset = MaximumInfoDatasetV1()
    sim = HabitatSim(config=config.TASK_CONFIG.SIMULATOR)
    dataset.episodes += generate_maximuminfo_episode(sim=sim, num_episodes=num)         
        
    logger.info("Create datasets")
    position_dict = {}
    for i in range(len(dataset.episodes)):
        position = dataset.episodes[i].start_position[1]
        
        num_pos = position_dict.get(position, 0)
        position_dict[position] = num_pos+1
                
    logger.info("LIST_SIZE: " + str(len(position_dict)))
        
    #z軸が少数だったものは削除
    sorted_positions = sorted(position_dict.items(), key=lambda x: x[1], reverse=True)

    # valueが1000以上の位置情報のみを抽出してリストに格納
    num_list = [(key, value) for key, value in sorted_positions if value >= 1000]

    # num_listに入れたkeyとそのvalueをprint
    logger.info(scene_name)
    for key, value in num_list:
        print(f"Position: {key}, Value: {value}")
        
    z_list = num_list
             
                
if __name__ == '__main__':
    research_valid_z()
    
    logger.info("################# FINISH EXPERIMENT !!!!! ##########################")