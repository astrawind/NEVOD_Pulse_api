
from src.utils import read_last_lines
from src.hv.v1.schemas import HVItem, HVChan
from src.hv.v1.config import settings
from datetime import date, datetime
from src.exceptions import CorruptedFile
import os

class HVHandler:
    
    def __init__(self, file_directory=settings.HV_DIRECTORY):
        if os.path.exists(file_directory):
            self.dir = file_directory
        else:
            raise CorruptedFile(f"directory {file_directory} is not found")

    def get_last_record(self, date) -> HVItem:
        try:
            hv_items_generator = read_last_lines(f'{self.dir}/hv{date.year}{date.month}{date.day}.log')
        except FileNotFoundError:
            return None
        line = next(hv_items_generator)
        if not 'Time=' in line:
            raise CorruptedFile(f'last lines of {self.filename}/hv{self.date.year}{self.date.month}{self.date.day} is corrupted')
        time, step = line.split('=')[1].split(' , ')
        time = datetime.strptime(time, "%d-%m-%Y %H:%M:%S")
        line = next(hv_items_generator)
        headers = [header.strip() for header in line.split('\t')]
        hv_chanels = list()
        for chanel in hv_items_generator:
            chanel_info = [metric.strip() for metric in chanel.split('\t')]
            hv_chanels.append(HVChan(**dict(zip(headers, chanel_info))))
        return HVItem(time=time, step=step, chans=hv_chanels)