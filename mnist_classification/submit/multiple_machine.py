import tensorflow as tf
import os
from keras.datasets import mnist
from keras.utils import to_categorical
from keras import optimizers
from keras import layers
from keras import models
import tensorflow as tf

BATCH_SIZE = 64
model_path = "gs://qc_cloud/mnist_classification_multiworkermirrored"

def _is_chief(task_type):
    return task_type == 'chief'
 
 
def _get_temp_dir(dirpath, task_id):
    base_dirpath = 'workertemp_' + str(task_id)
    temp_dir = os.path.join(dirpath, base_dirpath)
    tf.io.gfile.makedirs(temp_dir)
    return temp_dir

 
def write_filepath(filepath, task_type, task_id):
    dirpath = os.path.dirname(filepath)
    base = os.path.basename(filepath)
    if not _is_chief(task_type):
        dirpath = _get_temp_dir(dirpath, task_id)
    return os.path.join(dirpath, base)


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

    model.compile(optimizer=optimizers.SGD(learning_rate=0.01, momentum=0.9),
                loss='categorical_crossentropy',
                metrics=['accuracy']
                )
    return model


def main():
    (train_images, train_labels), (test_images, test_labels) = mnist.load_data()

    train_images = train_images.reshape((60000,28,28,1))
    train_images = train_images.astype('float32')/255

    test_images = test_images.reshape((10000,28,28,1))
    test_images = test_images.astype('float32')/255

    train_labels = to_categorical(train_labels)
    test_labels = to_categorical(test_labels)

    strategy = tf.distribute.MultiWorkerMirroredStrategy()

    with strategy.scope():
        model = create_model()

    model.fit(train_images, train_labels, epochs=20, batch_size=BATCH_SIZE)

    task_type, task_id = (strategy.cluster_resolver.task_type,
                        strategy.cluster_resolver.task_id)
    

    write_model_path = write_filepath(model_path, task_type, task_id)
    model.save(write_model_path)
    model.evaluate(test_images, test_labels)[1]


if __name__ == "__main__":
    main()
    