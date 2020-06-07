from pathlib import Path

ROOT_API_PATH = Path('/api/v1')
SAMPLES_API_PATH = ROOT_API_PATH / 'samples'
NEIGHBOURS_API_PATH = lambda eid: SAMPLES_API_PATH / eid / 'nearest-neighbours'
