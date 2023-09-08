# Import libraries
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# Constants
NUM_TOP_MAPS = 1024         # Number of popular maps to select
NUM_TOP_PLAYERS = 1024      # Number of prolific players to select
REPRESENTATION_SIZE = 11    # Size of skill/difficulty embedding
NUM_EPOCHS = 1000           # Number of epochs to train for
BATCH_SIZE = 10000          # Number of scores per batch

# Load top players and maps
scores = pd.read_csv('AllScoresExtracted.csv')
scores = scores.query("Modifiers.isnull()").copy(deep=True)
top_maps = scores['LeaderboardId'].value_counts().iloc[:NUM_TOP_MAPS].index.tolist()
scores = scores.query('LeaderboardId in @top_maps').copy(deep=True)
top_players = scores['PlayerId'].value_counts().iloc[:NUM_TOP_PLAYERS].index.tolist()
scores = scores.query('PlayerId in @top_players').copy(deep=True)
scores['LeaderboardId'] = pd.factorize(scores['LeaderboardId'])[0]
scores['PlayerId'] = pd.factorize(scores['PlayerId'])[0]

# Select PlayerId, LeaderboardId as inputs, Accuracy as target
X_maps = []
X_users = []
y = []
for index, row in scores.iterrows():
    X_maps.append(row['LeaderboardId'])
    X_users.append(row['PlayerId'])
    y.append(row['Accuracy'])

# Convert to one-hot encoding
X_maps = tf.one_hot(X_maps, depth=NUM_TOP_MAPS)
X_users = tf.one_hot(X_users, depth=NUM_TOP_PLAYERS)
y = np.array(y)

# Define the model architecture
map_input = layers.Input(shape=(NUM_TOP_MAPS,))
user_input = layers.Input(shape=(NUM_TOP_PLAYERS,))
map_embedding = layers.Dense(REPRESENTATION_SIZE)(map_input)
user_embedding = layers.Dense(REPRESENTATION_SIZE)(user_input)
output = layers.Dot(axes=1, normalize=False)([map_embedding, user_embedding])
output = layers.Dense(1, activation="exponential")(output)
model = keras.Model(inputs=[map_input, user_input], outputs=output)

# Compile the model with loss and metrics
model.compile(
    loss="mae",         # Use mse as the loss function
    optimizer="adam",   # Use adam as the optimizer
    metrics=["mae"]     # Use mae as the metric
)

# Train the model
model.fit([X_maps, X_users], y, batch_size=BATCH_SIZE, epochs=NUM_EPOCHS)

# Save model
model.save('saved_model')

# Evaluate the model
model.evaluate([X_maps, X_users], y, batch_size=BATCH_SIZE)[-1]




