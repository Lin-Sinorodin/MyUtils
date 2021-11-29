import os
import cv2
import numpy as np
from tabulate import tabulate
from tqdm.autonotebook import tqdm


class Video:
    def __init__(self, video_path: str):
        self.video_path = video_path
        self.video_cap = cv2.VideoCapture(video_path)

        self.num_frames = self._get_num_frames()
        self.fps = self._get_fps()
        self.height, self.width = self._get_frames_dimension()

    def __str__(self):
        return tabulate([
            ['Video path', self.video_path],
            ['Number of frames', self.num_frames],
            ['FPS', self.fps],
            ['(height, width)', f'({self.height}, {self.width})']
        ])

    def __iter__(self):
        for _ in range(self.num_frames):
            success, frame = self.video_cap.read()
            if success is False or frame is None:
                break
            yield frame

        self.video_cap.release()

    def _get_num_frames(self) -> int:
        num_frames = int(self.video_cap.get(cv2.CAP_PROP_FRAME_COUNT))
        assert num_frames > 0, 'The video contains 0 frames.'
        return num_frames

    def _get_fps(self) -> int:
        return int(self.video_cap.get(cv2.CAP_PROP_FPS))

    def _get_frames_dimension(self) -> tuple[int, int]:
        _, frame = cv2.VideoCapture(self.video_path).read()
        height, width, channels = frame.shape
        return height, width

    def export_frames(self, frames_path: str) -> None:
        os.makedirs(frames_path, exist_ok=True)
        file_name_zero_padding = len(str(self.num_frames))
        self.video_cap = cv2.VideoCapture(self.video_path)

        progress_bar_settings = {'desc': 'Exporting frames', 'unit': 'frame', 'total': self.num_frames}
        for count, frame in tqdm(enumerate(self), **progress_bar_settings):
            frame_number = str(count).zfill(file_name_zero_padding)
            frame_path = f'{frames_path}/{frame_number}.jpg'
            cv2.imwrite(frame_path, frame)

    def get_video_writer(self, video_path: str) -> cv2.VideoWriter:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        dimension = (self.width, self.height)
        return cv2.VideoWriter(video_path, fourcc, self.fps, dimension)

    def get_frames_tensor(self) -> np.array:
        return np.array([frame for frame in self])
