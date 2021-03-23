import scraping_glassdoor_selenium as gs
import pandas as pd

path = "C:/Users/alexa/OneDrive/Documentos/ds_salary_proj/chromedriver"

df = gs.get_jobs('data scientist', 'US', 15, False, path, 15)
