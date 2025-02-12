import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

class HotdogClassifier:
    def __init__(self, input_size, hidden_size=64):
        # Initialize weights and biases
        self.W1 = np.random.randn(input_size, hidden_size) * 0.01
        self.b1 = np.zeros((1, hidden_size))
        self.W2 = np.random.randn(hidden_size, 1) * 0.01
        self.b2 = np.zeros((1, 1))
    
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))
    
    def sigmoid_derivative(self, x):
        return x * (1 - x)
    
    def forward(self, X):
        # Forward propagation
        self.z1 = np.dot(X, self.W1) + self.b1
        self.a1 = self.sigmoid(self.z1)
        self.z2 = np.dot(self.a1, self.W2) + self.b2
        self.a2 = self.sigmoid(self.z2)
        return self.a2
    
    def backward(self, X, y, learning_rate=0.01):
        m = X.shape[0]
        
        # Backward propagation
        dz2 = self.a2 - y
        dW2 = np.dot(self.a1.T, dz2) / m
        db2 = np.sum(dz2, axis=0, keepdims=True) / m
        
        dz1 = np.dot(dz2, self.W2.T) * self.sigmoid_derivative(self.a1)
        dW1 = np.dot(X.T, dz1) / m
        db1 = np.sum(dz1, axis=0, keepdims=True) / m
        
        # Update parameters
        self.W2 -= learning_rate * dW2
        self.b2 -= learning_rate * db2
        self.W1 -= learning_rate * dW1
        self.b1 -= learning_rate * db1
    
    def train(self, X, y, epochs=1000, learning_rate=0.01):
        for epoch in range(epochs):
            # Forward and backward pass
            self.forward(X)
            self.backward(X, y, learning_rate)
            
            if epoch % 100 == 0:
                loss = np.mean(-y * np.log(self.a2) - (1 - y) * np.log(1 - self.a2))
                print(f"Epoch {epoch}, Loss: {loss:.4f}")
    
    def predict(self, X, threshold=0.5):
        predictions = self.forward(X)
        return (predictions >= threshold).astype(int)

def preprocess_image(image):
    # Assuming image is a numpy array of shape (height, width, channels)
    # Resize and flatten the image
    flattened = image.reshape(1, -1)
    # Scale pixel values to [0, 1]
    return flattened / 255.0

def main():
    # Example usage (you'll need to prepare your own dataset)
    # X should be your image data (n_samples, n_features)
    # y should be your labels (1 for hotdog, 0 for not hotdog)
    
    # Assuming you have X and y prepared
    # X = ... # Your image data
    # y = ... # Your labels
    
    # Split the data
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Initialize and train the model
    # input_size = X_train.shape[1]  # number of pixels in flattened image
    # model = HotdogClassifier(input_size)
    # model.train(X_train, y_train)
    
    # Make predictions
    # predictions = model.predict(X_test)
    # accuracy = np.mean(predictions == y_test)
    # print(f"Test accuracy: {accuracy:.4f}")

if __name__ == "__main__":
    main()
