import tkinter as tk
from tkinter import filedialog
import numpy as np
from PIL import Image
from PIL import ImageTk
import skimage.transform 

def classify_image(category_var):
    # Declare "image" as a global variable
    global image

    # Load and preprocess the image
    image_path = filedialog.askopenfilename(initialdir="/", title="Select Image",
                                            filetypes=(("Image files", "*.jpg *.jpeg *.png *.gif"), ("All files", "*.*")))
    if image_path:
        try:
            image = Image.open(image_path)
            processed_image = preprocess_image(image)

            # Display the image
            display_image(image)
            
            # Perform image classification based on the selected category
            category = category_var.get()
            predicted_category = classify_category(category, processed_image)

            # Display the result
            result_label.config(text="Image classified as {}".format(predicted_category))
        except Exception as e:
            result_label.config(text="Error loading or processing image: {}".format(str(e)))
    else:
        result_label.config(text="No image selected")


def preprocess_image(image):
    # Convert image to grayscale
    image = image.convert("L")

    # Print the original image size
    print("Original image size:", image.size)

    # Resize the image to a fixed size (e.g., 224x224)
    image = image.resize((224, 224), resample=Image.BILINEAR)

    # Print the resized image size
    print("Resized image size:", image.size)

    # Convert the image to a numpy array
    image_array = np.array(image)

    # Normalize the pixel values to the range [0, 1]
    image_array = image_array / 255.0

    # Expand the dimensions of the image to match the input shape expected by the model
    image_array = np.expand_dims(image_array, axis=0)

    return image_array

def classify_category(category, image):
    # Implement the classification logic based on the user's input category
    # Here's an example rule-based approach
    if category.lower() == "top":
        return "Top"
    elif category.lower() == "bottom":
        return "Bottom"
    elif category.lower() == "shoes":
        return "Shoes"
    elif category.lower() == "hat":
        return "Hat"
    elif category.lower() == "accessory":
        return "Accessory"
    else:
        return "Unknown"
    
def display_image(image):
    # Resize the image to fit within a specified maximum width and height while preserving the aspect ratio
    max_width = 400
    max_height = 400
    image.thumbnail((max_width, max_height))

    # Convert the PIL Image to a Tkinter-compatible PhotoImage
    image_tk = ImageTk.PhotoImage(image)

    # Update the image label with the new image
    image_label.config(image=image_tk)
    image_label.image = image_tk  # Keep a reference to avoid garbage collection


# Create the main window
window = tk.Tk()

# Create a variable to store the selected category
category_var = tk.StringVar()

# Add a label and entry for category input
category_label = tk.Label(window, text="Category:")
category_label.pack()
category_dropdown = tk.OptionMenu(window, category_var, "Top", "Bottom", "Shoes", "Hat", "Accessory")
category_dropdown.pack()

# Add a button to select the image and perform classification
classify_button = tk.Button(window, text="Select Image", command=lambda: classify_image(category_var))
classify_button.pack()

# Add a label to display the classification result
result_label = tk.Label(window, text="")
result_label.pack()

# Add a label to display the uploaded image
image_label = tk.Label(window)
image_label.pack()

# Start the main event loop
window.mainloop()
