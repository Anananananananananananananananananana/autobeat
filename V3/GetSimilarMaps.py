#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import libraries
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers


# In[2]:


# Constants
NUM_TOP_MAPS = 1024         # Number of popular maps to select
NUM_TOP_PLAYERS = 1024      # Number of prolific players to select
REPRESENTATION_SIZE = 11    # Size of skill/difficulty embedding
NUM_EPOCHS = 1000           # Number of epochs to train for
BATCH_SIZE = 10000          # Number of scores per batch


# In[3]:


# Load top players and maps
scores = pd.read_csv('AllScoresExtracted.csv')
scores = scores.query("Modifiers.isnull()").copy(deep=True)
top_maps = scores['LeaderboardId'].value_counts().iloc[:NUM_TOP_MAPS].index.tolist()
scores = scores.query('LeaderboardId in @top_maps').copy(deep=True)
top_players = scores['PlayerId'].value_counts().iloc[:NUM_TOP_PLAYERS].index.tolist()
scores = scores.query('PlayerId in @top_players').copy(deep=True)
scores['LeaderboardId'], maps = pd.factorize(scores['LeaderboardId'])
scores['PlayerId'], users = pd.factorize(scores['PlayerId'])


# In[4]:


# Select PlayerId, LeaderboardId as inputs, Accuracy as target
X_maps = []
X_users = []
y = []
for index, row in scores.iterrows():
    X_maps.append(row['LeaderboardId'])
    X_users.append(row['PlayerId'])
    y.append(row['Accuracy'])


# In[5]:


# Convert to one-hot encoding
X_maps = tf.one_hot(X_maps, depth=NUM_TOP_MAPS)
X_users = tf.one_hot(X_users, depth=NUM_TOP_PLAYERS)
y = np.array(y)


# In[6]:


# Define the model architecture
map_input = layers.Input(shape=(NUM_TOP_MAPS,))
map_embedding = layers.Dense(REPRESENTATION_SIZE)(map_input)
map_model = keras.Model(inputs=map_input, outputs=map_embedding)
map_model.compile(
    loss="mae",         # Use mse as the loss function
    optimizer="adam",   # Use adam as the optimizer
    metrics=["mae"]     # Use mae as the metric
)

map_input_2 = layers.Input(shape=(NUM_TOP_MAPS,))
map_embedding_2 = map_model(map_input_2)

user_input = layers.Input(shape=(NUM_TOP_PLAYERS,))
user_embedding = layers.Dense(REPRESENTATION_SIZE)(user_input)

output = layers.Dot(axes=1, normalize=False)([map_embedding_2, user_embedding])
output = layers.Dense(1, activation="linear")(output)
model = keras.Model(inputs=[map_input_2, user_input], outputs=output)


# In[7]:


# Compile the model with loss and metrics
model.compile(
    loss="mae",         # Use mse as the loss function
    optimizer="adam",   # Use adam as the optimizer
    metrics=["mae"]     # Use mae as the metric
)


# In[8]:


# Train the model
model.fit([X_maps, X_users], y, batch_size=BATCH_SIZE, epochs=NUM_EPOCHS)


# In[9]:


# Evaluate the model
model.evaluate([X_maps, X_users], y, batch_size=BATCH_SIZE)[-1]


# In[10]:


# Evaluate map ranks
test_maps = tf.one_hot(range(NUM_TOP_MAPS), depth=NUM_TOP_MAPS)
test_ranks = map_model.predict(test_maps, batch_size=BATCH_SIZE)


# In[11]:


# Normalize map ranks
test_ranks = [rank / np.linalg.norm(rank) for rank in test_ranks]


# In[20]:


# Compute similarity
target = '1944891'
target_rank = test_ranks[list(maps).index(target)]

results = []
for i in range(len(maps)):
    map = maps[i]
    rank = test_ranks[i]
    results.append((map, np.dot(rank, target_rank)))

results.sort(key=lambda el: el[1])

print('Target Map: https://www.beatleader.xyz/leaderboard/global/' + target)

print('\nMost Similar Maps:')
for i in range(2, 7):
    print(results[-i][1], ':', 'https://www.beatleader.xyz/leaderboard/global/' + results[-i][0])

print('\nLeast Similar Maps:')
for i in range(5):
    print(results[i][1], ':', 'https://www.beatleader.xyz/leaderboard/global/' + results[i][0])

print('\n')


# In[ ]:





# In[ ]:




