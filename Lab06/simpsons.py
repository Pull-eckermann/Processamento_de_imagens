import numpy as np
import tensorflow as tf
import keras
from keras.layers import GlobalAveragePooling2D, Dense, Dropout
from keras.models import Model
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.applications import ResNet50
from keras.applications.resnet import preprocess_input

# Tamanho imagem
img_rows, img_cols = 224, 224

input_shape = (img_rows, img_cols, 3)

#Batch size

batch_size = 32

path_train = './simpsons/Treino'
path_test = './simpsons/Valid/'

#Apresentando base de dados
train_dataset = tf.keras.utils.image_dataset_from_directory(
        path_train,
        image_size=(img_rows, img_cols),
        color_mode="rgb",
        batch_size=batch_size,
        shuffle=False)
test_dataset = tf.keras.utils.image_dataset_from_directory(
        path_test,
        image_size=(img_rows, img_cols),
        color_mode="rgb",
        batch_size=batch_size,
        shuffle=False)

AUTOTUNE = tf.data.AUTOTUNE

train_dataset = train_dataset.cache().prefetch(buffer_size=AUTOTUNE) #Otimização
test_dataset = test_dataset.cache().prefetch(buffer_size=AUTOTUNE)

#============================TREINANDO BASE======================
# Parâmetros
num_classes = 6

n_epochs = 100

batch_size = 32

seed = 42

# loss
loss = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
# métricas
metrics = ['accuracy']  

#Data augmentation
data_augmentation = tf.keras.Sequential([tf.keras.layers.experimental.preprocessing.RandomFlip('horizontal_and_vertical'),
                                         tf.keras.layers.experimental.preprocessing.RandomZoom(0.2),
                                         tf.keras.layers.experimental.preprocessing.RandomContrast(0.2, 0.2)])

#Criando modelo
resnet50 = ResNet50(weights='imagenet', include_top=False, input_shape=input_shape) #Corta camadas
resnet50.trainable = False #Para o primeiro treinamento as camadas convolucionais não serão treinadas
inputs = keras.Input(shape=input_shape)
x = data_augmentation(inputs)
x = preprocess_input(x)
x = resnet50(x, training=False) #Camadas de Batch Normalization em inference mode
x = GlobalAveragePooling2D()(x)
x = keras.layers.Dropout(0.4)(x) # Camada de Dropout
predictions = Dense(num_classes)(x) #Camada Densa sem ativação, pois a loss foi definida como from_logits=True
model = Model(inputs, predictions)

#Treinamento camada densa
opt_dense = keras.optimizers.Adam()
model.compile(metrics=metrics, loss=loss, optimizer=opt_dense)
callbacks_dense = [EarlyStopping(patience=10)]
history_dense =model.fit(train_dataset, epochs=n_epochs, verbose=1, validation_data=test_dataset, callbacks=callbacks_dense)

##Treinamento completo
#esnet50.trainable = True #Liberando todas as camadas com excessão das camadas de Batch Normalization
#pt_completo = keras.optimizers.Adam(learning_rate=0.00001)
#odel.compile(metrics=metrics, loss=loss, optimizer=opt_completo)
#allbacks_dense_completo = [EarlyStopping(patience=15), 
#                           ModelCheckpoint(filepath='./modelo/', save_weights_only=False, 
#                                           verbose=1, monitor='val_accuracy', mode='max', 
#                                           save_best_only=True)]
#istory_completo = model.fit(train_dataset, epochs=n_epochs, verbose=1, validation_data=test_dataset, callbacks=callbacks_dense_completo)
#best_model = tf.keras.models.load_model('./modelo/')

#=====================VETOR DE CARACTERISTICAS====================
#Extraindo características
X_train = model.predict(train_dataset)
X_test = model.predict(test_dataset)
y_train = np.concatenate([y for x, y in train_dataset], axis=0)
y_test = np.concatenate([y for x, y in test_dataset], axis=0)

#==============================RESULTS=============================
import sys
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn import preprocessing

# cria um kNN
neigh = KNeighborsClassifier(n_neighbors=1, metric='euclidean')
print ('Fitting knn')
neigh.fit(X_train, y_train)

# predicao do classificador
print ('Predicting...')
y_pred = neigh.predict(X_test)

# mostra o resultado do classificador na base de teste
print ('Accuracy: ',  neigh.score(X_test, y_test))

# cria a matriz de confusao
cm = confusion_matrix(y_test, y_pred)
print (cm)
print(classification_report(y_test, y_pred))






##Criando extrator modelo (Mais simplificado porém com melhor acurácia)
#cnn = ResNet50(weights='imagenet', include_top=False, input_shape=input_shape)
#inputs = keras.Input(shape=input_shape)
#x = preprocess_input(inputs)
#x = cnn(x)
#output = GlobalAveragePooling2D()(x)
#model = Model(inputs, output)