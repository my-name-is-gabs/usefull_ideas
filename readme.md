# My How to

## Table of contents
- [Testing with localStorage in vue](#1)
- [Testing samples for my data initialization in todolist](#2)
- [helpful tip to ignore console warning or error](#3)
- [Setting up the coverage in pytest](#4)
- [Image upload by application/json using flask and vuejs](#5)
- [Populating data in flask](#6)
- [Serving static file in API using Flask](#7)

<hr>

### Testing with localStorage in vue <div id="1"></div>
```javascript
import { shallowMount } from '@vue/test-utils';
import SampleComponent from '@/components/SampleComponent.vue';

describe('SampleComponent', () => {
  beforeEach(() => {
    // Reset the mock before each test
    jest.clearAllMocks();
  });

  it('should set registeredUser to staticData when localStorage is empty', () => {
    // Mock localStorage to return null
    jest.spyOn(Storage.prototype, 'getItem').mockReturnValue(null);

    const wrapper = shallowMount(SampleComponent);
    expect(wrapper.vm.registeredUser).toEqual([{ ...staticData }]);
  });

  it('should parse users from localStorage if available', () => {
    // Mock localStorage with JSON data
    const mockUsers = [{ id: 1, name: 'John Doe' }];
    jest.spyOn(Storage.prototype, 'getItem').mockReturnValue(JSON.stringify(mockUsers));

    const wrapper = shallowMount(SampleComponent);
    expect(wrapper.vm.registeredUser).toEqual(mockUsers);
  });

  it('should handle invalid JSON gracefully', () => {
    // Mock localStorage to return invalid JSON
    jest.spyOn(Storage.prototype, 'getItem').mockReturnValue("invalid-json");

    expect(() => shallowMount(SampleComponent)).toThrow();
  });
});

```

<hr>

### Testing samples for my data initialization in todolist <div id="2"></div>
```javascript
import { shallowMount } from '@vue/test-utils'
import SampleComponent from '@/components/SampleComponent.vue'

// Static data mock
const staticData = { name: 'John Doe', email: 'john.doe@example.com' }

describe('SampleComponent.vue', () => {
  beforeEach(() => {
    // Clear any previous mock setup
    localStorage.clear()
  })

  it('should initialize registeredUser from localStorage', () => {
    // Arrange: Mocking localStorage
    const mockData = JSON.stringify([{ name: 'Jane Doe', email: 'jane.doe@example.com' }])
    localStorage.setItem('registeredUser', mockData)

    // Act: Mounting the component
    const wrapper = shallowMount(SampleComponent)
    
    // Assert: Check that registeredUser is initialized from localStorage
    expect(wrapper.vm.registeredUser).toEqual(JSON.parse(mockData))
  })

  it('should use staticData when localStorage is empty or null', () => {
    // Arrange: Mocking empty localStorage
    localStorage.setItem('registeredUser', null)

    // Act: Mounting the component
    const wrapper = shallowMount(SampleComponent)
    
    // Assert: Check that registeredUser is initialized with staticData
    expect(wrapper.vm.registeredUser).toEqual([staticData])
  })

  it('should handle invalid JSON in localStorage', () => {
    // Arrange: Mocking invalid JSON in localStorage
    localStorage.setItem('registeredUser', 'invalid JSON')

    // Act: Mounting the component
    const wrapper = shallowMount(SampleComponent)

    // Assert: Check that registeredUser falls back to staticData
    expect(wrapper.vm.registeredUser).toEqual([staticData])
  })

  it('should handle localStorage.getItem() throwing an error', () => {
    // Arrange: Mocking localStorage to throw an error
    jest.spyOn(localStorage, 'getItem').mockImplementationOnce(() => {
      throw new Error('Failed to retrieve from localStorage')
    })

    // Act: Mounting the component
    const wrapper = shallowMount(SampleComponent)

    // Assert: Check that registeredUser is still initialized with staticData
    expect(wrapper.vm.registeredUser).toEqual([staticData])

    // Clean up mock
    jest.restoreAllMocks()
  })

  it('should add staticData to registeredUser if it is empty', () => {
    // Arrange: Mocking localStorage to return an empty array
    localStorage.setItem('registeredUser', JSON.stringify([]))

    // Act: Mounting the component
    const wrapper = shallowMount(SampleComponent)

    // Assert: Check that staticData was added
    expect(wrapper.vm.registeredUser).toEqual([staticData])
  })
})
```
<hr>

### helpful tip to ignore console warning or error <div id="3"></div>
1. Removing b-color-mode warning
```js
jest.spyOn(console, 'warn').mockImplementation((message) => {
  if (message.includes('b-color-mode')) return; // Ignore specific warning
  console.warn(message); // Let other warnings through
});
```

2. removing console error
```js
jest.spyOn(console, 'error').mockImplementation((message) => {
  if (message.includes('location.reload')) return; // Ignore the error
  console.error(message); // Allow other errors
});
```
<hr>

### Setting up the coverage in pytest <div id="4"></div>
![image](https://github.com/user-attachments/assets/569a27f5-0bbb-4632-9654-175e336a7575)

<hr>

### Image upload by application/json using flask and vuejs <div id="5"></div>
#### Backend
```python
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import base64
from io import BytesIO
from PIL import Image
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///images.db'
app.config['UPLOAD_FOLDER'] = './uploaded_images'

db = SQLAlchemy(app)

class ImageModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(100), nullable=False)

db.create_all()

@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        data = request.json
        image_data = data.get("image")
        filename = data.get("filename", "default.png")

        # Decode Base64
        image_bytes = base64.b64decode(image_data.split(",")[1])  # Skip "data:image/..." prefix
        image = Image.open(BytesIO(image_bytes))

        # Save the image
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(save_path)

        # Save to database
        new_image = ImageModel(filename=filename)
        db.session.add(new_image)
        db.session.commit()

        return jsonify({"message": "Image uploaded successfully!", "filename": filename}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
```
#### Backend (testing)
```python
import unittest
import base64
import os
from io import BytesIO
from PIL import Image
from app import app, db, ImageModel

class TestUploadEndpoint(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create the test database
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_images.db'
        app.config['UPLOAD_FOLDER'] = './test_uploaded_images'
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        cls.client = app.test_client()
        with app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        # Clean up the database and files
        with app.app_context():
            db.session.remove()
            db.drop_all()
        if os.path.exists(app.config['UPLOAD_FOLDER']):
            for file in os.listdir(app.config['UPLOAD_FOLDER']):
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file))
            os.rmdir(app.config['UPLOAD_FOLDER'])

    def test_upload_success(self):
        # Create a test image in memory
        img = Image.new('RGB', (100, 100), color='red')
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        image_data = base64.b64encode(buffer.read()).decode('utf-8')
        base64_image = f"data:image/png;base64,{image_data}"

        # Prepare payload
        payload = {
            "image": base64_image,
            "filename": "test_image.png"
        }

        # Make the POST request
        response = self.client.post('/upload', json=payload)
        self.assertEqual(response.status_code, 201)
        self.assertIn("Image uploaded successfully!", response.get_json()["message"])

        # Verify the image is saved
        saved_file_path = os.path.join(app.config['UPLOAD_FOLDER'], "test_image.png")
        self.assertTrue(os.path.exists(saved_file_path))

        # Verify the database entry
        with app.app_context():
            image_entry = ImageModel.query.filter_by(filename="test_image.png").first()
            self.assertIsNotNone(image_entry)

    def test_upload_failure(self):
        # Payload missing the image
        payload = {
            "filename": "test_image.png"
        }

        response = self.client.post('/upload', json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())

    def test_upload_invalid_base64(self):
        # Payload with invalid Base64 data
        payload = {
            "image": "data:image/png;base64,INVALID_DATA",
            "filename": "test_image.png"
        }

        response = self.client.post('/upload', json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.get_json())

if __name__ == "__main__":
    unittest.main()
```

#### Frontend 
```vue
<template>
  <div class="container mt-5">
    <b-card title="Upload Image">
      <b-form @submit.prevent="handleSubmit">
        <b-form-group label="Choose an image">
          <b-form-file
            v-model="selectedFile"
            accept="image/*"
            @change="convertToBase64"
          ></b-form-file>
        </b-form-group>
        <b-button type="submit" variant="primary" :disabled="!base64Image">Upload</b-button>
      </b-form>
      <div v-if="message" class="mt-3 alert alert-info">{{ message }}</div>
    </b-card>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      selectedFile: null,
      base64Image: null,
      message: null,
    };
  },
  methods: {
    convertToBase64() {
      const file = this.selectedFile;
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          this.base64Image = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    },
    async handleSubmit() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/upload', {
          image: this.base64Image,
          filename: this.selectedFile.name,
        });
        this.message = response.data.message;
      } catch (error) {
        this.message = `Error: ${error.response?.data?.error || error.message}`;
      }
    },
  },
};
</script>

<style>
@import "bootstrap/dist/css/bootstrap.css";
@import "bootstrap-vue-next/dist/bootstrap-vue-next.css";
</style>
```

#### Frontend (testing)
```js
import { mount } from '@vue/test-utils';
import { describe, it, expect, vi } from 'vitest';
import UploadImage from '@/components/UploadImage.vue';
import axios from 'axios';

vi.mock('axios');

describe('UploadImage.vue', () => {
  it('handles successful image upload', async () => {
    // Mock axios.post response
    axios.post.mockResolvedValueOnce({
      data: { message: 'Image uploaded successfully!' },
    });

    // Mount the component
    const wrapper = mount(UploadImage);

    // Set up data
    wrapper.setData({
      base64Image: 'data:image/png;base64,somebase64data',
      selectedFile: { name: 'test.png' },
    });

    // Trigger the form submission
    await wrapper.find('form').trigger('submit.prevent');

    // Verify axios.post was called with the correct payload
    expect(axios.post).toHaveBeenCalledWith('http://127.0.0.1:5000/upload', {
      image: 'data:image/png;base64,somebase64data',
      filename: 'test.png',
    });

    // Verify the message was updated
    expect(wrapper.vm.message).toBe('Image uploaded successfully!');
  });

  it('handles failed image upload', async () => {
    // Mock axios.post to reject
    axios.post.mockRejectedValueOnce({
      response: { data: { error: 'Upload failed' } },
    });

    // Mount the component
    const wrapper = mount(UploadImage);

    // Set up data
    wrapper.setData({
      base64Image: 'data:image/png;base64,somebase64data',
      selectedFile: { name: 'test.png' },
    });

    // Trigger the form submission
    await wrapper.find('form').trigger('submit.prevent');

    // Verify the error message
    expect(wrapper.vm.message).toBe('Error: Upload failed');
  });
});
```

<hr>

### Populating data with flask <div id="6"></div>
```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

@app.cli.command('populate-db')
def populate_db():
    """Populate the database with sample data."""
    users = [
        User(name='Alice', email='alice@example.com'),
        User(name='Bob', email='bob@example.com'),
        User(name='Charlie', email='charlie@example.com'),
    ]
    db.session.bulk_save_objects(users)
    db.session.commit()
    print("Database populated successfully!")
```

<hr>

### Serving static files in API using Flask <div id="7"></div>
1. Save your static image in a directory like static/images in your Flask project structure
```
project/
│
├── app.py
├── static/
│   └── images/
│       └── example.jpg
```
2. Serve static files
#### Backend
```python
from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route('/api/image/<filename>')
def get_image(filename):
    return send_from_directory('static/images', filename)

if __name__ == '__main__':
    app.run(debug=True)
```
#### Backend (testing)
```python
import os
import pytest
from flask import Flask
from app import app  # Import the Flask app from your main script

# Create a pytest fixture for the Flask app
@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client

# Test case for retrieving an existing image
def test_get_image_success(client):
    # Arrange: Ensure the test image exists
    test_image_dir = 'static/images'
    test_image_name = 'test_image.jpg'
    test_image_path = os.path.join(test_image_dir, test_image_name)
    os.makedirs(test_image_dir, exist_ok=True)
    with open(test_image_path, 'wb') as f:
        f.write(b'Test Image Content')

    # Act: Make a GET request to the endpoint
    response = client.get(f'/api/image/{test_image_name}')

    # Assert: Verify the response
    assert response.status_code == 200
    assert response.data == b'Test Image Content'

    # Cleanup: Remove the test image
    os.remove(test_image_path)

# Test case for handling a non-existent image
def test_get_image_not_found(client):
    # Act: Make a GET request to a non-existent image
    response = client.get('/api/image/non_existent.jpg')

    # Assert: Verify the response
    assert response.status_code == 404
```

#### Frontend
```vue
<template>
  <div>
    <h1>Flask Image</h1>
    <img :src="imageUrl" alt="Example" v-if="imageUrl" />
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      imageUrl: null,
    };
  },
  mounted() {
    this.fetchImage();
  },
  methods: {
    async fetchImage() {
      try {
        // Fetch the URL from your backend
        const response = await axios.get('http://127.0.0.1:5000/images/example.jpg', {
          responseType: 'blob',
        });
        this.imageUrl = URL.createObjectURL(response.data);
      } catch (error) {
        console.error('Error fetching the image:', error);
      }
    },
  },
};
</script>
```

#### Frontend (testing)
```js
import { mount } from '@vue/test-utils';
import axios from 'axios';
import MockAdapter from 'axios-mock-adapter';
import MyComponent from '@/components/MyComponent.vue'; // Adjust path to your component

describe('MyComponent.vue', () => {
  let mock;

  beforeEach(() => {
    // Create a mock instance of axios
    mock = new MockAdapter(axios);
  });

  afterEach(() => {
    // Reset the mock adapter
    mock.reset();
  });

  it('fetches the image successfully and updates imageUrl', async () => {
    // Arrange: Mock the API response
    const mockImageBlob = new Blob(['Test Image Content'], { type: 'image/jpeg' });
    mock.onGet('http://127.0.0.1:5000/images/example.jpg').reply(200, mockImageBlob);

    // Act: Mount the component
    const wrapper = mount(MyComponent);
    await wrapper.vm.$nextTick(); // Wait for the mounted lifecycle hook to complete

    // Assert: Verify the image URL is updated
    expect(wrapper.vm.imageUrl).toBeTruthy(); // Ensure imageUrl is set
    expect(wrapper.html()).toContain('<img'); // Check if <img> tag is rendered
  });

  it('handles an error when the API call fails', async () => {
    // Arrange: Mock a failed API response
    mock.onGet('http://127.0.0.1:5000/images/example.jpg').reply(404);

    // Spy on console.error to verify error handling
    const consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});

    // Act: Mount the component
    const wrapper = mount(MyComponent);
    await wrapper.vm.$nextTick(); // Wait for the mounted lifecycle hook to complete

    // Assert: Verify imageUrl remains null and error is logged
    expect(wrapper.vm.imageUrl).toBeNull(); // imageUrl should not be set
    expect(consoleErrorSpy).toHaveBeenCalled(); // Ensure error was logged

    // Cleanup the console spy
    consoleErrorSpy.mockRestore();
  });
});

```








