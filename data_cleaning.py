import pandas as pd
import re

df = pd.read_csv('glassdoor_jobs.csv')

#salary parsing

df['hourly'] = df['Salary Estimate'].apply(lambda x: 1 if 'per hour' in x.lower() else 0)
df['employer_provided'] = df['Salary Estimate'].apply(lambda x: 1 if 'employer provided salary:' in x.lower() else 0)

df = df[df['Salary Estimate'] != '-1']
salary = df['Salary Estimate'].apply(lambda x: x.split('(')[0])
minus_Kd = salary.apply(lambda x: x.replace('K','').replace('$',''))

min_hr = minus_Kd.apply(lambda x: x.lower().replace('per hour','').replace('employer provided salary:',''))

df['min_salary'] = min_hr.apply(lambda x: int(x.split('-')[0]))
df['max_salary'] = min_hr.apply(lambda x: int(x.split('-')[1]))
df['avg_salary'] = (df.min_salary+df.max_salary)/2

#Company name text only
df['Rating'] = df['Rating'].apply(lambda x: -1 if not (re.search('[0-9].[0-9]', x)) else float(x))
df['company_txt'] = df.apply(lambda x: x['Company Name'] if x['Rating'] <0 else x['Company Name'][:-4], axis = 1)

#state field
df['job_state'] = df['Location'].apply(lambda x: x.split(',')[1])

#age of company
df['Founded'] = df['Founded'].apply(lambda x: -1 if not (re.search('[0-9]{4}', str(x))) else int(x))
df['age'] = df.Founded.apply(lambda x: x if x <1 else 2020 - x)

# parsing of job description (python, etc.)

# python
df['python_yn'] = df['Job Description'].apply(lambda x: 1 if 'python' in str(x).lower() else 0)

# r studio
df['R_yn'] = df['Job Description'].apply(lambda x: 1 if 'r studio' in str(x).lower() or 'r-studio' in str(x).lower() else 0)
df.R_yn.value_counts()

# spark
df['spark'] = df['Job Description'].apply(lambda x: 1 if 'spark' in str(x).lower() else 0)
df.spark.value_counts()

# aws
df['aws'] = df['Job Description'].apply(lambda x: 1 if 'aws' in str(x).lower() else 0)
df.aws.value_counts()

# excel
df['excel'] = df['Job Description'].apply(lambda x: 1 if 'excel' in str(x).lower() else 0)
df.excel.value_counts()

df_out = df.drop(['Unnamed: 0'], axis=1)

df_out.to_csv('C:/Users/alexa/OneDrive/Documentos/ds_salary_proj/salary_data_cleaned.csv', index=False)
