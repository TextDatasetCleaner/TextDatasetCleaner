import os
from typing import List

from textdatasetcleaner.exceptions import TDCOSError, TDCRuntimeError, TDCValueError
from textdatasetcleaner.helpers import get_temp_file_path
from textdatasetcleaner.processors import BaseProcessor, processors_dict


class Loader:
    def __init__(self, config: dict, input_file: str, output_file: str):
        self.config = config
        self.input_file = input_file
        self.output_file = output_file

        self.previous_temp_file = ''

    def file_processing(self, stage: str) -> None:
        # TODO: tqdm + logger
        for processor_name in self.config[stage]:
            processor = processors_dict[processor_name]()

            temp_file_path = get_temp_file_path(self.config)
            try:
                result = processor.process_file(self.input_file, temp_file_path)
            except OSError as exc:
                # TODO: logging
                os.remove(temp_file_path)
                raise TDCOSError(exc)

            if not result:
                raise TDCRuntimeError(f'After "{stage}" stage by "{processor_name}" processor result file is empty')

            # TODO: log lines count

            self._remove_previous_temp(temp_file_path)
            self.input_file = temp_file_path

    def line_processing(self) -> None:
        temp_file_path = get_temp_file_path(self.config)
        processors = self._get_line_processors()

        # TODO: codecs?
        with open(self.input_file, encoding='utf-8') as fdr:
            with open(temp_file_path, 'w', encoding='utf-8') as fdw:
                # TODO: tqdm + logger.debug
                for line in fdr:
                    if not line:
                        continue

                    for proc in processors:
                        line = proc.process_line(line)  # type: ignore
                        # TODO: log processed line
                        if not line:  # empty or is None
                            break

                    # save after all processors
                    if line:  # not empty and is not None
                        fdw.write(f'{line}\n')

        # TODO: check need remove old input_file
        self.input_file = temp_file_path

    def finish(self) -> None:
        # FIXME: find another way
        os.rename(self.input_file, self.output_file)

    def _remove_previous_temp(self, new_temp_file_path: str = '') -> None:
        if self.previous_temp_file:
            os.remove(self.previous_temp_file)

        if not new_temp_file_path:
            self.previous_temp_file = new_temp_file_path

    def _get_line_processors(self) -> List[BaseProcessor]:
        processors = []
        for processor_data in self.config['PROCESSING']:
            params = {}
            if isinstance(processor_data, dict):
                # HACK: processor with parameters for __init__
                processor_name = list(processor_data)[0]
                params = processor_data[processor_name]
            elif isinstance(processor_data, str):
                processor_name = processor_data
            else:
                # TODO: own exceptions
                raise TDCValueError(f'Wrong processor: {processor_data}')

            processor = processors_dict[processor_name](**params)
            processors.append(processor)

        return processors
