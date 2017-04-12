import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

%matplotlib inline
sns.set(style='white', font_scale=0.9)

dataset = pd.read_csv('../input/loan.csv')

#missing value
#basic idea: categorize, then find out value
dataset['verification_status_joint'].fillna(dataset['verification_status'], inplace=True)

strColumns = dataset.select_dtypes(include=['object']).columns.values
dataset[strColumns] = dataset[strColumns].fillna('Unknown')
dataset.select_dtypes(exclude=[np.number]).isnull().sum()

dataset[dataset['application_type'] != 'INDIVIDUAL']['annual_inc_joint'].isnull().sum()

dataset['annual_inc_joint'].fillna(dataset['annual_inc'], inplace=True)
dataset['dti_joint'].fillna(dataset['dti'], inplace=True)

strColumns = dataset.select_dtypes(include=[np.number]).columns.values
dataset[strColumns] = dataset[strColumns].fillna(dataset[strColumns].mean())

#final check: if there is NaN values
dataset.select_dtypes(include=[np.number]).isnull().sum()

#create identification variable(default)
dataset['loan_status'].value_counts()
dataset = dataset[~dataset['loan_status'].isin(['Issued',
                                 'Does not meet the credit policy. Status:Fully Paid',
                                 'Does not meet the credit policy. Status:Charged Off'
                                ])
def CreateDefault(Loan_Status):
    if Loan_Status in ['Current', 'Fully Paid', 'In Grace Period']:
        return 0
    else:
        return 1 
    
dataset['Default'] = dataset['loan_status'].apply(lambda x: CreateDefault(x))

#explore other categories
dataset['term'].value_counts()

dataset['emp_length'].value_counts()

def EmpLength(emp_len):
    if emp_len[:2] == '10':
        return 10
    elif emp_len[:1] in ['<', 'n']:
        return 0
    else:
        return int(emp_len[:1])
    
dataset['Emp_Length_Years'] = dataset['emp_length'].apply(lambda x: EmpLength(x))
dataset['purpose'].value_counts()
dataset['grade'].value_counts().sort_index()

dataset['Earliest_Cr_Line_Yr'] = pd.to_numeric(dataset['earliest_cr_line'].str[-4:], errors='coerce').round(0)

#visualization of late payment
nNoLate = len(dataset[dataset['Default'] == 0])
nLate = len(dataset[dataset['Default'] == 1])

f, (ax1, ax2, ax3) = plt.subplots(1, 3, sharey=True, figsize=(9, 3))

sns.barplot(x='grade', y='id', data=dataset, 
            estimator=lambda x: len(x) / (nLate + nNoLate) * 100,
            ax=ax1, order=sorted(dataset['grade'].unique()), palette='deep')
sns.barplot(x='grade', y='id', data=dataset[dataset['Default'] == 0], 
            estimator=lambda x: len(x) / nNoLate * 100,
            ax=ax2, order=sorted(dataset['grade'].unique()), palette='deep')
sns.barplot(x='grade', y='id', data=dataset[dataset['Default'] == 1], 
            estimator=lambda x: len(x) / nLate * 100,
            ax=ax3, order=sorted(dataset['grade'].unique()), palette='deep')

ax1.set_title('Overall')
ax2.set_title('No Default')
ax3.set_title('Default')
ax1.set_ylabel('Percentage')
ax2.set_ylabel('')
ax3.set_ylabel('')

plt.tight_layout()
plt.show()

#visualization of loan amount
f, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 3))

sns.distplot(dataset[dataset['Default'] == 0]['loan_amnt'], bins=40, ax=ax1, kde=False)
sns.distplot(dataset[dataset['Default'] == 1]['loan_amnt'], bins=40, ax=ax2, kde=False)

ax1.set_title('No Default')
ax2.set_title('Default')

ax1.set_xbound(lower=0)
ax2.set_xbound(lower=0)

plt.tight_layout()
plt.show()

ax1 = sns.violinplot(x='Default', y='loan_amnt', data=dataset)
ax1.set_ybound(lower=0)
plt.show()

#visualization of loan term
nNoLate = len(dataset[dataset['Default'] == 0])
nLate = len(dataset[dataset['Default'] == 1])

f, (ax1, ax2, ax3) = plt.subplots(1, 3, sharey=True, figsize=(9, 3))

sns.barplot(x='term', y='id', data=dataset, 
            estimator=lambda x: len(x) / (nLate + nNoLate) * 100,
            ax=ax1, order=sorted(dataset['term'].unique()), palette='deep')
sns.barplot(x='term', y='id', data=dataset[dataset['Default'] == 0], 
            estimator=lambda x: len(x) / nNoLate * 100,
            ax=ax2, order=sorted(dataset['term'].unique()), palette='deep')
sns.barplot(x='term', y='id', data=dataset[dataset['Default'] == 1], 
            estimator=lambda x: len(x) / nLate * 100,
            ax=ax3, order=sorted(dataset['term'].unique()), palette='deep')

ax1.set_title('Overall')
ax2.set_title('No Default')
ax3.set_title('Default')
ax1.set_ylabel('Percentage')
ax2.set_ylabel('')
ax3.set_ylabel('')

plt.tight_layout()
plt.show()

#interest rate
f, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 3))

sns.distplot(dataset[dataset['Default'] == 0]['int_rate'], bins=30, ax=ax1, kde=False)
sns.distplot(dataset[dataset['Default'] == 1]['int_rate'], bins=30, ax=ax2, kde=False)

ax1.set_title('No Default')
ax2.set_title('Default')

ax1.set_xbound(lower=0)
ax2.set_xbound(lower=0)

plt.tight_layout()
plt.show()

ax1 = sns.boxplot(x='Default', y='int_rate', data=dataset)
ax1.set_ybound(lower=0)
plt.show()

ax1 = sns.boxplot(x='grade', y='int_rate', data=dataset, hue='Default', 
                     order=sorted(dataset['grade'].unique()))
ax1.set_ybound(lower=0)
plt.show()

#home ownship
nNoLate = len(dataset[dataset['Default'] == 0])
nLate = len(dataset[dataset['Default'] == 1])

f, (ax1, ax2, ax3) = plt.subplots(1, 3, sharey=True, figsize=(9, 3))

sns.barplot(x='home_ownership', y='id', data=dataset, 
            estimator=lambda x: len(x) / (nLate + nNoLate) * 100,
            ax=ax1, order=['MORTGAGE', 'OWN', 'RENT'], palette='deep')
sns.barplot(x='home_ownership', y='id', data=dataset[dataset['Default'] == 0], 
            estimator=lambda x: len(x) / nNoLate * 100,
            ax=ax2, order=['MORTGAGE', 'OWN', 'RENT'], palette='deep')
sns.barplot(x='home_ownership', y='id', data=dataset[dataset['Default'] == 1], 
            estimator=lambda x: len(x) / nLate * 100,
            ax=ax3, order=['MORTGAGE', 'OWN', 'RENT'], palette='deep')

ax1.set_title('Overall')
ax2.set_title('No Default')
ax3.set_title('Default')
ax1.set_ylabel('Percentage')
ax2.set_ylabel('')
ax3.set_ylabel('')

plt.tight_layout()
plt.show()





