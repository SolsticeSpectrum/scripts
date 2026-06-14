import tensorflow as tf
from tensorflow import keras
import numpy as np

def get_input(prompt):
    try:
        return int(input(prompt))
    except ValueError:
        print("Please enter a valid integer.")
        return get_input(prompt)

def predict_next_input(model, test_number):
    predictions = model.predict(test_number)
    return np.argmax(predictions) + 1  # Add 1 to convert 0-indexed prediction to 1-10 range

def predictor():
    train_numbers = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
    train_labels = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9])

    model = keras.Sequential([
        keras.layers.Input(shape=(1,)),    
        keras.layers.Dense(10, activation='relu'),
        keras.layers.Dense(10, activation='softmax')   
    ])

    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    model.fit(train_numbers, train_labels, epochs=10)

    while True:
        user_input = get_input("Enter a number from 1 to 10 (or any other number to exit): ")
        
        if user_input < 1 or user_input > 10:
            print("Exiting the predictor.")
            break

        test_number = np.array([user_input])
        predicted_number = predict_next_input(model, test_number)

        print("You entered number:", user_input)
        print("The prediction was:", predicted_number)

predictor()
