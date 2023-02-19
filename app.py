import streamlit as st
import pandas as pd

print(pd.__version__)
print(st.__version__)

pd.options.display.max_columns = 11_509
st.set_page_config(layout="wide")

VIDEOS_TO_SHOW = 40
df = pd.read_csv('kargin_processed.csv')

# էս հեչ
# df.rename(columns={'Unnamed: 8': 'place'}, inplace=True)
# df['haytni_srtshsetutun'].fillna('', inplace=True)
# df['text'].fillna('', inplace=True)
# df['all_text'] = df['haytni_srtshsetutun'] + ' ' + df['text']


# cols_to_keep = ['titles', 'links', 'haytni_srtshsetutun', 'text', 'characters',
#                 'number_of_actors', 'character_name', 'place', 'light','languages', 'all_text']

# df = df[cols_to_keep]
# df.to_csv('kargin_processed.csv', index=False)	

def get_unique_by_frequency(col_name):
    return list(df[col_name].value_counts().index.unique())

places = ['չեմ հիշում'] + get_unique_by_frequency('place')
lights = ['չեմ հիշում'] + get_unique_by_frequency('light')
languages = ['չեմ հիշում'] + get_unique_by_frequency('languages')

# streamlit app start
st.title('Կարգին search')

text = st.text_input('Գրեք որևէ արտահայտություն որը հիշում եք, այն լեզվով որով որ ասվում է')
search_exact = st.checkbox('Արդյո՞ք փնտրենք հստակ համընկնում (եթե վստահ եք որ հենց այպիսի)')
place = st.multiselect("Ընտրեք թե ինչ վայրում է տեղի ունեցել Կարգինը", options=places)
light = st.selectbox("Ընտրեք թե ինչպիսի լուսավորություն էր", options=lights)
lang = st.selectbox("Ընտրեք թե ինչ լեզվով/լեզուներով են խոսում կարգինում", options=languages)
actor_count = st.number_input("Քանի՞ դերասան կա կարգինում", min_value=0, max_value=20, step=1, value=0)


df_filter = df.copy()
#print('len initial df', len(df))


# filters by place
for p in place:
    if p:
        df_filter = df_filter[df_filter['place'] == p]
#        print(f'df len after filtering place to be {place}')

# filters by light and language
for i, col_name in zip([light, lang], ['light', 'languages']):
    if i != 'չեմ հիշում':
        df_filter = df_filter[df_filter[col_name] == i]
#        print(f'After filtering by {col_name} len -> {len(df_filter)}')

# filters by actor count
if actor_count:
    df_filter = df_filter[df_filter['number_of_actors'] == str(int(actor_count))]
#    print(f'df len after filtering actor count == {actor_count}')

def search_text_exact(df, text):
    indexes = []
    # temporary solution
    for i in range(len(df)):
        if text in df.iloc[i]['all_text']:
            indexes.append(i)
    
    return df.iloc[indexes]

def fuzzy_search(df, text):
    # to do
    pass

if text:
    # only works for exact match now
    df_filter = search_text_exact(df_filter, text)
    df_filter = search_text_exact(df_filter, text)
#    print(f'Len df after exact text({text}) filter ->', len(df_filter))


st.write('Գտնված կարգինների քանակը', len(df_filter))
st.write('եթե մեծաքանակ կարգիններ են գտնվել փորձեք նշել տեքստ/վայր/լուսավորություն/լեզու որ ավելի լավ փնտրենք')
# st.write(df_filter)


c1, c2, c3, c4 = st.columns(4)
cols = [c1, c2, c3, c4]

links = list(df_filter['links'].values)

# if len(links) < VIDEOS_TO_SHOW:
#     print(type(links))
#     links = links + [''] * (VIDEOS_TO_SHOW - len(links))
# else:
links = links[:40]

for i, link in enumerate(links):  
    with cols[i % 4]:
        st.video(link)


# with c1:
#     print(df_filter.iloc[0].links)
#     st.video(df_filter.iloc[0].links)

# with c2:
#     st.video(df_filter.iloc[1].links)

# if len(df_filter) > 2:
#     with c3:
#         st.video(df_filter.iloc[2].links)
    



# # print(df_filter)


