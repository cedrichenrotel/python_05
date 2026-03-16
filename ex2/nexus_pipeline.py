#!/usr/bin/env python3

# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  nexus_pipeline.py                                 :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: cehenrot <cehenrot@student.42lyon.fr>     +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/16 07:33:05 by cehenrot        #+#    #+#               #
#  Updated: 2026/03/16 19:53:19 by cehenrot        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from abc import ABC, abstractmethod
from typing import Any, List, Protocol, runtime_checkable
import json


@runtime_checkable
class ProcessingStage(Protocol):
    def process(self, data: Any) -> Any:
        pass


class ProcessingPipeline(ABC):

    def __init__(self, pipeline_id: str) -> None:
        self.pipeline_id = pipeline_id
        self.stages: List[ProcessingStage] = []

    def add_stage(self, stage: ProcessingStage) -> None:
        self.stages.append(stage)

    def run_pipeline(self, data: Any) -> Any:
        for i in self.stages:
            data = i.process(data)
        return data

    @abstractmethod
    def process(self, data: Any):
        pass


class InputStage():

    def process(self, data: Any) -> Any:
        try:
            rst = str(data.strip())
            return rst
        except TypeError as e:
            print(f"[KO] InputStage {e}")
            return data


class TransformStage():
    def process(self, data: Any) -> Any:
        try:
            rst = data.capitalize()
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
    def __init__(self, pipeline_id: str) -> None:
        super().__init__(pipeline_id)
        self.add_stage(InputStage())
        self.add_stage(TransformStage())
        self.add_stage(OutputStage())

    def process(self, data: str) -> Any:
        try:
            rst = json.loads(data)
            rst = str(rst["value"])
            return self.run_pipeline(rst)
        except (TypeError, KeyError) as e:
            print(f"[KO] JSONAdapter: {e}")


class CSVAdapter(ProcessingPipeline):
    def __init__(self, pipeline_id: str) -> None:
        super().__init__(pipeline_id)
        self.add_stage(InputStage())
        self.add_stage(TransformStage())
        self.add_stage(OutputStage())

    def process(self, data: str) -> Any:
        try:
            items = data.split(',')
            result = []
            for i in items:
                result.append(self.run_pipeline(i))
            return result
        except AttributeError as e:
            print(f"[KO] CSVAdapter: {e}")


class StreamAdapter(ProcessingPipeline):
    def __init__(self, pipeline_id: str) -> None:
        super().__init__(pipeline_id)
        self.add_stage(InputStage())
        self.add_stage(TransformStage())
        self.add_stage(OutputStage())

    def process(self, data: str) -> Any:
        return self.run_pipeline(data)


class NexusManager:
    def __init__(self) -> None:
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
    json_data = '{"sensor": "temp", "value": "trois", "unit": "C"}'
    print(f"Input: {json_data}")
    print(f"Result: {json_pipe.process(json_data)}")

    print("\nProcessing CSV data through same pipeline...")
    csv_data = "user,action,timestamp"
    print(f'Input: "{csv_data}"')
    print(f"result: {csv_pipe.process(csv_data)}")
    print("\nAll systems operational.")


if __name__ == "__main__":
    main()
