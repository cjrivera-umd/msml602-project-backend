import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
import sklearn.metrics as metrics
import pickle

# Get data
df = pd.read_csv('./preprocessed_results.csv')

# One Hot Encoding None Numeric Columns
ohe = OneHotEncoder()
encoded_features = ohe.fit_transform(df[['home_team', 'away_team', 'tournament', 'neutral']]).toarray()

feature_labels = ohe.categories_
feature_labels_flattened = np.hstack(feature_labels)

features_df = pd.DataFrame(encoded_features, columns=feature_labels_flattened)

# Create new dataframe
winner_df = df['winner']
cleaned_df = df[['home_team_win_percent', 'away_team_win_percent']]
final_df = pd.concat([cleaned_df, features_df], axis=1)
print(final_df.head())

# Split data
X_train, X_test, y_train, y_test = train_test_split(final_df, winner_df, test_size=0.2, stratify=winner_df)

# Model
mnb = MultinomialNB()
y_pred = mnb.fit(X_train, y_train)

# # Save model
# with open('model_pickle', 'wb') as f:
#     pickle.dump(y_pred, f)

# # Save one hot encoder
# with open('encoder_pickle', 'wb') as f:
#     pickle.dump(ohe, f)

# Accuracy
predicted_labels = y_pred.predict(X_test)
print(f'Accuracy  = {metrics.accuracy_score(predicted_labels,  y_test)}')
print(f'Dataframe Size: {len(df.index)} Rows')
print(f'Unique Home Teams: {len(df["home_team"].unique())}')
print(f'Unique Away Teams: {len(df["away_team"].unique())}')
print(f'Unique Tournaments: {len(df["tournament"].unique())}')

with open('model_pickle', 'rb') as f:
    model = pickle.load(f)
    predicted_labels_2 = model.predict(X_test)
    print(f'Accuracy  = {metrics.accuracy_score(predicted_labels_2,  y_test)}')


