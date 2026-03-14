#!/usr/bin/env python3

# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  data_stream.py                                    :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: cehenrot <cehenrot@student.42lyon.fr>     +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/03/12 11:26:07 by cehenrot        #+#    #+#               #
#  Updated: 2026/03/14 16:18:00 by cehenrot        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from abc import ABC, abstractmethod
from typing import Any, List, Dict, Union, Optional


class DataStream(ABC):

    def __init__(self, stream_id: str) -> None:
        self.stream_id = stream_id

    @abstractmethod
    def process_batch(self, data_batch: List[Any]) -> str:
        pass

    def filter_data(self, data_batch: List[Any], criteria: Optional[str]
                    = None) -> List[Any]:
        pass

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        pass


class SensorStream(DataStream):

    def __init__(self, stream_id: str) -> None:
        super().__init__(stream_id)
        self.type = "Environmental Data"
        self.temp = 0.0
        self.len_tab = 0
        self.lst_err: list[Any] = []

        print(f"Stream ID: {stream_id}, Type: {self.type}")

    def process_batch(self, data_batch: List[Any]) -> str:

        self.len_tab = len(data_batch)

        try:
            for i in data_batch:
                if isinstance(i, str) and ':' in i:
                    data = i.split(':')
                if data[0] == 'temp':
                    self.temp = float(data[1])
        except ValueError as e:
            print(f"Error process_batch : {e}")

        return (f"Sensor analysis: {self.len_tab} readings "
                f"processed, avg temp: {self.temp}°C")

    def filter_data(self, data_batch: List[Any], criteria: Optional[str]
                    = None) -> List[Any]:
        error = []
        limittemperature = float(criteria) if criteria else 100.0

        try:
            for i in data_batch:
                if isinstance(i, str) and ':' in i:
                    data = i.split(':')
                    if (data[0] == 'temp' and float(data[1]) >=
                            limittemperature):
                        error.append(i)
                        self.lst_err.append(i)
        except ValueError as e:
            print(f"Error filter_data: {e}")
        return error

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        return {
                "type": self.type,
                "temp": self.temp,
                "len_tab": self.len_tab,
                "number error": len(self.lst_err)
                }


class TransactionStream(DataStream):

    def __init__(self, stream_id: str) -> None:
        super().__init__(stream_id)
        self.type = "Financial Data"
        self.nb_sell = 0
        self.lst_err: list[Any] = []

        print(f"Stream ID: {stream_id}, Type: {self.type}")

    def process_batch(self, data_batch: List[Any]) -> str:

        total = 0

        try:
            for i in data_batch:
                if isinstance(i, str) and ':' in i:
                    data = i.split(':')
                    if data[0] == "buy":
                        total += int(data[1])
                    elif data[0] == "sell":
                        total -= int(data[1])
                        self.nb_sell += 1
        except ValueError as e:
            print(f"Error process_batch: {e}")

        if total > 0:
            sign = '+'
        else:
            sign = ''

        return (f"Transaction analysis: {len(data_batch)} operations, net "
                f"flow: {sign}{total} units")

    def filter_data(self, data_batch: List[Any], criteria: Optional[str]
                    = None) -> List[Any]:

        error = []
        accountneg = int(criteria) if criteria else 500

        for i in data_batch:
            try:
                if isinstance(i, str) and ':' in i:
                    data = i.split(':')
            except ValueError as e:
                print(f"Error filter_data: {e}")
            if data[0] == "buy" and int(data[1]) >= accountneg:
                error.append(i)
                self.lst_err.append(f"Flow Alert: {i}")
        return error

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        return {
                "type": self.type,
                "number error": len(self.lst_err)
                }


class EventStream(DataStream):

    def __init__(self, stream_id: str) -> None:
        super().__init__(stream_id)
        self.type = "System Events"
        self.lst_err: list[Any] = []
        self.len_tab = 0

        print(f"Stream ID: {stream_id}, Type: {self.type}")

    def process_batch(self, data_batch: List[Any]) -> str:

        total_err = 0
        self.len_tab = len(data_batch)

        try:
            for i in data_batch:
                if i == 'error':
                    total_err += 1
        except TypeError as e:
            print(f"Error process_batch: {e}")

        return (f"Event analysis: {self.len_tab} events, {total_err} error "
                "detected")

    def filter_data(self, data_batch: List[Any], criteria: Optional[str]
                    = None) -> List[Any]:

        rst = []
        target = criteria if criteria else "error"
        for i in data_batch:
            if i == target:
                rst.append(i)
            if i == "error":
                self.lst_err.append(target)
        return rst

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        return {
            "type": self.type,
            "len_tab": self.len_tab,
            "number error": len(self.lst_err)
                }


class StreamProcessor:

    def __init__(self) -> None:
        self.streams: List[DataStream] = []

    def add_stream(self, stream: DataStream) -> None:
        self.streams.append(stream)

    def process_all(self, all_payloads: List[List[Any]]) -> None:

        print("\nBatch 1 Results:")
        for i, stream in enumerate(self.streams):
            stream.process_batch(all_payloads[i])
            if isinstance(stream, SensorStream):
                name, unit, count = "Sensor", "readings", len(all_payloads[i])
            elif isinstance(stream, TransactionStream):
                name, unit, count = "Transaction", "operations",
                len(all_payloads[i])
            elif isinstance(stream, EventStream):
                name, unit, count = "Event", "events", len(all_payloads[i])
            print(f"- {name} data: {count} {unit} processed")


def main() -> None:
    print("=== CODE NEXUS - POLYMORPHIC STREAM SYSTEM ===")

    print("Initializing Sensor Stream...")
    sensor = SensorStream("SENSOR_001")
    print("Processing sensor batch: [temp:22.5, humidity:65, pressure:1013]")
    print(sensor.process_batch(["temp:22.5", "humidity:65", "pressure:1013"]))

    print("\nInitializing Transaction Stream...")
    transaction = TransactionStream("TRANS_001")
    print("Processing transaction batch: [buy:100, sell:150, buy:75]")
    print(transaction.process_batch(["buy:100", "sell:150", "buy:75"]))

    print("\nInitializing Event Stream...")
    event = EventStream("EVENT_001")
    print("Processing event batch: [login, error, logout]")
    print(event.process_batch(["login", "error", "logout"]))

    print("\n=== Polymorphic Stream Processing ===")
    print("Processing mixed stream types through unified interface...")

    processor = StreamProcessor()
    processor.add_stream(sensor)
    processor.add_stream(transaction)
    processor.add_stream(event)

    payloads = [
        ["temp:22.5", "temp:25.0"],
        ["buy:50", "sell:20", "buy:10", "buy:5"],
        ["login", "error", "logout"]
    ]

    StreamProcessor.process_all(payloads)

    print("\nStream filtering active: High-priority data only")
    false_sensor = sensor.filter_data(["temp:110", "temp:120"], "100")
    false_trans = transaction.filter_data(["buy:1000"], "500")
    print(f"Filtered results: {len(false_sensor)} critical sensor alerts, "
          f"{len(false_trans)} large transaction")

    print("\nAll streams processed successfully. Nexus throughput optimal.")


if __name__ == "__main__":
    main()
