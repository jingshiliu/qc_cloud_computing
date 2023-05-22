from keras.datasets import mnist
from keras.utils import to_categorical
from keras import optimizers
from keras import layers
from keras import models
import tensorflow as tf


(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

train_images = train_images.reshape((60000,28,28,1))
train_images = train_images.astype('float32')/255

test_images = test_images.reshape((10000,28,28,1))
test_images = test_images.astype('float32')/255

train_labels = to_categorical(train_labels)
test_labels = to_categorical(test_labels)


def create_model():
    model = models.Sequential()
    model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu'))
    model.add(layers.Flatten())
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dense(10, activation='softmax'))
    return model

strategy = tf.distribute.MirroredStrategy()
with strategy.scope():
    model = create_model()
    model.summary()
    model.compile(optimizer=optimizers.SGD(learning_rate=0.01, momentum=0.9),
                loss='categorical_crossentropy',
                metrics=['accuracy']
                )

BATCH_SIZE = 64
model.fit(train_images, train_labels, epochs=1, batch_size=BATCH_SIZE)

model.evaluate(test_images, test_labels)[1]
model.save('./mnist_model')