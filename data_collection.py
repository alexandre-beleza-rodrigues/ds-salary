import scraping_glassdoor_selenium as gs
import pandas as pd

path = "C:/Users/alexa/OneDrive/Documentos/ds_salary_proj/chromedriver"

df = gs.get_jobs('data scientist', 'US', 2000, False, path, 15)

df.to_csv('C:/Users/alexa/OneDrive/Documentos/ds_salary_proj/glassdoor_jobs.csv')
