from sklearn.preprocessing import LabelEncoder

def preprocess_data(df):
    df = df.drop(columns=['ID'])

    le_gender = LabelEncoder()
    df['Jenis Kelamin'] = le_gender.fit_transform(df['Jenis Kelamin'])

    le_target = LabelEncoder()
    df['Kategori Detak Jantung'] = le_target.fit_transform(df['Kategori Detak Jantung'])

    X = df.drop(columns=['Kategori Detak Jantung'])
    y = df['Kategori Detak Jantung']

    return X, y, le_gender, le_target
