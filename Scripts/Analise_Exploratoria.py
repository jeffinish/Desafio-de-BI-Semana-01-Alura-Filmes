# Importando Bibliotecas

import pandas as pd
pd.set_option('display.float_format', '{:.2f}'.format)

# Importando base de dados
# df = pd.read_csv(r'H:\My Drive\1. ESTUDO\Desafio de BI - Semana 01 - Alura Filmes\Dados Brutos\Filmes.csv')
df = pd.read_csv(r'G:\My Drive\1. ESTUDO\Desafio de BI - Semana 01 - Alura Filmes\Dados Brutos\Filmes.csv')

# Primeiras informações
df.head()
df.info()

## Colunas com campos nulos
gross_null = df.Gross.isnull().sum()
print(f'Nossa base de dados possui {gross_null} entradas com a coluna Gross nula')
metascore_null = df.Meta_score.isnull().sum()
print(f'Nossa base de dados possui {metascore_null} entradas com a coluna Meta_score nula')
## Ajustando a coluna Gross para valores numéricos
df.Gross
df['Gross'] = pd.to_numeric(df.Gross.str.replace(',',''),downcast='float')
df.head()

# Respondendo algumas perguntas básicas:

## Quais foram os filmes mais votados

df_votes = df[['Series_Title','Noofvotes','Gross','Released_Year']]
df_votes.sort_values(by='Noofvotes',ascending=False,inplace=True)
df_votes
print("O Total de votos computados é: {}".format(df_votes.Noofvotes.sum()))
### Criando uma coluna com a porcentagem dos votos
df_votes['%Votes']= ((df_votes.Noofvotes/df_votes.Noofvotes.sum()).round(4))*100
df_votes

## Quais são os gêneros mais rentáveis

### Dividindo os múltiplos gêneros em colunas distintas
df_genres = df.Genre.str.split(',',expand=True)
df_genres

### Descobrindo quantos gêneros distintos existem:
n_genres = len(pd.concat([df_genres[0],df_genres[1],df_genres[2]]).unique())
print(f'Existem ao todo (a prinícipio) {n_genres} gêneros de filmes')
pd.concat([df_genres[0],df_genres[1],df_genres[2]]).unique()
### Trimando os espaços em branco
genres_all = pd.DataFrame(pd.concat([df_genres[0],df_genres[1],df_genres[2]]).drop_duplicates().sort_values())
genres_all
genres_all.sort_values(by=[0]).reset_index(drop=True,inplace=True)
genres_all[0] = genres_all[0].str.strip()
genres_all = genres_all.drop_duplicates().sort_values(by=[0]).reset_index(drop=True)
genres_all.rename(columns={0:'Genêro'},inplace=True)
genres_all

### Calculando o valor arrecadado por genero
genres_list = genres_all.iloc[:-1,0] #Ignorando o último que é o valor 'None'
gross_per_genre = pd.DataFrame()
for genre in genres_list:
    f = df[df['Genre'].str.contains(genre)]
    f['Gross'].sum()
    gpg_temp = {}
    gpg_temp['Gênero'] = genre
    gpg_temp['Gross'] = f['Gross'].sum().astype('float')
    gpg_temp
    t = pd.DataFrame([gpg_temp])
    t = t.astype({'Gross':'float'})
    gross_per_genre = pd.concat([gross_per_genre,t])


gross_per_genre['%Gross'] = ((gross_per_genre.Gross/gross_per_genre.Gross.sum()).round(4))*100
gross_per_genre.sort_values(by=['Gross'],ascending=False).reset_index(drop=True)[:4].sum()

## Estrelas que mais aparecem em filmes

### Considerando qualquer posição
all_stars = pd.concat([df.Star1,df.Star2,df.Star3,df.Star4]).drop_duplicates().reset_index(drop=True)
print(f'O número total de atores estrelando os filmes é {len(all_stars)}')
all_stars

stars = pd.DataFrame()
(df.values == 'Tim Robbins').any(1).sum()
for star in all_stars:
        a_star = (df.values == star).any(1).sum()
        s_temp = {}
        s_temp['Star'] = star
        s_temp['NofMovies'] = a_star
        s_temp = pd.DataFrame([s_temp])
        stars = pd.concat([stars,s_temp])

stars.reset_index(drop=True,inplace=True)
stars.sort_values(by=['NofMovies'],ascending=False)[:20]

### Considerando a ordem:
df.groupby('Star1').count()[['Id_Title']].sort_values(by=['Id_Title'],ascending=False)[:7]

df.groupby('Star2').count()[['Id_Title']].sort_values(by=['Id_Title'],ascending=False)[:7]
