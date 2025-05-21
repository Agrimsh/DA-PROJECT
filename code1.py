import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

df = pd.read_csv('C:/Users/user/Desktop/python programs/archive/netflix_titles.csv')
df.columns = df.columns.str.strip()
df.dropna(subset=['date_added'], inplace=True)
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
df['year_added'] = df['date_added'].dt.year
df['month_added'] = df['date_added'].dt.month
df['director'].fillna('Unknown', inplace=True)
df['cast'].fillna('Unknown', inplace=True)
df['country'].fillna('Unknown', inplace=True)
df['genre'] = df['listed_in'].str.split(',').str[0]
df['duration_value'] = pd.to_numeric(df['duration'].str.extract('(\d+)')[0], errors='coerce')
df['duration_type'] = df['duration'].str.extract(r'\d+\s*(\w+)')

plt.figure(figsize=(6,4))
sns.countplot(data=df, x='type', palette='Set2')
plt.title('Content Type Count')
plt.xlabel('Type')
plt.ylabel('Count')
plt.show()

country_counts = df['country'].value_counts().head(10)
plt.figure(figsize=(8,5))
sns.barplot(x=country_counts.values, y=country_counts.index, palette='viridis')
plt.title('Top 10 Countries with Most Titles')
plt.xlabel('Number of Titles')
plt.ylabel('Country')
plt.show()

genre_counts = df['genre'].value_counts().head(10)
plt.figure(figsize=(8,5))
sns.barplot(x=genre_counts.values, y=genre_counts.index, palette='coolwarm')
plt.title('Top 10 Genres')
plt.xlabel('Number of Titles')
plt.ylabel('Genre')
plt.show()

year_counts = df['year_added'].value_counts().sort_index()
plt.figure(figsize=(10,5))
sns.lineplot(x=year_counts.index, y=year_counts.values, marker='o')
plt.title('Titles Added Over the Years')
plt.xlabel('Year')
plt.ylabel('Number of Titles')
plt.grid(True)
plt.show()

month_counts = df['month_added'].value_counts().sort_index()
plt.figure(figsize=(10,5))
sns.barplot(x=month_counts.index, y=month_counts.values)
plt.title('Netflix Titles Added per Month')
plt.xlabel('Month')
plt.ylabel('Number of Titles')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

type_trend = df.groupby(['year_added', 'type']).size().unstack()
type_trend.plot(kind='line', marker='o', figsize=(12,6))
plt.title('Movies vs TV Shows Added Over the Years')
plt.xlabel('Year')
plt.ylabel('Number of Titles')
plt.grid(True)
plt.show()

top_directors = df['director'].value_counts().drop('Unknown').head(10)
plt.figure(figsize=(10,5))
sns.barplot(x=top_directors.values, y=top_directors.index)
plt.title('Top 10 Directors on Netflix')
plt.xlabel('Number of Titles')
plt.ylabel('Director')
plt.grid(axis='x', linestyle='--', alpha=0.7)
plt.show()

title_words = ' '.join(df['title'])
wordcloud = WordCloud(background_color='black', max_words=200, width=1200, height=600).generate(title_words)
plt.figure(figsize=(15,7))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Most Frequent Words in Netflix Titles', fontsize=18)
plt.show()

df.to_csv('cleaned_netflix_data.csv', index=False)
