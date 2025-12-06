import os
import pickle
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import Adam

DATA_DIR = 'dataset/asl_alphabet_train/asl_alphabet_train'
SAVE_DIR = 'models'
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

MODEL_SAVE_PATH = os.path.join(SAVE_DIR, 'resnet_rgb_model.h5')
CLASS_SAVE_PATH = os.path.join(SAVE_DIR, 'classes_rgb.pkl')

IMG_SIZE = 224
BATCH_SIZE = 64
EPOCHS = 15

def train_model():
    print(f"--- STARTING MODEL TRAINING FROM: {DATA_DIR} ---")

    train_datagen = ImageDataGenerator(
        preprocessing_function=preprocess_input,
        validation_split=0.2
    )

    try:
        train_generator = train_datagen.flow_from_directory(
            DATA_DIR,
            target_size=(IMG_SIZE, IMG_SIZE),
            batch_size=BATCH_SIZE,
            class_mode='categorical',
            subset='training',
            shuffle=True
        )

        validation_generator = train_datagen.flow_from_directory(
            DATA_DIR,
            target_size=(IMG_SIZE, IMG_SIZE),
            batch_size=BATCH_SIZE,
            class_mode='categorical',
            subset='validation',
            shuffle=False
        )
    except Exception as e:
        print("PATH ERROR: Image not found. Please check the extracted folder.")
        print("Current path:", DATA_DIR)
        print("Folders in /content/dataset:", os.listdir('/content/dataset'))
        return

    class_names = list(train_generator.class_indices.keys())
    print(f"-> Found {len(class_names)} classes.")
    with open(CLASS_SAVE_PATH, 'wb') as f:
        pickle.dump(class_names, f)

    base_model = ResNet50(weights='imagenet', include_top=False, input_shape=(IMG_SIZE, IMG_SIZE, 3))
    for layer in base_model.layers:
        layer.trainable = False

    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(512, activation='relu')(x)
    x = Dropout(0.5)(x)
    predictions = Dense(len(class_names), activation='softmax')(x)

    model = Model(inputs=base_model.input, outputs=predictions)
    model.compile(optimizer=Adam(learning_rate=0.0001),
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    checkpoint = ModelCheckpoint(MODEL_SAVE_PATH, monitor='val_accuracy', save_best_only=True, verbose=1)
    early_stop = EarlyStopping(monitor='val_accuracy', patience=5, restore_best_weights=True)

    history = model.fit(
        train_generator,
        epochs=EPOCHS,
        validation_data=validation_generator,
        callbacks=[checkpoint, early_stop]
    )

    plt.plot(history.history['accuracy'], label='Train Accuracy')
    plt.plot(history.history['val_accuracy'], label='Val Accuracy')
    plt.title('Training Result')
    plt.legend()
    plt.show()

train_model()