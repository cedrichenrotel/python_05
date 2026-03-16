#!/usr/bin/env python3

# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  nexus_pipeline.py                                 :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: cehenrot <cehenrot@student.42.fr>         +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/16 07:33:05 by cehenrot        #+#    #+#               #
#  Updated: 2026/03/16 15:15:26 by cehenrot        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from abc import ABC, abstractmethod
from typing import Any, List, Union, Protocol, runtime_checkable
import json
import csv

#contre maitre
@runtime_checkable
class ProcessingStage(Protocol):
    def process(self, data: Any) -> Any:
        pass


class ProcessingPipeline(ABC):

    def __init__(self, pipeline_id: str) -> None:
        self.pipeline_id = pipeline_id          # nom json, csv...
        self.stages: List[ProcessingStage] = []  # liste[]contenenant les stages

    def add_stage(self, stage: ProcessingStage) -> None:
        self.stages.append(stage)                 # ajoute un stage(processing stage)

    def run_pipeline(self, data: Any) -> Any: # permet de passer une str, dict, listdans le stage
        for i in self.stages:
            data = i.process(data)
        return data

    @abstractmethod
    def process(self, data: Any):
        pass


class InputStage():

    def process(self, data: Any) -> Any:
        try:
            rst = data.strip()# permet supprimer esc debut et fin de str
            return rst
        except TypeError as e:
            print(f"InputStage {e}")
            return


class TransformStage():
    def process(self, data: Any) -> Any:
        try:
            rst = data.capitalize()# permet de mettre une maj au debut de la str
            return rst
        except TypeError as e:
            print(f"TransformStage {e}")
            return


class OutputStage():
    def process(self, data: Any) -> Any:
        try:
            rst = "[Output]" + data
            return rst
        except TypeError as e:
            print(f"OutputStage {e}")
            return


class JSONAdapter(ProcessingPipeline):
    def __init__(self, pipeline_id: str) -> None: #initialise stage et pipelin_id
        super().__init__(pipeline_id)
        self.add_stage(InputStage()) # ajout stage ouvrier
        self.add_stage(TransformStage())
        self.add_stage(OutputStage())

    def process(self, data: str) -> Any:
        rst = json.loads(data)
        return self.run_pipeline(rst)


class CSVAdapter(ProcessingPipeline):
    def __init__(self, pipeline_id: str) -> None: #initialise stage et pipelin_id
        super().__init__(pipeline_id)
        self.add_stage(InputStage()) # ajout stage ouvrier
        self.add_stage(TransformStage())
        self.add_stage(OutputStage())
    
    def process(self, data: str) -> Any:
        rst = data.split(',')
        return self.run_pipeline(rst)
    

class StreamAdapter(ProcessingPipeline):
    def __init__(self, pipeline_id: str) -> None: #initialise stage et pipelin_id
        super().__init__(pipeline_id)
        self.add_stage(InputStage()) # ajout stage ouvrier
        self.add_stage(TransformStage())
        self.add_stage(OutputStage())

    def process(self, data: str) -> Any:
        return self.run_pipeline(data)   
    

class NexusManager:
    def __init__(self) -> None: # stock les adapters
        self.pipeline: List[ProcessingPipeline] = []

    def add_pipeline(self, pipeline: ProcessingPipeline) -> None:
        self.pipeline.append(pipeline)

    def run_all(self, data: Any) -> None:
        for pipe in self.pipeline:
            result = pipe.process(data)
            print(f"Pipeline {pipe.pipeline_id} result: {result}")


def main():
    print("=== CODE NEXUS - ENTERPRISE PIPELINE SYSTEM ===")
    print("\nInitializing Nexus Manager...")
    manager = NexusManager()

    json_pipe = JSONAdapter("JSON_READER")
    csv_pipe = CSVAdapter("CSV_READER")
    stream_pipe = StreamAdapter("REALSME_STREAM")
    
    manager.add_pipeline(json_pipe)
    manager.add_pipeline(csv_pipe)
    manager.add_pipeline(stream_pipe)

    print("\nProcessing JSON data through pipeline...")
    json_data = '{"value": "  nexus core  "}'
    print(f"Input: {json_data}")
    print(f"Result: {json_pipe.process(json_data)}")


if __name__ == "__main__":
    main()
