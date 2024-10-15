# Depop Price Prediction with CNN and Transformer
This project implements a neural network to predict the price at which an item will sell on Depop based on its attributes such as the item’s image, description, brand, price listed, and size. The model consists of a Convolutional Neural Network (CNN) for processing item images, a Transformer-based description encoder using BERT for textual features, and fully connected layers to combine all data types. Prior to using the model, data is extracted (scraped) from Depop's website, note this is against their ToS and is not recommended.

## Project Structure
 - CNN Module: This processes the image data of the items.
 - Transformer Module: Uses BertModel to process and encode item descriptions.
 - Combined Model: The CNN, description embeddings, and other features (e.g., brand, size) are combined through fully connected layers for final price prediction.
 - Custom Loss and Evaluation Metrics: The model is trained with MSE loss for regression and evaluated with Mean Absolute Percentage Error (MAPE) and Mean Absolute Error (MAE).
## Model Overview
### Inputs:
 - Image: Item image (3-channel RGB, resized to 128x128).
 - Description: Item description, tokenized using BERT.
 - Other Features: One-hot encoded brand and size data, scaled price listed value.
### Outputs:
 - Price: The predicted price for which the item will sell.
## Requirements
To run this project, you’ll need the following Python libraries:
 - #### For the neural network portion:
   - Python 3.8+
   - PyTorch
   - Hugging Face's Transformers
   - Scikit-Learn
   - NumPy
   - Matplotlib
   - Pandas
 - #### For data extraction:
   - Selenium
   - Requests
   - PIL (Python Imaging Library)
   - Random
   - Time
   - Pandas   
## How to Run the Project
### 1. Data Preparation:
The scraping module is defined in retrieve_sold_items.py which is currently set to extract the link to the top image, the description, price listed, price sold, size, brand, date sold, location of sale (although note that the last two columns are dropped during processing). Then, as we want to avoid making requests to Depop's site, the images are saved to Drive in the save_images_to_drive.ipynb. Remaining preprocessing is handled in depop_price_cnn.py and should be tailored/modified for the dataset being used on the neural network.

### 2. Custom Transformer
The custom transformer is based on a pre-trained BERT model to process item descriptions. It is extended with transformer encoder layers and fully connected layers for text classification tasks.
```
class DescriptionTransformer(nn.Module):
    def __init__(self, bert_model_name='bert-base-uncased', num_encoder_layers=4):
        super(DescriptionTransformer, self).__init__()
        self.bert_model = BertModel.from_pretrained(bert_model_name)
        # Add transformer and fully connected layers
        # Additional transformer layers and FC layers to process descriptions
```

### 3. Model Initialization:
The model is defined in depop_price_cnn.py and includes the CNN for image features and the transformer-based description encoder. You can initialize the model as follows:
```
model = DepopPriceCNN()
```
### 4. Training:
The model is trained using the MSE loss function, with an optimizer like Adam. The code includes a training loop that calculates training loss and validation loss, along with MAPE metrics to evaluate model performance.
Example training loop:
```
for epoch in range(num_epochs):
    model.train()
    for batch in train_loader:
        # Perform forward pass, compute loss, backpropagation, and update parameters
        pass

    model.eval()
    for batch in val_loader:
        # Perform forward pass for validation and calculate metrics
        pass
 ```    
### 5. Visualization:

After training, visualize the training and validation loss, as well as the MAPE metric over time:
```
plt.plot(train_loss_list, label='Train Loss')
plt.plot(val_loss_list, label='Validation Loss')
plt.show()

plt.plot(train_accuracy_list, label='Train MAPE')
plt.plot(val_accuracy_list, label='Validation MAPE')
plt.show()
```
## Future Improvements
The CNN-BERT model is currently running on 41% error, which isn't too great. Note that this is according to my dataset of shop sales, which only amounts to about 450. Over time, more sales should be used for training the neural network.
 - Hyperparameter Tuning: Experiment with different learning rates, batch sizes, and dropout rates.
 - Data Augmentation: Augment the dataset with more examples or use augmentation techniques for image data.
 - BERT Fine-Tuning: Currently, the BERT model is frozen, but you could enable fine-tuning of BERT's layers to improve performance on your specific dataset.
## Acknowledgments
 - Depop for supplying sellers with shop stats
 - Hugging Face Transformers for providing the pre-trained BERT model.
 - PyTorch for the deep learning framework.
## Disclaimer
While this project involves extracting data for the purpose of training a neural network model, I do not condone or encourage scraping Depop or any other website without permission. Always ensure you are in compliance with the website's terms of service and legal guidelines when accessing and using their data. If needed, reach out to the platform for permission or use their official API if available.
## License
This project is not licensed for public or private use. No permission is granted to copy, modify, distribute, or use the code contained in this repository without explicit permission from the author.
