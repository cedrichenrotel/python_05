#!/usr/bin/env python3

# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  data_stream.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: cehenrot <cehenrot@student.42.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/12 11:26:07 by cehenrot        #+#    #+#               #
#  Updated: 2026/03/12 13:29:23 by cehenrot        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from abc import ABC, abstractmethod
from typing import Any, List, Dict, Union, Optional


class DataStream(ABC):

    def __init__(self, stream_id: str) -> None:
        self.stream_id = stream_id

    @abstractmethod
    def process_batch(self, data_batch: List[Any]) -> str:                  #traite liste
        pass

    def filter_data(self, data_batch: List[Any], criteria: Optional[str]    #filtre data
                    = None) -> List[Any]:
        pass

    def get_stats(self) -> Dict[str, Union[str, int, float]]:               #retourne les statistiques
        pass


class SensorStream(DataStream): #capteur de temperature

    def __init__(self, stream_id: str) -> None:


    def process_batch(self, data_batch: List[Any]) -> str:


    def filter_data(self, data_batch: List[Any], criteria: Optional[str]
                    = None) -> List[Any]:
        

    def get_stats(self) -> Dict[str, Union[str, int, float]]:



def main() -> None:

    print("=== CODE NEXUS - POLYMORPHIC STREAM SYSTEM ===")
    print("\nInitializing Sensor Stream...")

    stream_id = "SENSOR_001"
    capteur =["temp:22.5", "humidity:65", "pressure:1013"]
    proc = SensorStream(stream_id)

    print(proc.process_batch(capteur))