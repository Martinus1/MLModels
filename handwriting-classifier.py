import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dense, Dropout, Flatten

pixel_width = 28
pixel_height = 28
batch_size = 32
epochs = 10

num_of_classes = 10

(features_train, labels_train), (features_test, labels_test) = mnist.load_data()

print(features_train.shape)

features_train = features_train.reshape(features_train.shape[0], pixel_width, pixel_height ,1)
features_test = features_test.reshape(features_test.shape[0], pixel_width, pixel_height ,1)

input_shape = (pixel_width, pixel_height, 1)

features_train = features_train.astype('float32')
features_test = features_test.astype('float32')

features_train /= 255
features_test /= 255

labels_train = keras.utils.to_categorical(labels_train, num_of_classes)
labels_test = keras.utils.to_categorical(labels_test, num_of_classes)

model = Sequential()
model.add(Conv2D(32, kernel_size=(3,3), activation = 'relu', input_shape=input_shape))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation = 'relu'))
model.add(Dense(num_of_classes, activation='softmax'))

model.compile(loss= keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adadelta(),
              metrics=['accuracy'])

model.fit(features_train, labels_train,
            batch_size= batch_size,
            epochs= epochs,
            verbose=1,
            validation_data=(features_test,labels_test))

score = model.evaluate(features_test, labels_test, verbose=0)

model.save('/Users/martin_michalko/Desktop/handwriting_model.h5')


import coremltools
coreml_model = coremltools.converters.keras.convert(model, input_names=['image'], image_input_names=['image'])

coreml_model.author = 'martin_michalko'
coreml_model.license = 'MIT'
coreml_model.short_description = 'Predicts character passed in as a number 1-9.'
coreml_model.input_description['image'] = 'A 28x28 pixel grayscale image.'
coreml_model.output_description['output1'] = 'A multiarray where the index with the greatest float value (0-1) is the recognized digit.'

coreml_model.save('/Users/martin_michalko/Desktop/handwriting.mlmodel')
