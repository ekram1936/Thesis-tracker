from .mad_lab import scrape_mad_lab
from .pr_lab import scrape_pr_lab
from .lstm_lab import scrape_lstm_lab
from .chair_auto_control import scrape_chair_auto_control
from .asm_lab import scrape_asm_lab
from .i_meet_lab import scrape_i_meet
from .chair_info_sys_1 import scrape_information_systems


# Register scraper functions here, keyed by lab name.
SCRAPER_REGISTRY = {
    "MAD Lab": scrape_mad_lab,
    "PR Lab": scrape_pr_lab,
    "LSTM Lab": scrape_lstm_lab,
    "Chair of Automatic Control": scrape_chair_auto_control,
    "Chair of Autonomous Systems and Mechatronics": scrape_asm_lab,
    "I-Meet Lab": scrape_i_meet,
    "Chair of Information Systems I, Innovation and Value Creation": scrape_information_systems

}


# Function to retrieve scraper function by lab name.
def get_scraper_func(lab_name: str):
    return SCRAPER_REGISTRY.get(lab_name)
