HELPER_PATH = r"C:\Users\Calin PC\Documents\Proiecte\linux_monitoring_project\helper"
CONFIG_PATH = (
    r"C:\Users\Calin PC\Documents\Proiecte\linux_monitoring_project\data\config.txt"
)
SQL_QUERY = "SELECT * FROM public.records"
DATABASE = "POSTGRESQL"
CONST_COLS = ["devtmpfs", "irq", "steal", "guest", "mem_total", "swap_total"]
FEATURES = [
    "sys",
    "sys_diff",
    "sys_diff_mean_ratio",
    "sys_diff_threshold_ratio",
    "usr",
    "sda1",
]
N_ESTIMATORS = 100
MAX_SAMPLES = "auto"
RANDOM_STATE = 42
