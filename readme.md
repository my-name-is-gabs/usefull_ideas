# Get some help

### Testing with localStorage in vue
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

### Testing samples for my data initialization in todolist
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

### helpful tip to ignore console warning or error
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

### Setting up the coverage in pytest
![image](https://github.com/user-attachments/assets/569a27f5-0bbb-4632-9654-175e336a7575)

