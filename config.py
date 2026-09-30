from dotenv import load_dotenv
import os

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
TEACHER_ID = int(os.getenv("TEACHER_ID"))

GROUP_ID = -1003765095754